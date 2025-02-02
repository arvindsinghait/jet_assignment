{{
    config(
        materialized='table',
        alias = 'silver_comic_detail'
    )
}}

WITH source_data AS (
    SELECT *, 'xkcd' AS source_system
    FROM {{ source('bronze_layer', 'xkcd_comic_detail') }}
)

SELECT
    source_system,
    num AS comic_unique_num,
    day AS day,
    month AS month,
    year AS year,
    link AS link,
    news AS news,
    safe_title AS comic_safe_title,
    transcript AS transcript,
    alt AS alt,
    img AS img_url,
    title AS comic_title,
    CURRENT_TIMESTAMP AS _created_at
FROM source_data
