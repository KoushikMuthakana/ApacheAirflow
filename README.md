# Apache Airflow
- Apache Airflow is a way to programmatically author,schedule and monitor data pipilines


### Core Components
- [Web server](/notes/webserver.ipynb)
- [Scheduler](/notes/schedular.ipynb)
- [Meta Database](/notes/database.ipynb)
- [Executor](/notes/executor.ipynb)
- [Worker](/notes/worker.ipynb)

### Core Concepts
- DAG
    * Is a graph object representation of data pipeline
    * Nodes are represented as tasks and edges reperesents as dependencies between tasks
- Operator
    
    * Describes a single tasks in the data pipeline
    * Eg: If any bash command needs to execute , then operator named BashOperator is used
    * This operator will be task in DAG

- Task
    
    * Is an instance of an operator

- TaskInstance

    * Is a specific execution of task, which is DAG+ task+time

Workflow -  All the above core concepts combined is workflow

### Architecture:

* Single Node

![Single Node Architecture ](/images/singlenode.png)

-   In single node all the components, Webserver, Executor, scheduler will be on the same node.
- It is better to maintain metadata database on the seperate node for failover  
- Queueing service is a part of executor, which helps the tasks to execute in which order, 
    
    * Queueing services - RabbitMQ


![Multi Node Architecture ](/images/cluster.png)

- In the cluster(Multi Node), only webserver and scheduler will be on the same node.
- All the executor n, will be on seperate node, helps to reduce the load
- Can add executors on fly, if needed to increase the processing load

Note: Using an external Queue service like RabbitMQ is mandatory

### Execution Flow:

Step 1: Scheduler reads the DAGs folder, if any python program associated with DAG is there or not

Step 2: If a DAG exists, it must be triggered. A DAGRun object is created based on scheduling parameter
    

Step 3: A Taskinstance is instantiated for each task need to be executed and flagged "Scheduled" in the metadata database

Step 4: The scheduler gets all the tasks with status "Scheduled" from the metadata database, changes the state to "Queue" and sends them to the executors to execute 

Step 5: Executors pulls outs the each task from the Queue based on the execution priority. Changes the state from "Queued" to "Running" and workers start executing the TaskInstance

Step 6: When the task is finished, executor changes the state from "Running" to its final status like Success, failed, etc. 

- DAGRun status is also updated with the status Success or failure

Webserver continuously fetches the data from the metadata database and updates the UI accordingly 



### Installation Steps

1. Create virtual environment
    * Mac and Linux
        
        * python3 -m venv <b>env_name</b>
    * windows

        * py -m venv <b>env_name</b> 
2. Activate the virtual environment 
    *    source <b>env_name></b>/bin/activate

3.Install apache airflow with custom plugins

* pip install apache-airflow[postgres,gcp]==1.10.12 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
    Once the installation all the packages is done,type
    
    Ref: Instalation Guide - [Offical Document](https://airflow.apache.org/docs/stable/installation.html)

* airflow intidb #Which initializes the database with necessary tables.
        * Folder Structure
            |
            
            |-- airflow.cfg  # All configurations
            
            |-- airflow.db # SQL lite db

            |-- logs # logs

            |-- uninttests.cfg

    * Create a dags folder
        
        * default dags folder path will be at airflow.cfg
          
            ``` grep dags_folder aitflow.cfg ```


# Docker 
 
 Step 1: Download docker-compose file [docker-compose](/docker-compose.yaml)
 
 Step 2: Initiate the db
 
  ```docker-compose up airflow-init ```
 
 Step 3: Create and start the airflow services
 
 ```docker-compose up -d```
 
 
 

### Useful commands

* airflow initdb     # Initialize the metadata databse sqllite 
* airflow resetdb    # Drops all the metadata
* airflow webserver  # Starts the webserver
* airflow scheduler  # Starts the scheduler instance
* airflow list_dags  # list all dags
* airflow list_tasks <dag_name> # list all tasks
* airflow list_tasks <dag_name> --tree # list all tasks dependencies
* airflow test <dag_name> <task_name> <passed_date>
