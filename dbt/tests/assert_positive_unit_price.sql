SELECT *
FROM {{ ref('fact_sales') }}
WHERE unit_price <= 0