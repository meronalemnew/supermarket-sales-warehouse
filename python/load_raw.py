import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


project_root = Path(__file__).resolve().parents[1]
csv_path = project_root / "data" / "supermarket_sales_clean.csv"

load_dotenv(project_root / ".env")


def load_raw_data():
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

        cursor.execute("TRUNCATE TABLE raw.supermarket_sales;")

        copy_sql = """
        COPY raw.supermarket_sales (
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

        print("Loading CSV...")

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            cursor.copy_expert(copy_sql, csv_file)

        cursor.execute("""
            SELECT
                COUNT(*),
                COUNT(invoice_id),
                COUNT(DISTINCT invoice_id)
            FROM raw.supermarket_sales;
        """)

        total_rows, non_null_invoice_ids, unique_invoices = cursor.fetchone()

        connection.commit()

        print("Load complete.")
        print(f"Total rows: {total_rows}")
        print(f"Non-null invoice IDs: {non_null_invoice_ids}")
        print(f"Unique invoices: {unique_invoices}")

        cursor.close()

    except Exception as error:
        if connection:
            connection.rollback()

        print("Load failed.")
        print(error)
        raise

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    load_raw_data()