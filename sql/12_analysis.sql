-- =========================================================
-- Supermarket Sales Warehouse
-- Portfolio Analysis Queries
-- =========================================================


-- Revenue by branch
SELECT
    b.branch,
    b.city,
    SUM(f.total) AS total_revenue
FROM dbt_dev.fact_sales f
JOIN dbt_dev.dim_branch b
    ON f.branch_key = b.branch_key
GROUP BY
    b.branch,
    b.city
ORDER BY total_revenue DESC;


-- Revenue by product line
SELECT
    p.product_line,
    SUM(f.total) AS total_revenue
FROM dbt_dev.fact_sales f
JOIN dbt_dev.dim_product_line p
    ON f.product_line_key = p.product_line_key
GROUP BY
    p.product_line
ORDER BY total_revenue DESC;


-- Customer segment performance
SELECT
    c.customer_type,
    c.gender,
    COUNT(*) AS transaction_count,
    SUM(f.total) AS total_revenue,
    ROUND(AVG(f.total), 2) AS avg_transaction_value
FROM dbt_dev.fact_sales f
JOIN dbt_dev.dim_customer_segment c
    ON f.customer_segment_key = c.customer_segment_key
GROUP BY
    c.customer_type,
    c.gender
ORDER BY total_revenue DESC;


-- Sales by time of day
SELECT
    t.time_of_day,
    COUNT(*) AS transaction_count,
    SUM(f.total) AS total_revenue,
    ROUND(AVG(f.total), 2) AS avg_transaction_value
FROM dbt_dev.fact_sales f
JOIN dbt_dev.dim_time t
    ON f.time_key = t.time_key
GROUP BY
    t.time_of_day
ORDER BY total_revenue DESC;


-- Monthly sales
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(*) AS transaction_count,
    SUM(f.total) AS total_revenue
FROM dbt_dev.fact_sales f
JOIN dbt_dev.dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- Payment method performance
SELECT
    p.payment,
    COUNT(*) AS transaction_count,
    SUM(f.total) AS total_revenue,
    ROUND(AVG(f.total), 2) AS avg_transaction_value
FROM dbt_dev.fact_sales f
JOIN dbt_dev.dim_payment p
    ON f.payment_key = p.payment_key
GROUP BY
    p.payment
ORDER BY total_revenue DESC;