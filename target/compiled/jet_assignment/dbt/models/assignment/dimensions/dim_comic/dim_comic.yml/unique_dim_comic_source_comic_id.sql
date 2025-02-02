
    
    

select
    source_comic_id as unique_field,
    count(*) as n_records

from "jet_assignment"."jet_assignment_gold"."dim_comic"
where source_comic_id is not null
group by source_comic_id
having count(*) > 1


