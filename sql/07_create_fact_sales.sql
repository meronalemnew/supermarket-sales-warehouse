DROP TABLE IF EXISTS warehouse.fact_sales;

CREATE TABLE warehouse.fact_sales (
    sales_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    invoice_id TEXT NOT NULL UNIQUE,

    branch_key INTEGER NOT NULL,
    product_line_key INTEGER NOT NULL,
    customer_segment_key INTEGER NOT NULL,
    payment_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    time_key INTEGER NOT NULL,

    unit_price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    tax_5_percent NUMERIC(12, 4) NOT NULL,
    total NUMERIC(12, 4) NOT NULL,
    cogs NUMERIC(12, 2) NOT NULL,
    gross_income NUMERIC(12, 4) NOT NULL,
    rating NUMERIC(3, 1) NOT NULL,

    FOREIGN KEY (branch_key)
        REFERENCES warehouse.dim_branch(branch_key),

    FOREIGN KEY (product_line_key)
        REFERENCES warehouse.dim_product_line(product_line_key),

    FOREIGN KEY (customer_segment_key)
        REFERENCES warehouse.dim_customer_segment(customer_segment_key),

    FOREIGN KEY (payment_key)
        REFERENCES warehouse.dim_payment(payment_key),

    FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),

    FOREIGN KEY (time_key)
        REFERENCES warehouse.dim_time(time_key)
);