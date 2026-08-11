-- Branch dimension
INSERT INTO warehouse.dim_branch (
    branch_code,
    city
)
SELECT DISTINCT
    branch,
    city
FROM staging.supermarket_sales_clean
ON CONFLICT (branch_code, city) DO NOTHING;


-- Product line dimension
INSERT INTO warehouse.dim_product_line (
    product_line
)
SELECT DISTINCT
    product_line
FROM staging.supermarket_sales_clean
ON CONFLICT (product_line) DO NOTHING;


-- Customer segment dimension
INSERT INTO warehouse.dim_customer_segment (
    customer_type,
    gender
)
SELECT DISTINCT
    customer_type,
    gender
FROM staging.supermarket_sales_clean
ON CONFLICT (customer_type, gender) DO NOTHING;


-- Payment dimension
INSERT INTO warehouse.dim_payment (
    payment_method
)
SELECT DISTINCT
    payment
FROM staging.supermarket_sales_clean
ON CONFLICT (payment_method) DO NOTHING;


-- Date dimension
INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_of_week
)
SELECT DISTINCT
    TO_CHAR(sale_date, 'YYYYMMDD')::INTEGER,
    sale_date,
    EXTRACT(DAY FROM sale_date)::INTEGER,
    EXTRACT(MONTH FROM sale_date)::INTEGER,
    TO_CHAR(sale_date, 'FMMonth'),
    EXTRACT(QUARTER FROM sale_date)::INTEGER,
    EXTRACT(YEAR FROM sale_date)::INTEGER,
    TO_CHAR(sale_date, 'FMDay')
FROM staging.supermarket_sales_clean
ON CONFLICT (date_key) DO NOTHING;


-- Time dimension
INSERT INTO warehouse.dim_time (
    time_key,
    full_time,
    hour,
    minute,
    time_of_day
)
SELECT DISTINCT
    TO_CHAR(sale_time, 'HH24MI')::INTEGER,
    sale_time,
    EXTRACT(HOUR FROM sale_time)::INTEGER,
    EXTRACT(MINUTE FROM sale_time)::INTEGER,
    CASE
        WHEN EXTRACT(HOUR FROM sale_time) < 12 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM sale_time) < 17 THEN 'Afternoon'
        ELSE 'Evening'
    END
FROM staging.supermarket_sales_clean
ON CONFLICT (time_key) DO NOTHING;