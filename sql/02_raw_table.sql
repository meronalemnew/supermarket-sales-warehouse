DROP TABLE IF EXISTS raw.supermarket_sales;

CREATE TABLE raw.supermarket_sales (
    invoice_id TEXT,
    branch TEXT,
    city TEXT,
    customer_type TEXT,
    gender TEXT,
    product_line TEXT,
    unit_price TEXT,
    quantity TEXT,
    tax_5_percent TEXT,
    total TEXT,
    sale_date TEXT,
    sale_time TEXT,
    payment TEXT,
    cogs TEXT,
    gross_margin_percentage TEXT,
    gross_income TEXT,
    rating TEXT
);