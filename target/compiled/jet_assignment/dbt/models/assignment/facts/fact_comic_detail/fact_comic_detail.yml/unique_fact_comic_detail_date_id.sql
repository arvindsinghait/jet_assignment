
    
    

select
    date_id as unique_field,
    count(*) as n_records

from "jet_assignment"."jet_assignment_gold"."fact_comic_detail"
where date_id is not null
group by date_id
having count(*) > 1


