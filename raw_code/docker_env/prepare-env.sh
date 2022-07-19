#!/bin/bash

if [ ! $(ls | grep datalake) ]; then
    mkdir -p datalake/
    if [ $? -eq 0 ]
    then
        echo "Datalake Created"
    else
        echo "Datalake creation failed"
    fi
fi

PATH_DL="$(pwd)/datalake"

cd airflow

sed -i "s@AIRFLOW_LOCAL_DL=.*@AIRFLOW_LOCAL_DL='${PATH_DL}'@" .env
sed -i "s@AIRFLOW_UID=.*@AIRFLOW_UID=$(id -u)@" .env

cd ../datawarehouse/

sed -i "s@DATALAKE_PATH=.*@DATALAKE_PATH=${PATH_DL}@" .env