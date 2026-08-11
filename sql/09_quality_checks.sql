-- Row-count reconciliation
SELECT
    (SELECT COUNT(*)
     FROM staging.supermarket_sales_clean) AS staging_rows,

    (SELECT COUNT(*)
     FROM warehouse.fact_sales) AS fact_rows;


-- Revenue reconciliation
SELECT
    (SELECT SUM(total)
     FROM staging.supermarket_sales_clean) AS staging_revenue,

    (SELECT SUM(total)
     FROM warehouse.fact_sales) AS warehouse_revenue;


-- Quantity reconciliation
SELECT
    (SELECT SUM(quantity)
     FROM staging.supermarket_sales_clean) AS staging_quantity,

    (SELECT SUM(quantity)
     FROM warehouse.fact_sales) AS warehouse_quantity;


-- Gross income reconciliation
SELECT
    (SELECT SUM(gross_income)
     FROM staging.supermarket_sales_clean) AS staging_gross_income,

    (SELECT SUM(gross_income)
     FROM warehouse.fact_sales) AS warehouse_gross_income;


-- Foreign-key completeness
SELECT
    COUNT(*) FILTER (WHERE branch_key IS NULL) AS missing_branch_keys,
    COUNT(*) FILTER (WHERE product_line_key IS NULL) AS missing_product_line_keys,
    COUNT(*) FILTER (WHERE customer_segment_key IS NULL) AS missing_customer_segment_keys,
    COUNT(*) FILTER (WHERE payment_key IS NULL) AS missing_payment_keys,
    COUNT(*) FILTER (WHERE date_key IS NULL) AS missing_date_keys,
    COUNT(*) FILTER (WHERE time_key IS NULL) AS missing_time_keys
FROM warehouse.fact_sales;