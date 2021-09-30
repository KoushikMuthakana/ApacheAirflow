from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

# Using Context Manager, Grouping all the tags
with DAG(dag_id='BASH_OPERATOR_SEQUENCE_EXAMPLE',
         description="This DAG shows the simple bash sequence tasks",
         schedule_interval="@daily",
         start_date=days_ago(1),
         catchup=False)as dag:
    task1 = BashOperator(
        task_id="task1",
        bash_command="echo task 1",

    )
    task2 = BashOperator(
        task_id="task2",
        bash_command="echo task 2"
    )
    task3 = BashOperator(
        task_id="task3",
        bash_command="echo task 3",
        trigger_rule="one_failed"
    )
    task4 = BashOperator(
        task_id="task4",
        bash_command="echo task 4"
    )

    # Dependencies between the tasks
    task2 >> [task1,task3, task4]
