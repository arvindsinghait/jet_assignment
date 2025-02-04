# jet_assignment
Data &amp; Analytics Case Study

# Scripts : 
In scripts folder we have scripts for extracting and loading data from web to postgres sql 

# DBT : 
In dbt folder we have dbt transformation scripts. We have defined different layers. Example Bronze layer, Silver Layer and Gold Layer. In Gold layer, we have created our dimension and facts

# Dag : 
We have created two DAGs : 
1. DAG Name : Ingest_comic_data: This is for extracting and loading data using API on scheduled time with polling logic applied i.e Mondays, Wednesdays, 
and Fridays
2. DAG Name : dwh_comic_data : This is to run DBT transformation on demand

# Steps for replicating it : 
1. Clone the repo in local
2. Install DBT, PostgreSQL and Airflow separately
3. Export env varilable DBT_POSTGRES_PASSWORD based on password you have set while installing postgreSQL

# DBT Airflow screenshot : 
<img width="1483" alt="image" src="https://github.com/user-attachments/assets/18d0ae91-ecc9-4b8b-a1db-6a111ba4fdf3" />

# Ingest Airflow screenshot : 
<img width="1506" alt="image" src="https://github.com/user-attachments/assets/50c5daef-c0f7-4221-b259-2f46a3f9f592" />

# DBT Docs - Data Flow : 
<img width="1132" alt="image" src="https://github.com/user-attachments/assets/08942bc3-2636-469b-87ae-9f93de600166" />
