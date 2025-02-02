
    
    

select
    comic_unique_num as unique_field,
    count(*) as n_records

from "jet_assignment"."jet_assignment_gold"."fact_comic_detail"
where comic_unique_num is not null
group by comic_unique_num
having count(*) > 1


