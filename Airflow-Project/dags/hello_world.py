from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime


# Function to be called by PythonOperator
def hello_world():
    print("Hello, world! This is my first DAG.")


# Define default arguments for the DAG
default_args = {
    "owner": "admin",
    "start_date": datetime(2025, 4, 17),  # Use the current date or another start date
    "retries": 1,
    "catchup": False,  # To avoid backfilling
}

# Instantiate the DAG
dag = DAG(
    "hello_world_dag",  # Unique dag_id
    default_args=default_args,
    description="A simple Hello World DAG",
    schedule="@daily",  # This DAG will run daily (new format)
)

# Define the tasks

# Empty task to mark the beginning (replaces DummyOperator)
start_task = EmptyOperator(
    task_id="start",
    dag=dag,
)

# Python task that prints "Hello, world!"
python_task = PythonOperator(
    task_id="hello_world_task",
    python_callable=hello_world,  # Function to call
    dag=dag,
)

# Empty task to mark the end (replaces DummyOperator)
end_task = EmptyOperator(
    task_id="end",
    dag=dag,
)

# Set the task dependencies
(
    start_task >> python_task >> end_task
)  # Execute tasks in sequence: start -> python -> end
