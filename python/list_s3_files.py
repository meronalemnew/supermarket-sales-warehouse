import boto3


BUCKET_NAME = "meron-supermarket-data-pipeline"
INCOMING_PREFIX = "incoming/"
AWS_PROFILE = "supermarket-dev"
AWS_REGION = "us-east-1"


def list_incoming_files():
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )

    s3 = session.client("s3")

    paginator = s3.get_paginator("list_objects_v2")

    files = []

    for page in paginator.paginate(
        Bucket=BUCKET_NAME,
        Prefix=INCOMING_PREFIX,
    ):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            # Skip the folder marker itself
            if key == INCOMING_PREFIX:
                continue

            if key.lower().endswith(".csv"):
                files.append(key)

    if not files:
        print("No CSV files found in S3 incoming/.")
        return []

    print("Incoming S3 files:")

    for key in files:
        print(f"- {key}")

    return files


if __name__ == "__main__":
    list_incoming_files()