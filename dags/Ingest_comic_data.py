import os
import time
import requests
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Set no_proxy to avoid networking issues in Airflow
os.environ["no_proxy"] = "*"

# Path to the DAGs and project directories
DAGS_DIR = os.path.abspath(os.path.dirname(__file__))  # Path to `dags/`
PROJECT_DIR = os.path.dirname(DAGS_DIR)  # `jet_assignment/`
SCRIPT_PATH = os.path.join(PROJECT_DIR, "scripts/fetch_comic_data.py")

# Function to check if new comic data is available
def check_for_new_comic():
    url = "https://xkcd.com/info.0.json"  # URL to check for latest comic
    try:
        response = requests.get(url, timeout=10)  # Add timeout to avoid hanging
        response.raise_for_status()  # Raise an error for bad status codes
        comic_data = response.json()
        print(f"Latest Comic ID: {comic_data['num']}")
        return comic_data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the latest comic data: {e}")
        return None

# Polling function
def poll_for_new_comic(**kwargs):
    max_retries = 5  # Maximum attempts to check for new data
    delay = 600  # Delay in seconds (10 minutes)

    for attempt in range(max_retries):
        comic_data = check_for_new_comic()
        if comic_data:
            # If we got the comic data, exit the loop and proceed with the DAG
            print(f"New comic found: {comic_data['num']}")
            return comic_data
        else:
            print(f"Attempt {attempt + 1}: No new comic, retrying...")
            time.sleep(delay)  # Wait for 10 minutes before retrying

    print("Max retries reached, no new comic data found.")
    return None

# Default Arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
}

# DAG Definition
dag = DAG(
    'ingest_comic_data',
    default_args=default_args,
    description='Fetch XKCD comic data with polling',
    schedule_interval="0 10 * * 1,3,5",  # Run on Monday, Wednesday, and Friday at 10:00 AM
    start_date=datetime(2025, 1, 30),
    catchup=False,  
)

# Tasks
start_task = DummyOperator(task_id='start_task', dag=dag)

# Polling task using PythonOperator
poll_comic_task = PythonOperator(
    task_id='poll_comic_data',
    python_callable=poll_for_new_comic,  
    provide_context=True, 
    dag=dag,
)

# Task to fetch comic data
fetch_comic_data_task = BashOperator(
    task_id='ingest_comic_data',
    bash_command=f'python {SCRIPT_PATH}',  # Fetch comic data if new comic is found
    dag=dag,
)

end_task = DummyOperator(task_id='end_task', dag=dag)

# DAG Execution Order
start_task >> poll_comic_task >> fetch_comic_data_task >> end_task