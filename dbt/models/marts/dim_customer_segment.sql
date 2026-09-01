with unique_customer_segments as (

    select distinct
        customer_type,
        gender
    from {{ ref('stg_supermarket_sales') }}

),

final as (

    select
        row_number() over (
            order by customer_type, gender
        )::integer as customer_segment_key,
        customer_type,
        gender
    from unique_customer_segments

)

select *
from final