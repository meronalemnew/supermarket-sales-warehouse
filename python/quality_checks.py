import os

import psycopg2
from dotenv import load_dotenv
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")


def run_quality_checks():
    connection = None

    try:
        print("Running data quality checks...")

        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                (SELECT COUNT(*)
                 FROM raw.supermarket_sales) AS raw_rows,

                (SELECT COUNT(*)
                 FROM staging.supermarket_sales_clean) AS staging_rows,

                (SELECT COUNT(*)
                 FROM warehouse.fact_sales) AS fact_rows,

                (SELECT COUNT(DISTINCT invoice_id)
                 FROM warehouse.fact_sales) AS unique_fact_invoices,

                (SELECT SUM(total)
                 FROM staging.supermarket_sales_clean) AS staging_revenue,

                (SELECT SUM(total)
                 FROM warehouse.fact_sales) AS warehouse_revenue,

                (SELECT SUM(quantity)
                 FROM staging.supermarket_sales_clean) AS staging_quantity,

                (SELECT SUM(quantity)
                 FROM warehouse.fact_sales) AS warehouse_quantity,

                (SELECT SUM(gross_income)
                 FROM staging.supermarket_sales_clean) AS staging_gross_income,

                (SELECT SUM(gross_income)
                 FROM warehouse.fact_sales) AS warehouse_gross_income,

                (
                    SELECT COUNT(*)
                    FROM warehouse.fact_sales
                    WHERE branch_key IS NULL
                       OR product_line_key IS NULL
                       OR customer_segment_key IS NULL
                       OR payment_key IS NULL
                       OR date_key IS NULL
                       OR time_key IS NULL
                ) AS missing_dimension_keys;
        """)

        result = cursor.fetchone()

        (
            raw_rows,
            staging_rows,
            fact_rows,
            unique_fact_invoices,
            staging_revenue,
            warehouse_revenue,
            staging_quantity,
            warehouse_quantity,
            staging_gross_income,
            warehouse_gross_income,
            missing_dimension_keys,
        ) = result

        if not (raw_rows == staging_rows == fact_rows):
            raise ValueError(
                f"Row-count mismatch: raw={raw_rows}, "
                f"staging={staging_rows}, fact={fact_rows}"
            )

        if unique_fact_invoices != fact_rows:
            raise ValueError(
                "Duplicate invoice IDs found in fact_sales."
            )

        if staging_revenue != warehouse_revenue:
            raise ValueError("Revenue reconciliation failed.")

        if staging_quantity != warehouse_quantity:
            raise ValueError("Quantity reconciliation failed.")

        if staging_gross_income != warehouse_gross_income:
            raise ValueError("Gross income reconciliation failed.")

        if missing_dimension_keys != 0:
            raise ValueError(
                f"{missing_dimension_keys} fact rows have missing dimension keys."
            )

        print("Data quality checks passed.")
        print(f"Rows reconciled: {fact_rows}")
        print(f"Revenue reconciled: {warehouse_revenue}")
        print(f"Quantity reconciled: {warehouse_quantity}")
        print(f"Gross income reconciled: {warehouse_gross_income}")
        print("Missing dimension keys: 0")

        cursor.close()

    except Exception as error:
        print("Data quality checks failed.")
        print(error)
        raise

    finally:
        if connection:
            connection.close()