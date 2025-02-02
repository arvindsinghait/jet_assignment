


SELECT
    source_system,
    comic_unique_num,
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
    (RANDOM() * 10000)::int AS views,
    LENGTH(REPLACE(comic_safe_title, ' ', '')) * 5 AS cost,
    ROUND((RANDOM() * 9 + 1)::NUMERIC, 2) AS customer_reviews,
    CURRENT_TIMESTAMP AS _created_at
FROM "jet_assignment"."jet_assignment_silver"."silver_comics_details"