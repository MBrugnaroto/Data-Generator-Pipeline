#!/bin/bash

dump(){
	for file in *
 	do
                mysql -uroot -p${MARIADB_ROOT_PASSWORD} DB_TEST < $file
		if [ $? -eq 0 ]
		then
			echo "Dump from" $file "to" $1 "was peformed"
		else
			echo "Dump from" $file "to" $1 "was not performed"
		fi
	done
}

cd docker-entrypoint-initdb.d/
LOCAL=$(ls | grep dump)

if [ $(pwd | grep dump) ]
then
        dump
elif [ "${LOCAL:-0}" != 0 ]
then
        cd dump/
        dump
else
        echo "Dump folder not found."
fi