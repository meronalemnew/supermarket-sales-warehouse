WITH counts AS (

    SELECT
        (SELECT COUNT(*)
         FROM {{ source('raw', 'supermarket_sales') }}) AS raw_rows,

        (SELECT COUNT(*)
         FROM {{ ref('stg_supermarket_sales') }}) AS staging_rows,

        (SELECT COUNT(*)
         FROM {{ ref('fact_sales') }}) AS fact_rows

)

SELECT *
FROM counts
WHERE raw_rows <> staging_rows
   OR staging_rows <> fact_rows