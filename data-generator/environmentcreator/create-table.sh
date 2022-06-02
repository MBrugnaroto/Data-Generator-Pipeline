#!/bin/bash

mysql -u root <<EOF
		USE $1;

		CREATE TABLE IF NOT EXISTS $2 (
			id int NOT NULL, 
			quantity int, 
			operator_total_time float, 
			function_total_time float, 
			operator varchar(20) NOT NULL, 
			primary key(id, operator));
EOF
if [ $? -eq 0 ]
then
        echo 'Creation of' $2 'table was successfull.'
else
        echo 'Creation of' $2 'table was not performed.'
fi
