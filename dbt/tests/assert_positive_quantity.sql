SELECT *
FROM {{ ref('fact_sales') }}
WHERE quantity <= 0