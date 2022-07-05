from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator

default_args = {
    'owner': 'mbrugnar',    
    'start_date': datetime(2022, 7, 4),
    'depends_on_past': False,
    'email': ['brugnaroto@gmail.com'],
    'email_on_failure': True,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    }

with DAG(
    dag_id="testing_connection",
    description="A simple connection test with my MariaDB",
    default_args=default_args,
    schedule_interval="0 9 * * *",
    tags=["example", "mariadb"]
) as dag:
    getTables = MySqlOperator(
        task_id="showTables",
        database="DB_TEST",
        mysql_conn_id="mariadb_default",
        sql="SHOW TABLES"
    )
    
    getTables
    