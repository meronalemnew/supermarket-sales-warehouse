CREATE OR REPLACE VIEW warehouse.vw_sales_detail AS
SELECT
    f.invoice_id,
    b.branch_code,
    b.city,
    p.product_line,
    c.customer_type,
    c.gender,
    pm.payment_method,
    d.full_date AS sale_date,
    d.year,
    d.month,
    d.month_name,
    d.day_of_week,
    t.full_time AS sale_time,
    t.time_of_day,
    f.unit_price,
    f.quantity,
    f.tax_5_percent,
    f.total,
    f.cogs,
    f.gross_income,
    f.rating
FROM warehouse.fact_sales f
JOIN warehouse.dim_branch b
    ON f.branch_key = b.branch_key
JOIN warehouse.dim_product_line p
    ON f.product_line_key = p.product_line_key
JOIN warehouse.dim_customer_segment c
    ON f.customer_segment_key = c.customer_segment_key
JOIN warehouse.dim_payment pm
    ON f.payment_key = pm.payment_key
JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
JOIN warehouse.dim_time t
    ON f.time_key = t.time_key;


CREATE OR REPLACE VIEW warehouse.vw_branch_performance AS
SELECT
    b.branch_code,
    b.city,
    COUNT(*) AS transaction_count,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.total) AS total_revenue,
    SUM(f.gross_income) AS total_gross_income,
    ROUND(AVG(f.total), 2) AS avg_transaction_value,
    ROUND(AVG(f.rating), 2) AS avg_rating
FROM warehouse.fact_sales f
JOIN warehouse.dim_branch b
    ON f.branch_key = b.branch_key
GROUP BY
    b.branch_code,
    b.city;


CREATE OR REPLACE VIEW warehouse.vw_monthly_performance AS
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(*) AS transaction_count,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.total) AS total_revenue,
    SUM(f.gross_income) AS total_gross_income,
    ROUND(AVG(f.total), 2) AS avg_transaction_value
FROM warehouse.fact_sales f
JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name;