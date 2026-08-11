# Star Schema

The warehouse uses `fact_sales` as the central fact table. It connects to six dimension tables.

```mermaid
flowchart LR
    branch[dim_branch] --> fact[fact_sales]
    product[dim_product_line] --> fact
    customer[dim_customer_segment] --> fact
    payment[dim_payment] --> fact
    date[dim_date] --> fact
    time[dim_time] --> fact

    ## Documentation

- [Data dictionary](docs/data_dictionary.md)
- [Star schema](docs/star_schema.md)