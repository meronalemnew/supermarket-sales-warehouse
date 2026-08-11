CREATE INDEX IF NOT EXISTS idx_fact_sales_branch_key
ON warehouse.fact_sales(branch_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product_line_key
ON warehouse.fact_sales(product_line_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_segment_key
ON warehouse.fact_sales(customer_segment_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_payment_key
ON warehouse.fact_sales(payment_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date_key
ON warehouse.fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_time_key
ON warehouse.fact_sales(time_key);

ANALYZE warehouse.fact_sales;