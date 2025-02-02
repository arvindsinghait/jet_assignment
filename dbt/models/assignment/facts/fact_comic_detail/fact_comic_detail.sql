{{
    config(
        materialized='table',
        alias = 'fact_comic_detail'
    )
}}

SELECT
    dc.comic_id,
    dd.date_id,
    source.source_system,
    source.day,
    source.month,
    source.year, 
    source.total_customer_views,
    source.comic_creation_cost,
    source.avg_customer_reviews,
    CURRENT_TIMESTAMP AS _created_at
FROM {{ref('staging_comic_detail')}} source
LEFT JOIN  {{ref('dim_comic')}} dc
ON source.source_comic_id=dc.source_comic_id
AND source.source_system=dc.source_system
LEFT JOIN  {{ref('dim_date')}} dd
ON  source.day = dd.day
AND source.month = dd.month
AND source.year = dd.year