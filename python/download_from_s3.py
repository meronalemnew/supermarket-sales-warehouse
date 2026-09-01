import sys
from pathlib import Path, PurePosixPath

import boto3


BUCKET_NAME = "meron-supermarket-data-pipeline"
AWS_REGION = "us-east-1"


project_root = Path(__file__).resolve().parents[1]
landing_dir = project_root / "data" / "landing"


def download_from_s3(s3_key):
    landing_dir.mkdir(parents=True, exist_ok=True)

    file_name = PurePosixPath(s3_key).name
    local_file = landing_dir / file_name

    session = boto3.Session(
        region_name=AWS_REGION,
    )

    s3 = session.client("s3")

    print(f"Downloading s3://{BUCKET_NAME}/{s3_key}...")

    s3.download_file(
        BUCKET_NAME,
        s3_key,
        str(local_file),
    )

    print(f"Downloaded successfully to: {local_file}")

    return str(local_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python python/download_from_s3.py "
            "<s3_key>"
        )
        sys.exit(1)

    download_from_s3(sys.argv[1])