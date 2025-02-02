import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# 🔍 Get the DAGs folder dynamically
DAGS_FOLDER = os.path.dirname(os.path.abspath(__file__))  # Path to `dags/` folder

# Define the DBT project and virtual environment relative to the DAGs folder
PROJECT_ROOT = os.path.dirname(DAGS_FOLDER)  # Get the parent folder (i.e., `jet_assignment/`)
DBT_PROJECT_DIR = os.path.join(PROJECT_ROOT, "dbt")  # Path to `jet_assignment/dbt/`
DBT_VENV_DIR = os.path.join(PROJECT_ROOT, "dbt-venv")  # Path to `jet_assignment/dbt-venv/`

# Default Arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'dwh_comic_data',
    default_args=default_args,
    description='Run DBT models and tests in Airflow',
    schedule_interval=None,
    start_date=datetime(2025, 1, 30),
)

# Start task
start_task = DummyOperator(
    task_id='start_task',
    dag=dag,
)

# Task to run dbt models and Test together
dbt_build_task = BashOperator(
    task_id='dbt_build',
    bash_command=(
        f'export DBT_PROFILES_DIR="{PROJECT_ROOT}" && '  # Set the DBT profiles path
        f'source {DBT_VENV_DIR}/bin/activate && '  # Activate the virtual environment
        f'cd {DBT_PROJECT_DIR} && '  # Change directory to DBT project
        'dbt build'  # Run DBT models
    ),
    dag=dag,
)

# End task
end_task = DummyOperator(
    task_id='end_task',
    dag=dag,
)

# Task dependencies
start_task >> dbt_build_task  >> end_task
