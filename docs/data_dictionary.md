# Data Dictionary

This document describes the main tables and dbt models used in the Supermarket Sales Data Engineering Pipeline.

## raw.supermarket_sales

Raw landing table populated by the Python ingestion process.

The source values are stored as text so that typing and transformation can be handled downstream by dbt.

The grain is one row per source invoice transaction.

## dbt_dev.stg_supermarket_sales

Cleaned and typed staging model created from `raw.supermarket_sales`.

The grain remains one row per invoice transaction.

Key transformations include:

- trimming text fields
- converting numeric fields
- converting sale dates to `DATE`
- converting sale times to `TIME`

## dbt_dev.dim_branch

One row per supermarket branch.

| Column | Description |
|---|---|
| branch_key | Surrogate key for the branch |
| branch | Source branch identifier |
| city | City associated with the branch |

## dbt_dev.dim_product_line

One row per product-line category.

| Column | Description |
|---|---|
| product_line_key | Surrogate key for the product line |
| product_line | Product-line category |

## dbt_dev.dim_customer_segment

One row per customer-type and gender combination.

| Column | Description |
|---|---|
| customer_segment_key | Surrogate key for the customer segment |
| customer_type | Customer membership type |
| gender | Gender value from the source data |

## dbt_dev.dim_payment

One row per payment method.

| Column | Description |
|---|---|
| payment_key | Surrogate key for the payment method |
| payment | Payment method such as Cash, Credit card, or Ewallet |

## dbt_dev.dim_date

One row per sale date.

| Column | Description |
|---|---|
| date_key | Date key in YYYYMMDD format |
| sale_date | Calendar date of the transaction |
| year | Calendar year |
| quarter | Calendar quarter |
| month | Month number |
| month_name | Month name |
| day | Day of the month |
| day_name | Weekday name |

## dbt_dev.dim_time

One row per distinct transaction time.

| Column | Description |
|---|---|
| time_key | Time key in HHMM format |
| sale_time | Transaction time |
| hour | Hour of the day |
| minute | Minute of the hour |
| time_of_day | Morning, Afternoon, or Evening |

## dbt_dev.fact_sales

Central fact table for supermarket sales.

Grain:

**One row per invoice transaction**

The model is materialized incrementally using `invoice_id` as its unique key.

| Column | Description |
|---|---|
| invoice_id | Unique invoice identifier from the source |
| branch_key | Foreign key to `dim_branch` |
| product_line_key | Foreign key to `dim_product_line` |
| customer_segment_key | Foreign key to `dim_customer_segment` |
| payment_key | Foreign key to `dim_payment` |
| date_key | Foreign key to `dim_date` |
| time_key | Foreign key to `dim_time` |
| unit_price | Unit price of the product |
| quantity | Number of units purchased |
| tax_5_percent | Five-percent tax amount |
| total | Transaction total including tax |
| cogs | Cost of goods sold |
| gross_margin_percentage | Gross-margin percentage from the source |
| gross_income | Gross income from the transaction |
| rating | Customer rating |

## snapshots.dim_branch_snapshot

Historical snapshot of branch attributes used to demonstrate Slowly Changing Dimension Type 2 behavior.

The snapshot uses `branch` as the unique business key and tracks changes to `city`.

dbt adds metadata columns such as:

| Column | Description |
|---|---|
| dbt_scd_id | dbt-generated identifier for a historical version |
| dbt_updated_at | Timestamp associated with the snapshot version |
| dbt_valid_from | Time when the version became valid |
| dbt_valid_to | Time when the version stopped being current; NULL for the current version |