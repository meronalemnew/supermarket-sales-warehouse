{% snapshot dim_branch_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='branch',
        strategy='check',
        check_cols=['city']
    )
}}

select
    branch,
    city
from {{ ref('dim_branch') }}

{% endsnapshot %}