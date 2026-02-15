from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


def extract_data(**kwargs):
    # Extract data logic here
    print("Extracting data...")


def transform_data(**kwargs):
    # Transform data logic here
    print("Transforming data...")


def load_mongodb(**kwargs):
    # Load data into MongoDB logic here
    print("Loading data into MongoDB...")


def load_mysql(**kwargs):
    # Load data into MySQL logic here
    print("Loading data into MySQL...")


def create_dag():
    dag = DAG( 
        dag_id='etl_pipeline', 
        schedule_interval='@daily', 
        start_date=datetime(2026, 2, 15), 
        catchup=False, 
    )

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        dag=dag,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        dag=dag,
    )

    load_mongodb_task = PythonOperator(
        task_id='load_mongodb',
        python_callable=load_mongodb,
        dag=dag,
    )

    load_mysql_task = PythonOperator(
        task_id='load_mysql',
        python_callable=load_mysql,
        dag=dag,
    )

    extract_task >> transform_task >> load_mongodb_task >> load_mysql_task


dag = create_dag()