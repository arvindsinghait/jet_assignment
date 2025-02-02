
  
    

  create  table "jet_assignment"."jet_assignment_silver"."silver_comics_details__dbt_tmp"
  
  
    as
  
  (
    

WITH source_data AS (
    SELECT *, 'xkcd' AS source_system
    FROM "jet_assignment"."jet_assignment_bronze"."xkcd_comics_details"
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
  );
  