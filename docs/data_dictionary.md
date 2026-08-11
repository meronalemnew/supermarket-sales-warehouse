# Data Dictionary

This document describes the main tables and columns used in the Supermarket Sales Data Warehouse.

## warehouse.dim_branch

Stores the supermarket branch and city information.

| Column | Description |
|---|---|
| branch_key | Surrogate key used to identify each branch in the warehouse |
| branch_code | Original branch code from the source data |
| city | City where the branch is located |

## warehouse.dim_product_line

Stores the product categories from the source data.

| Column | Description |
|---|---|
| product_line_key | Surrogate key for each product line |
| product_line | Product category, such as Food and beverages or Health and beauty |

## warehouse.dim_customer_segment

Stores customer segments based on customer type and gender.

| Column | Description |
|---|---|
| customer_segment_key | Surrogate key for each customer segment |
| customer_type | Customer type: Member or Normal |
| gender | Gender value from the source data |

## warehouse.dim_payment

Stores the payment methods used in sales transactions.

| Column | Description |
|---|---|
| payment_key | Surrogate key for each payment method |
| payment_method | Cash, Credit card, or Ewallet |


## warehouse.dim_date

Stores calendar information for each sale date.

| Column | Description |
|---|---|
| date_key | Date key in YYYYMMDD format |
| full_date | Full calendar date |
| day | Day of the month |
| month | Month number |
| month_name | Month name |
| quarter | Calendar quarter |
| year | Calendar year |
| day_of_week | Name of the weekday |

## warehouse.dim_time

Stores time information for each transaction time.

| Column | Description |
|---|---|
| time_key | Time key in HHMM format |
| full_time | Full transaction time |
| hour | Hour of the day |
| minute | Minute of the hour |
| time_of_day | Morning, Afternoon, or Evening |

## warehouse.fact_sales

Stores the sales transactions and the measures used for reporting.

The grain of this table is one row per invoice transaction.

| Column | Description |
|---|---|
| sales_key | Surrogate key for each fact row |
| invoice_id | Invoice number from the source data |
| branch_key | Foreign key to dim_branch |
| product_line_key | Foreign key to dim_product_line |
| customer_segment_key | Foreign key to dim_customer_segment |
| payment_key | Foreign key to dim_payment |
| date_key | Foreign key to dim_date |
| time_key | Foreign key to dim_time |
| unit_price | Unit price recorded in the transaction |
| quantity | Number of units sold |
| tax_5_percent | 5% tax amount |
| total | Total transaction amount including tax |
| cogs | Cost of goods sold value from the source |
| gross_income | Gross income value from the source |
| rating | Customer rating for the transaction |