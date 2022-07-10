from airflow.decorators import dag
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount
from datetime import datetime

ENV = {
    'DB': 'DB_TEST',
    'HOST': 'db_container',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD': 'pw_root',
    'MAX_INVOICES': 10,
    'MAX_ITEMS': 10,
    'QUANTITY': 100
}

VOLUME = [
    Mount(target="/usr/src/app/datalake", source="/home/mbrugnar/workspace/data-generator/docker/datalake", type='bind')
]

@dag(start_date=datetime(2022, 7, 9), schedule_interval='@daily', catchup=False)
def generator_dag():
    t1 = DockerOperator(
        task_id='invoice_generator',
        image='mbrugnar/generator:latest',
        container_name='generator_container',
        environment=ENV,
        force_pull=True,
        auto_remove=True,
        network_mode="database_connect_network",
        mounts=VOLUME
    )
    
    t1
    
dag=generator_dag()