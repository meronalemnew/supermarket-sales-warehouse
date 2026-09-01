WITH totals AS (

    SELECT
        (SELECT SUM(quantity)
         FROM {{ ref('stg_supermarket_sales') }}) AS staging_quantity,

        (SELECT SUM(quantity)
         FROM {{ ref('fact_sales') }}) AS fact_quantity

)

SELECT *
FROM totals
WHERE staging_quantity IS DISTINCT FROM fact_quantity