import sys
from pathlib import PurePosixPath

import boto3


BUCKET_NAME = "meron-supermarket-data-pipeline"
PROCESSED_PREFIX = "processed/"
AWS_PROFILE = "supermarket-dev"
AWS_REGION = "us-east-1"


def archive_s3_file(source_key):
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )

    s3 = session.client("s3")

    file_name = PurePosixPath(source_key).name
    destination_key = f"{PROCESSED_PREFIX}{file_name}"

    print(
        f"Archiving s3://{BUCKET_NAME}/{source_key}"
    )

    # Copy the object into processed/
    s3.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={
            "Bucket": BUCKET_NAME,
            "Key": source_key,
        },
        Key=destination_key,
    )

    # Delete the original from incoming/
    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=source_key,
    )

    print(
        f"Archived to s3://{BUCKET_NAME}/{destination_key}"
    )

    return destination_key


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python python/archive_s3_file.py "
            "<s3_key>"
        )
        sys.exit(1)

    archive_s3_file(sys.argv[1])