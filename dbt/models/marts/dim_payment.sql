with unique_payment_methods as (

    select distinct
        payment
    from {{ ref('stg_supermarket_sales') }}

),

final as (

    select
        row_number() over (order by payment)::integer as payment_key,
        payment
    from unique_payment_methods

)

select *
from final