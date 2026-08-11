import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")


def load_incremental_raw(csv_path):
    connection = None

    try:
        print(f"Loading file: {csv_path}")

        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        cursor = connection.cursor()

        # Temporary table for the incoming CSV
        cursor.execute("""
            CREATE TEMP TABLE incoming_sales
            (LIKE raw.supermarket_sales);
        """)

        copy_sql = """
        COPY incoming_sales (
            invoice_id,
            branch,
            city,
            customer_type,
            gender,
            product_line,
            unit_price,
            quantity,
            tax_5_percent,
            total,
            sale_date,
            sale_time,
            payment,
            cogs,
            gross_margin_percentage,
            gross_income,
            rating
        )
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ',',
            QUOTE '"'
        );
        """

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            cursor.copy_expert(copy_sql, csv_file)

        # Insert only invoices that are not already in raw
        cursor.execute("""
            INSERT INTO raw.supermarket_sales
            SELECT i.*
            FROM incoming_sales i
            WHERE NOT EXISTS (
                SELECT 1
                FROM raw.supermarket_sales r
                WHERE r.invoice_id = i.invoice_id
            );
        """)

        inserted_rows = cursor.rowcount

        cursor.execute("""
            SELECT COUNT(*)
            FROM raw.supermarket_sales;
        """)

        total_raw_rows = cursor.fetchone()[0]

        connection.commit()

        print(f"New rows inserted: {inserted_rows}")
        print(f"Total raw rows: {total_raw_rows}")

        cursor.close()

    except Exception as error:
        if connection:
            connection.rollback()

        print("Incremental load failed.")
        print(error)
        raise

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python python/load_raw_incremental.py "
            "<csv_file>"
        )
        sys.exit(1)

    load_incremental_raw(sys.argv[1])