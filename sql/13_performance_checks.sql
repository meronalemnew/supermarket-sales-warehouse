-- Update PostgreSQL statistics
ANALYZE warehouse.fact_sales;
ANALYZE warehouse.dim_branch;


-- Review branch revenue query plan
EXPLAIN ANALYZE
SELECT
    b.branch_code,
    b.city,
    SUM(f.total) AS total_revenue
FROM warehouse.fact_sales f
JOIN warehouse.dim_branch b
    ON f.branch_key = b.branch_key
GROUP BY
    b.branch_code,
    b.city
ORDER BY total_revenue DESC;


-- Review indexed branch filter
EXPLAIN ANALYZE
SELECT
    invoice_id,
    total,
    quantity
FROM warehouse.fact_sales
WHERE branch_key = 3;