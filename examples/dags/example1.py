from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator


with DAG(
        dag_id="An_example_1",
        tags=["testing"],
        start_date=days_ago(1),
        schedule_interval="@daily",
        catchup=False
) as dag:
    task1 = PythonOperator(
        task_id="Task1",
        python_callable=lambda: print("Task 1")
    )
    task2 = PythonOperator(
        task_id="Task2",
        python_callable=lambda: print("Task 2")
    )

    task1 >> task2
