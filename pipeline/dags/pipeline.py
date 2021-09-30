from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow import settings
from airflow.models import Connection


def get_aws_s3_url():
    session = settings.Session()
    connection = session.query(Connection).filter(Connection.conn_id == 'orders_s3').first()
    return f"{connection.schema}://{connection.host}/orders.csv"


def slack_password():
    session = settings.Session()
    connection = session.query(Connection).filter(Connection.conn_id == 'slack').first()
    pwd= connection.password
    return "T02GKQ42DC1/B02FSEPP4P9"


def get_orders_filter_cmd():
    cmd1 = "hadoop fs -rm -R -f  airflow_output"
    cmd2 = "spark-submit orders.py"
    return cmd1 + "&&" + cmd2


download_order_command = "rm -rf airflow_pipeline && mkdir -p airflow_pipeline && cd airflow_pipeline && wget " \
                         + get_aws_s3_url()


def load_customer_info_cmd():
    cmd1 = "hive -e 'DROP TABLE airflow.customers'"
    cmd2 = "sqoop import --connect jdbc:mysql://localhost:3306/retail_db --username root --password cloudera --table " \
           "customers --hive-import --create-hive-table --hive-table airflow.customers "
    return f"{cmd1} && {cmd2}"


with DAG(
        dag_id="Customer_360_pipeline",
        start_date=days_ago(1),
        schedule_interval="@daily",
        catchup=False,
        tags=["customer_360", "aws"]

) as dag:
    aws_sensor = HttpSensor(
        task_id="watch_for_order_s3",
        endpoint="orders.csv",
        http_conn_id="orders_s3",
        retries=10,
        response_check=lambda response: response.status_code == 200,
        retry_delay=timedelta(seconds=10)
    )

    ssh_edge_download_task = SSHOperator(
        task_id="download_orders",
        ssh_conn_id="cloudera",
        command=download_order_command,

    )
    import_customers_info = SSHOperator(
        task_id="import_customers_from_sql",
        ssh_conn_id="cloudera",
        command=load_customer_info_cmd()
    )

    upload_orders_to_hdfs = SSHOperator(
        task_id="upload_orders_to_hdfs",
        ssh_conn_id="cloudera",
        command="hdfs dfs -rm -R -f airflow_input && hdfs dfs -mkdir -p airflow_input && hadoop fs -put "
                "./airflow_pipeline/orders.csv airflow_input/ "
    )
    run_spark_job = SSHOperator(
        task_id="run_spark_job",
        ssh_conn_id="cloudera",
        command=get_orders_filter_cmd()
    )

    slack_success_task = SlackWebhookOperator(
        task_id="Success_notify",
        http_conn_id="slack",
        message="Data loaded successfully",
        channel="#alerts",
        username="airflow",
        webhook_token=slack_password()
    )
    slack_failure_task = SlackWebhookOperator(
        task_id="failure_notify",
        http_conn_id="slack",
        message="Data loading is failed",
        channel="#alerts",
        username="airflow",
        webhook_token=slack_password(),
        trigger_rule="all_failed"
    )

    aws_sensor >> import_customers_info >> [slack_success_task, slack_failure_task]
    aws_sensor >> ssh_edge_download_task >> upload_orders_to_hdfs >> run_spark_job >> [slack_success_task,
                                                                                       slack_failure_task]
