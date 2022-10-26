from airflow import DAG
#from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator

from datetime import timedelta
import pendulum

from config_priv import PERSONAL_EMAIL


def get_recently_played_data_from_spotify():
    from src.data import SpotifyClass
    SpotifyClass.get_data_from_spotify_api()



def json_data_to_sql_file():
    from src.data import SpotifyClass
    SpotifyClass.transform_data_to_sql_file()

args = {

    "owner": "bubba_tam",
    "start_date": pendulum.datetime(2022, 10, 21, tz="Europe/London"),
    "email" : [PERSONAL_EMAIL],
    "email_on_failure" : True,
    "email_on_retry" : True,
    "retries" : 1,
    "retry_delay" : timedelta(seconds=20)
}

dag = DAG(
    dag_id = "spotify_data_dag",
    default_args=args,
    # CRON expression for 19:45
    schedule_interval = "45 19 * * *",
    template_searchpath="src/sql_queries",
    catchup=False)

with dag:
    get_spotify_data = PythonOperator(
        task_id="extract_spotify_data",
        python_callable = get_recently_played_data_from_spotify
    )
    load_data_to_sql_file = PythonOperator(
        task_id="transfer_data_to_sql_file",
        python_callable = json_data_to_sql_file
    )
    create_db_table = MySqlOperator(
        task_id = "create_db_table",
        mysql_conn_id = "local_mysql",
        sql="create_my_played_tracks_table.sql"
    )
    insert_spotify_data_to_mysql = MySqlOperator(
        task_id = "insert_data_to_mysql",
        mysql_conn_id = "local_mysql",
        sql="append_spotify_music_to_played_tracks_table.sql"
    )

    get_spotify_data >> load_data_to_sql_file >> create_db_table >> insert_spotify_data_to_mysql