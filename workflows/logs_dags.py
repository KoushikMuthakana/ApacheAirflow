from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import datetime
default_args ={
"start_date": datetime(2020,1,1),
"owner":"airflow"

}

with DAG(dag_id="log_dags_1",schedule_interval="@daily",default_args= default_args) as dag:
    waiting_to_logs = FileSensor(task_id="waiting_for_dag_logs",fs_conn_id= "fs_logs",filepath="dag_processor_manager.log",poke_interval=5)