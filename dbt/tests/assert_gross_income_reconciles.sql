WITH totals AS (

    SELECT
        (SELECT SUM(gross_income)
         FROM {{ ref('stg_supermarket_sales') }}) AS staging_gross_income,

        (SELECT SUM(gross_income)
         FROM {{ ref('fact_sales') }}) AS fact_gross_income

)

SELECT *
FROM totals
WHERE staging_gross_income IS DISTINCT FROM fact_gross_income