with unique_dates as (

    select distinct
        sale_date
    from {{ ref('stg_supermarket_sales') }}

),

final as (

    select
        to_char(sale_date, 'YYYYMMDD')::integer as date_key,
        sale_date,
        extract(year from sale_date)::integer as year,
        extract(quarter from sale_date)::integer as quarter,
        extract(month from sale_date)::integer as month,
        trim(to_char(sale_date, 'Month')) as month_name,
        extract(day from sale_date)::integer as day,
        trim(to_char(sale_date, 'Day')) as day_name
    from unique_dates

)

select *
from final