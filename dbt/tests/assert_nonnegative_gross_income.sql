SELECT *
FROM {{ ref('fact_sales') }}
WHERE gross_income < 0