import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


project_root = Path(__file__).resolve().parents[1]
sql_path = project_root / "sql" / "04_load_staging.sql"

load_dotenv(project_root / ".env")


def load_staging():
    connection = None
    cursor = None

    try:
        print("Connecting to PostgreSQL...")

        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        cursor = connection.cursor()

        print("Connected successfully.")

        # Read the staging transformation SQL
        with open(sql_path, "r", encoding="utf-8") as sql_file:
            staging_sql = sql_file.read()

        print("Transforming new raw rows into staging...")

        # Insert only rows that are not already in staging
        cursor.execute(staging_sql)

        inserted_rows = cursor.rowcount

        # Validate the staging table
        cursor.execute("""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT invoice_id) AS unique_invoices
            FROM staging.supermarket_sales_clean;
        """)

        total_rows, unique_invoices = cursor.fetchone()

        connection.commit()

        print("Staging load complete.")
        print(f"New staging rows inserted: {inserted_rows}")
        print(f"Total staging rows: {total_rows}")
        print(f"Unique invoices: {unique_invoices}")

    except Exception as error:
        if connection:
            connection.rollback()

        print("Staging load failed.")
        print(error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    load_staging()