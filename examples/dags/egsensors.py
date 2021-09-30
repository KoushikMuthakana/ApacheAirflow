from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.bash import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago

with DAG(dag_id="SensorExample", start_date=days_ago(1), schedule_interval="@daily", catchup=False) as dag:
    sensor = HttpSensor(
        task_id="httpsensor",
        endpoint="/",
        http_conn_id="http_conn",
        retries=5,
        retry_delay=timedelta(seconds=3)
    )
    task1 = BashOperator(
        task_id="task1",
        bash_command="echo hello task1"
    )
    task2 = BashOperator(
        task_id="task2",
        bash_command="echo hello task2"
    )

    sensor >> [task1, task2]
