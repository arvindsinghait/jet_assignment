
  
    

  create  table "jet_assignment"."jet_assignment_bronze"."test_model__dbt_tmp"
  
  
    as
  
  (
    

WITH source_data AS (
    SELECT * 
    FROM "jet_assignment"."jet_assignment_bronze"."xkcd_comics_details"
)

SELECT * 
FROM source_data
  );
  