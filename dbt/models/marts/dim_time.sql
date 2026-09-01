with unique_times as (

    select distinct
        sale_time
    from {{ ref('stg_supermarket_sales') }}

),

final as (

    select
        (
            extract(hour from sale_time)::integer * 100
            + extract(minute from sale_time)::integer
        ) as time_key,
        sale_time,
        extract(hour from sale_time)::integer as hour,
        extract(minute from sale_time)::integer as minute,
        case
            when extract(hour from sale_time) < 12 then 'Morning'
            when extract(hour from sale_time) < 17 then 'Afternoon'
            else 'Evening'
        end as time_of_day
    from unique_times

)

select *
from final