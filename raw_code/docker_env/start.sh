#!/bin/bash

/bin/bash prepare-env.sh
docker-compose -f datawarehouse/docker-compose.yml up -d
docker-compose -f airflow/docker-compose.yml up airflow-init -d
docker-compose -f airflow/docker-compose.yml up -d