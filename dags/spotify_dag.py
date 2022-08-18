from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

import sys 
from pprint import pprint


from config_priv import PERSONAL_EMAIL
from src.data import SpotifyClass
from src import app


def example_1():
    pprint(sys.path)
def example_2():
    print("hello, i am back")

args = {

    "owner": "bubba_tam",
    "start_date": days_ago(0),
    "email" : PERSONAL_EMAIL,
    "email_on_failure" : False,
    "email_on_retry" : False,
    "retries" : 1,
    "retry_delay" : timedelta(seconds=20)
}
#define DAG
dag = DAG(
    dag_id = 'spotify_data_dag',
    default_args=args,
    schedule_interval=timedelta(days=1))

with dag:
    extract_spotify_data = PythonOperator(
        task_id='extract_spotify_data',
        #python_callable = example_1
        python_callable = app.flask_app.run(debug=True)
    )

    load_spotify_data = PythonOperator(
        task_id='load_spotify_data',
        #python_callable = example_2
        python_callable = SpotifyClass.load_data_to_sql()
    )

    extract_spotify_data >> load_spotify_data