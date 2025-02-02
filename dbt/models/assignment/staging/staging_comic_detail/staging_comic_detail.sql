{{
    config(
        materialized='table',
        alias = 'staging_comic_detail'
    )
}}


SELECT
    source_system,
    comic_unique_num AS source_comic_id,
    day,
    month,
    year,
    link,
    news,
    comic_safe_title,
    transcript,
    alt,
    img_url,
    comic_title,    
    (RANDOM() * 10000)::int AS total_customer_views,
    LENGTH(REPLACE(comic_safe_title, ' ', '')) * 5 AS comic_creation_cost,
    ROUND((RANDOM() * 9 + 1)::NUMERIC, 2) AS avg_customer_reviews,
    CURRENT_TIMESTAMP AS _created_at
FROM {{ref('silver_comic_detail')}}
