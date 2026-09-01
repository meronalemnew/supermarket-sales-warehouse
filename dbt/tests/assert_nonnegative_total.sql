SELECT *
FROM {{ ref('fact_sales') }}
WHERE total < 0