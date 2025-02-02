
  
    

  create  table "jet_assignment"."jet_assignment_gold"."dim_comic__dbt_tmp"
  
  
    as
  
  (
    


SELECT
 md5(cast(coalesce(cast(source_comic_id as 
    varchar
), '') || '-' || coalesce(cast(source_system as 
    varchar
), '') as 
    varchar
))                 AS comic_id,
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
FROM "jet_assignment"."jet_assignment_silver"."staging_comic_detail"
  );
  