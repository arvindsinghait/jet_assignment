
    
    

select
    fact_comic_detail_id as unique_field,
    count(*) as n_records

from "jet_assignment"."jet_assignment_gold"."fact_comic_detail"
where fact_comic_detail_id is not null
group by fact_comic_detail_id
having count(*) > 1


