import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


project_root = Path(__file__).resolve().parents[1]

dimensions_sql_path = project_root / "sql" / "06_load_dimensions.sql"
fact_sql_path = project_root / "sql" / "08_load_fact_sales.sql"

load_dotenv(project_root / ".env")


def load_warehouse():
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

        # Load any new dimension values
        with open(
            dimensions_sql_path,
            "r",
            encoding="utf-8"
        ) as sql_file:
            dimensions_sql = sql_file.read()

        print("Loading new dimension values...")
        cursor.execute(dimensions_sql)

        # Load only new fact rows
        with open(
            fact_sql_path,
            "r",
            encoding="utf-8"
        ) as sql_file:
            fact_sql = sql_file.read()

        print("Loading new fact rows...")
        cursor.execute(fact_sql)

        new_fact_rows = cursor.rowcount

        # Validate fact table
        cursor.execute("""
            SELECT
                COUNT(*) AS fact_rows,
                COUNT(DISTINCT invoice_id) AS unique_invoices
            FROM warehouse.fact_sales;
        """)

        fact_rows, unique_invoices = cursor.fetchone()

        connection.commit()

        print("Warehouse load complete.")
        print(f"New fact rows inserted: {new_fact_rows}")
        print(f"Total fact rows: {fact_rows}")
        print(f"Unique invoices: {unique_invoices}")

    except Exception as error:
        if connection:
            connection.rollback()

        print("Warehouse load failed.")
        print(error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    load_warehouse()