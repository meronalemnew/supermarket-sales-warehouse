import sys
from datetime import timedelta
from pathlib import Path

import pendulum
from airflow.sdk import PokeReturnValue, dag, task


project_root = Path(__file__).resolve().parents[2]
python_dir = project_root / "python"

sys.path.insert(0, str(python_dir))


from list_s3_files import list_incoming_files
from download_from_s3 import download_from_s3
from load_raw_incremental import load_incremental_raw
from load_staging import load_staging
from load_warehouse import load_warehouse
from quality_checks import run_quality_checks
from archive_s3_file import archive_s3_file


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


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
    default_args=default_args,
    tags=["supermarket", "data-engineering", "aws"],
)
def supermarket_pipeline():

    @task.sensor(
        poke_interval=10,
        timeout=300,
        mode="reschedule",
        soft_fail=True,
    )
    def wait_for_s3_file() -> PokeReturnValue:
        files = list_incoming_files()

        if not files:
            return PokeReturnValue(
                is_done=False
            )

        return PokeReturnValue(
            is_done=True,
            xcom_value=files[0],
        )

    @task
    def download_file(s3_key: str):
        return download_from_s3(s3_key)

    @task
    def load_raw(local_file: str):
        load_incremental_raw(local_file)

    @task
    def load_staging_task():
        load_staging()

    @task
    def load_warehouse_task():
        load_warehouse()

    @task
    def quality_checks_task():
        run_quality_checks()

    @task
    def archive_file(
        s3_key: str,
        local_file: str,
    ):
        archive_s3_file(s3_key)

        local_path = Path(local_file)

        if local_path.exists():
            local_path.unlink()
            print(
                f"Removed local file: {local_path}"
            )

    s3_key = wait_for_s3_file()

    local_file = download_file(s3_key)

    raw = load_raw(local_file)
    staging = load_staging_task()
    warehouse = load_warehouse_task()
    quality = quality_checks_task()
    archive = archive_file(
        s3_key,
        local_file,
    )

    raw >> staging >> warehouse >> quality >> archive


supermarket_pipeline()