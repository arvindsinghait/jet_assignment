select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "jet_assignment"."jet_assignment_test"."not_null_fact_comic_detail_source_system"
    
      
    ) dbt_internal_test