select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "jet_assignment"."jet_assignment_test"."unique_silver_comic_detail_comic_unique_num"
    
      
    ) dbt_internal_test