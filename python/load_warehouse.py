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
        print("Clearing warehouse tables...")

        cursor.execute("""
            TRUNCATE TABLE
                warehouse.fact_sales,
                warehouse.dim_branch,
                warehouse.dim_product_line,
                warehouse.dim_customer_segment,
                warehouse.dim_payment,
                warehouse.dim_date,
                warehouse.dim_time
            RESTART IDENTITY;
        """)

        with open(dimensions_sql_path, "r", encoding="utf-8") as sql_file:
            dimensions_sql = sql_file.read()

        print("Loading dimensions...")
        cursor.execute(dimensions_sql)

        with open(fact_sql_path, "r", encoding="utf-8") as sql_file:
            fact_sql = sql_file.read()

        print("Loading fact_sales...")
        cursor.execute(fact_sql)

        cursor.execute("""
            SELECT
                COUNT(*) AS fact_rows,
                COUNT(DISTINCT invoice_id) AS unique_invoices
            FROM warehouse.fact_sales;
        """)

        fact_rows, unique_invoices = cursor.fetchone()

        connection.commit()

        print("Warehouse load complete.")
        print(f"Fact rows: {fact_rows}")
        print(f"Unique invoices: {unique_invoices}")

        cursor.close()

    except Exception as error:
        if connection:
            connection.rollback()

        print("Warehouse load failed.")
        print(error)
        raise

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    load_warehouse()