import shutil
import sys
from datetime import timedelta
from pathlib import Path

import pendulum
from airflow.sdk import PokeReturnValue, dag, task


project_root = Path(__file__).resolve().parents[2]
python_dir = project_root / "python"

sys.path.insert(0, str(python_dir))

from load_raw_incremental import load_incremental_raw
from load_staging import load_staging
from load_warehouse import load_warehouse
from quality_checks import run_quality_checks


landing_dir = project_root / "data" / "landing"
processed_dir = project_root / "data" / "processed"


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
    tags=["supermarket", "data-engineering"],
)
def supermarket_pipeline():

    @task.sensor(
        poke_interval=10,
        timeout=300,
        mode="reschedule",
    )
    def wait_for_sales_file() -> PokeReturnValue:
        files = sorted(landing_dir.glob("*.csv"))

        if not files:
            return PokeReturnValue(is_done=False)

        sales_file = str(files[0])

        return PokeReturnValue(
            is_done=True,
            xcom_value=sales_file,
        )

    @task
    def load_raw(file_path: str):
        load_incremental_raw(file_path)

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
    def archive_file(file_path: str):
        processed_dir.mkdir(exist_ok=True)

        source = Path(file_path)
        destination = processed_dir / source.name

        shutil.move(str(source), str(destination))

        print(f"Archived file: {destination}")

    sales_file = wait_for_sales_file()

    raw = load_raw(sales_file)
    staging = load_staging_task()
    warehouse = load_warehouse_task()
    quality = quality_checks_task()
    archive = archive_file(sales_file)

    raw >> staging >> warehouse >> quality >> archive


supermarket_pipeline()