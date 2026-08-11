from load_raw import load_raw_data
from load_staging import load_staging
from load_warehouse import load_warehouse
from quality_checks import run_quality_checks


def run_pipeline():
    print("Starting supermarket data pipeline...\n")

    load_raw_data()
    print()

    load_staging()
    print()

    load_warehouse()
    print()

    run_quality_checks()
    print()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()