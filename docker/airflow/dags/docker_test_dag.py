from airflow.decorators import task, dag
from airflow.operators.docker_operator import DockerOperator

from datetime import datetime

ENV_DOCKER = {
    'TEST': 'Testando env'
}

@dag(start_date=datetime(2022, 7, 9), schedule_interval='@daily', catchup=False)
def docker_dag():
    
    @task()
    def t1():
        pass

    t2 = DockerOperator(
        task_id='t2',
        image='mbrugnar/testing:latest',
        container_name='testing_container',
        force_pull=True,
        auto_remove=True,
        network_mode='bridge',
        environment=ENV_DOCKER
    )
    t1() >> t2
    
dag = docker_dag()