INSERT INTO staging.supermarket_sales_clean (
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
SELECT
    BTRIM(r.invoice_id),
    BTRIM(r.branch),
    BTRIM(r.city),
    BTRIM(r.customer_type),
    BTRIM(r.gender),
    BTRIM(r.product_line),
    r.unit_price::NUMERIC(10, 2),
    r.quantity::INTEGER,
    r.tax_5_percent::NUMERIC(12, 4),
    r.total::NUMERIC(12, 4),
    TO_DATE(r.sale_date, 'MM/DD/YYYY'),
    r.sale_time::TIME,
    BTRIM(r.payment),
    r.cogs::NUMERIC(12, 2),
    r.gross_margin_percentage::NUMERIC(12, 9),
    r.gross_income::NUMERIC(12, 4),
    r.rating::NUMERIC(3, 1)
FROM raw.supermarket_sales r
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.supermarket_sales_clean s
    WHERE s.invoice_id = BTRIM(r.invoice_id)
);