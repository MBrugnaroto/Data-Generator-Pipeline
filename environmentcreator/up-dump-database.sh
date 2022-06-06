#!/bin/bash

dump(){
	for file in *
 	do
                mysql -u root $1 < $file
		if [ $? -eq 0 ]
		then
			echo "Dump from" $file "to" $1 "was peformed"
		else
			echo "Dump from" $file "to" $1 "was not performed"
		fi
	done
}

LOCAL=$(ls | grep dump)

if [ $(pwd | grep dump) ]
then
        dump $1
elif [ "${LOCAL:-0}" != 0 ]
then
        cd dump/
        dump $1
else
        echo "Dump folder not found."
fi