{{ config(
    materialized='incremental',
    unique_key='invoice_id'
) }}

with sales as (

    select *
    from {{ ref('stg_supermarket_sales') }}

    {% if is_incremental() %}

    where invoice_id not in (
        select invoice_id
        from {{ this }}
    )

    {% endif %}

),

final as (

    select
        sales.invoice_id,
        branch.branch_key,
        product_line.product_line_key,
        customer_segment.customer_segment_key,
        payment.payment_key,
        date_dimension.date_key,
        time_dimension.time_key,
        sales.unit_price,
        sales.quantity,
        sales.tax_5_percent,
        sales.total,
        sales.cogs,
        sales.gross_margin_percentage,
        sales.gross_income,
        sales.rating

    from sales

    inner join {{ ref('dim_branch') }} as branch
        on sales.branch = branch.branch
        and sales.city = branch.city

    inner join {{ ref('dim_product_line') }} as product_line
        on sales.product_line = product_line.product_line

    inner join {{ ref('dim_customer_segment') }} as customer_segment
        on sales.customer_type = customer_segment.customer_type
        and sales.gender = customer_segment.gender

    inner join {{ ref('dim_payment') }} as payment
        on sales.payment = payment.payment

    inner join {{ ref('dim_date') }} as date_dimension
        on sales.sale_date = date_dimension.sale_date

    inner join {{ ref('dim_time') }} as time_dimension
        on sales.sale_time = time_dimension.sale_time

)

select *
from final