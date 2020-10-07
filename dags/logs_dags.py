from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from logsparsing import fetch_logs
from logsparsing import preprocess_logs


default_args ={
"start_date": datetime(2020,1,1),
"owner":"airflow"

}

with DAG(dag_id="log_dag",schedule_interval="@daily",default_args= default_args) as dag:
    waiting_to_logs = FileSensor(task_id="waiting_for_dag_logs",fs_conn_id= "fs_logs", filepath="logs_dags.py.log",poke_interval=5)
    fetching_logs = PythonOperator(task_id="fetching_logs", python_callable=fetch_logs.main)
    error_logs = PythonOperator(task_id="preprocess_logs",python_callable=preprocess_logs.main)
