from datetime import timedelta 
from airflow import DAG
from airflow.operators.python_operator import PythonOperator 
from airflow.utils.dates import days_ago
from datetime import datetime
import main

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
    "dag1",
    schedule_interval="0 18 * * *",
    default_args=default_args,
    description="Get comments and KAP notifications",
    start_date = datetime (2024, 3, 25),
    end_date = datetime(2024, 4, 5)  
)

run_etl = PythonOperator(
    task_id="getting_comments_and_kap",
    python_callable=main,
    dag=dag
)

run_etl