{{
    config(
        materialized='table',
        alias = 'dim_date'
    )
}}


SELECT 
   {{ dbt_utils.surrogate_key([
        'd::DATE'
      ])
    }}                 AS date_id,
    d::DATE AS full_date,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(QUARTER FROM d) AS quarter,
    CASE 
        WHEN EXTRACT(MONTH FROM d) BETWEEN 1 AND 6 THEN 1 
        ELSE 2 
    END AS semester,
    EXTRACT(MONTH FROM d) AS month,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(DAY FROM d) AS day,
    EXTRACT(ISODOW FROM d) AS day_of_week,
    TO_CHAR(d, 'Day') AS day_name,
    EXTRACT(WEEK FROM d) AS week_number,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6,7) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series(
    '2000-01-01'::DATE, 
    '2024-12-31'::DATE,  
    '1 day'::INTERVAL 
) d