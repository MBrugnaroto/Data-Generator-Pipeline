#!/bin/bash

docker-compose -f airflow/docker-compose.yml down -v
docker-compose -f database/docker-compose.yml down -v
