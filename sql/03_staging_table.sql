DROP TABLE IF EXISTS staging.supermarket_sales_clean;

CREATE TABLE staging.supermarket_sales_clean (
    invoice_id TEXT PRIMARY KEY,
    branch VARCHAR(1) NOT NULL,
    city VARCHAR(50) NOT NULL,
    customer_type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    product_line VARCHAR(50) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    tax_5_percent NUMERIC(12, 4) NOT NULL,
    total NUMERIC(12, 4) NOT NULL,
    sale_date DATE NOT NULL,
    sale_time TIME NOT NULL,
    payment VARCHAR(20) NOT NULL,
    cogs NUMERIC(12, 2) NOT NULL,
    gross_margin_percentage NUMERIC(12, 9) NOT NULL,
    gross_income NUMERIC(12, 4) NOT NULL,
    rating NUMERIC(3, 1) NOT NULL,
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);