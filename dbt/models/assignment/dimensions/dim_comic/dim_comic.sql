{{
    config(
        materialized='table',
        alias = 'dim_comic'
    )
}}


SELECT
 {{ dbt_utils.surrogate_key([
        'source_comic_id',
        'source_system'
      ])
    }}                 AS comic_id,
    source_comic_id,
    source_system,
    link,
    news,
    comic_safe_title,
    transcript,
    alt,
    img_url,
    comic_title,
    CURRENT_TIMESTAMP AS _created_at
FROM {{ref('staging_comic_detail')}}
