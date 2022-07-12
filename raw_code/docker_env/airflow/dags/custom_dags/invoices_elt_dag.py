from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.models import Variable

from datetime import datetime
from docker.types import Mount


ENV = {
    'DB': Variable.get("DB"),
    'HOST': Variable.get("HOST"),
    'PORT': Variable.get("PORT"),
    'USER': Variable.get("USER"),
    'PASSWORD': Variable.get("PASSWORD"),
    'MAX_INVOICES': Variable.get("MAX_INVOICES", default_var=10),
    'MAX_ITEMS': Variable.get("MAX_ITEMS", default_var=10),
    'QUANTITY': Variable.get("QUANTITY", default_var=100)
}

VOLUME = [
    Mount(target='/usr/src/app/datalake', source=Variable.get("DATALAKE"), type='bind')
]

ARGS = {
    "owner": "root",
    "depends_on_past": False,
    "start_date": datetime(2022, 7, 9),
    "schedule_interval": "0 9 * * *"
}


with DAG(
    dag_id="invoices_elt_dag", 
    default_args=ARGS,
    max_active_runs=1,
    catchup=False
) as dag:
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
    