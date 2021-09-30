from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


def get_name():
    return Variable.get("myname")


with DAG(dag_id="variables", start_date=days_ago(1),
         schedule_interval="@daily",
         catchup=False,
         tags=['variables']) as dag:
    read_variable_task = PythonOperator(
        task_id="variable_task",
        python_callable=get_name
    )

    print_name_task= BashOperator(
        task_id="print_name",
        bash_command= Variable.get("mycommand")
    )

    read_variable_task >> print_name_task
