select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "jet_assignment"."jet_assignment_test"."unique_dim_comic_source_comic_id"
    
      
    ) dbt_internal_test