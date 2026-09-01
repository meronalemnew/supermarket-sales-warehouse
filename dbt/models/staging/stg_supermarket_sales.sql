with source_data as (

    select *
    from {{ source('raw', 'supermarket_sales') }}

),

cleaned_data as (

    select
        trim(invoice_id) as invoice_id,
        trim(branch) as branch,
        trim(city) as city,
        trim(customer_type) as customer_type,
        trim(gender) as gender,
        trim(product_line) as product_line,
        cast(unit_price as numeric(10, 2)) as unit_price,
        cast(quantity as integer) as quantity,
        cast(tax_5_percent as numeric(12, 4)) as tax_5_percent,
        cast(total as numeric(12, 4)) as total,
        to_date(sale_date, 'MM/DD/YYYY') as sale_date,
        cast(sale_time as time) as sale_time,
        trim(payment) as payment,
        cast(cogs as numeric(12, 4)) as cogs,
        cast(gross_margin_percentage as numeric(12, 9))
            as gross_margin_percentage,
        cast(gross_income as numeric(12, 4)) as gross_income,
        cast(rating as numeric(3, 1)) as rating
    from source_data

)

select *
from cleaned_data