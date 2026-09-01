with unique_branches as (

    select distinct
        branch,
        city
    from {{ ref('stg_supermarket_sales') }}

),

final as (

    select
        row_number() over (order by branch)::integer as branch_key,
        branch,
        city
    from unique_branches

)

select *
from final