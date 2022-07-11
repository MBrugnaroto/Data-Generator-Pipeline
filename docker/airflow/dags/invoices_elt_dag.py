from airflow.decorators import dag
from airflow.operators.docker_operator import DockerOperator
from click import command
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
    Mount(target='/usr/src/app/datalake', source='/home/mbrugnar/workspace/data-generator/docker/datalake', type='bind')
]

@dag(start_date=datetime(2022, 7, 9), schedule_interval='@daily', catchup=False)
def invoices_elt_dag():
    t1 = DockerOperator(
        task_id='invoice_generator',
        image='mbrugnar/generator:latest',
        container_name='generator_container',
        environment=ENV,
        force_pull=True,
        auto_remove=True,
        network_mode='database_connect_network',
        mounts=VOLUME
    )
    
    t2 = DockerOperator(
        task_id='invoice_loader',
        image='mbrugnar/loader:latest',
        container_name='loader_container',
        working_dir='/usr/src/app/services',
        command='engine.py',
        environment=ENV,
        force_pull=True,
        auto_remove=True,
        network_mode='database_connect_network',
        mounts=VOLUME
    )
    
    t1 >> t2
    
dag=invoices_elt_dag()