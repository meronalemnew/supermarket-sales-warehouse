SELECT *
FROM {{ ref('fact_sales') }}
WHERE rating < 0
   OR rating > 10