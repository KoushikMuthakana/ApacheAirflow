from airflow import DAG


with DAG(dag_id="logs_dag_1",schedule_interval="@daily") as dag:
    pass