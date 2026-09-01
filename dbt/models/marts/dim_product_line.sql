with unique_product_lines as (

    select distinct
        product_line
    from {{ ref('stg_supermarket_sales') }}

),

final as (

    select
        row_number() over (order by product_line)::integer
            as product_line_key,
        product_line
    from unique_product_lines

)

select *
from final