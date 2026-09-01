WITH totals AS (

    SELECT
        (SELECT SUM(total)
         FROM {{ ref('stg_supermarket_sales') }}) AS staging_revenue,

        (SELECT SUM(total)
         FROM {{ ref('fact_sales') }}) AS fact_revenue

)

SELECT *
FROM totals
WHERE staging_revenue IS DISTINCT FROM fact_revenue