from datetime import timedelta 
from airflow import DAG
from airflow.operators.python_operator import PythonOperator 
from airflow.utils.dates import days_ago
from datetime import datetime
from src.get_bist_live_csv import get_bist_live

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    "dag2",
    schedule_interval="0 7-15 * * *",
    default_args=default_args,
    description="Get bist live",
    start_date = datetime (2024, 3, 25),
    end_date = datetime(2024, 4, 5)  
)

run_etl = PythonOperator(
    task_id="getting_bist_live",
    python_callable=get_bist_live,
    dag=dag
)

run_etl