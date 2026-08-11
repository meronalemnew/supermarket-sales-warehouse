import sys

from load_raw_incremental import load_incremental_raw
from load_staging import load_staging
from load_warehouse import load_warehouse
from quality_checks import run_quality_checks


def run_pipeline(csv_path):
    print("Starting supermarket data pipeline...\n")

    load_incremental_raw(csv_path)
    print()

    load_staging()
    print()

    load_warehouse()
    print()

    run_quality_checks()
    print()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python python/run_pipeline.py "
            "<csv_file>"
        )
        sys.exit(1)

    run_pipeline(sys.argv[1])