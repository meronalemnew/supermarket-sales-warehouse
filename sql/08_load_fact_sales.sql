INSERT INTO warehouse.fact_sales (
    invoice_id,
    branch_key,
    product_line_key,
    customer_segment_key,
    payment_key,
    date_key,
    time_key,
    unit_price,
    quantity,
    tax_5_percent,
    total,
    cogs,
    gross_income,
    rating
)
SELECT
    s.invoice_id,
    b.branch_key,
    p.product_line_key,
    c.customer_segment_key,
    pm.payment_key,
    d.date_key,
    t.time_key,
    s.unit_price,
    s.quantity,
    s.tax_5_percent,
    s.total,
    s.cogs,
    s.gross_income,
    s.rating
FROM staging.supermarket_sales_clean s

JOIN warehouse.dim_branch b
    ON s.branch = b.branch_code
   AND s.city = b.city

JOIN warehouse.dim_product_line p
    ON s.product_line = p.product_line

JOIN warehouse.dim_customer_segment c
    ON s.customer_type = c.customer_type
   AND s.gender = c.gender

JOIN warehouse.dim_payment pm
    ON s.payment = pm.payment_method

JOIN warehouse.dim_date d
    ON s.sale_date = d.full_date

JOIN warehouse.dim_time t
    ON s.sale_time = t.full_time

ON CONFLICT (invoice_id) DO NOTHING;