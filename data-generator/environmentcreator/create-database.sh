#!/bin/bash

mysql -u root <<EOF
		DROP DATABASE IF EXISTS $1;

		CREATE DATABASE $1
		DEFAULT CHARACTER SET UTF8;

		SHOW DATABASES;
EOF
if [ $? -eq 0 ]
then
        echo 'Creation of' $1 'database was successfull.'
else
        echo 'Creation of' $1 'database was not performed.'
fi

