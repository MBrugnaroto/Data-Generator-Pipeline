#!/bin/bash

docker-compose -f airflow/docker-compose.yml down -v
docker-compose -f datawarehouse/docker-compose.yml down -v
