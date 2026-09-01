import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import pendulum
from airflow.sdk import PokeReturnValue, dag, task


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

project_root = Path(__file__).resolve().parents[2]

python_dir = project_root / "python"
dbt_dir = project_root / "dbt"

dbt_executable = project_root / ".dbt-venv" / "bin" / "dbt"


sys.path.insert(0, str(python_dir))


# ---------------------------------------------------------
# Project imports
# ---------------------------------------------------------

from list_s3_files import list_incoming_files
from download_from_s3 import download_from_s3
from load_raw_incremental import load_incremental_raw
from archive_s3_file import archive_s3_file


# ---------------------------------------------------------
# Default Airflow settings
# ---------------------------------------------------------

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


# ---------------------------------------------------------
# DAG
# ---------------------------------------------------------

@dag(
    dag_id="supermarket_sales_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(
        2026,
        8,
        12,
        tz="America/New_York",
    ),
    catchup=False,

    # Prevent two DAG runs from processing
    # the same S3 file at the same time.
    max_active_runs=1,

    default_args=default_args,
    tags=[
        "supermarket",
        "data-engineering",
        "aws",
        "dbt",
    ],
)
def supermarket_pipeline():

    # -----------------------------------------------------
    # 1. Wait for a CSV file in S3 incoming/
    # -----------------------------------------------------

    @task.sensor(
        poke_interval=10,
        timeout=300,
        mode="reschedule",
        soft_fail=True,
    )
    def wait_for_s3_file() -> PokeReturnValue:

        files = list_incoming_files()

        if not files:
            print("No incoming CSV file found.")

            return PokeReturnValue(
                is_done=False
            )

        selected_file = files[0]

        print(
            f"Detected incoming file: {selected_file}"
        )

        return PokeReturnValue(
            is_done=True,
            xcom_value=selected_file,
        )

    # -----------------------------------------------------
    # 2. Download file from S3
    # -----------------------------------------------------

    @task
    def download_file(s3_key: str):

        print(
            f"Downloading incoming file: {s3_key}"
        )

        local_file = download_from_s3(s3_key)

        return local_file

    # -----------------------------------------------------
    # 3. Incrementally load raw PostgreSQL table
    # -----------------------------------------------------

    @task
    def load_raw(local_file: str):

        print(
            f"Starting incremental raw load: {local_file}"
        )

        load_incremental_raw(local_file)

        print("Raw load completed.")

    # -----------------------------------------------------
    # 4. Run dbt transformations + tests
    # -----------------------------------------------------

    @task
    def dbt_build():

        print("Starting dbt build...")

        print(
            f"dbt project directory: {dbt_dir}"
        )

        print(
            f"dbt executable: {dbt_executable}"
        )

        if not dbt_executable.exists():
            raise FileNotFoundError(
                f"dbt executable not found: "
                f"{dbt_executable}"
            )

        result = subprocess.run(
            [
                str(dbt_executable),
                "build",
                "--select",
                "+fact_sales",
            ],
            cwd=str(dbt_dir),
            check=True,
        )

        print(
            "dbt build completed successfully."
        )

        print(
            f"dbt return code: "
            f"{result.returncode}"
        )

    # -----------------------------------------------------
    # 5. Archive processed S3 file
    # -----------------------------------------------------

    @task
    def archive_file(
        s3_key: str,
        local_file: str,
    ):

        print(
            f"Archiving successfully "
            f"processed file: {s3_key}"
        )

        archive_s3_file(s3_key)

        # Remove downloaded local copy
        local_path = Path(local_file)

        if local_path.exists():
            local_path.unlink()

            print(
                f"Removed local file: "
                f"{local_path}"
            )

        print("Archive step completed.")

    # -----------------------------------------------------
    # Task definitions
    # -----------------------------------------------------

    s3_key = wait_for_s3_file()

    local_file = download_file(
        s3_key
    )

    raw = load_raw(
        local_file
    )

    dbt = dbt_build()

    archive = archive_file(
        s3_key,
        local_file,
    )

    # -----------------------------------------------------
    # Dependency order
    # -----------------------------------------------------

    raw >> dbt >> archive


supermarket_pipeline()