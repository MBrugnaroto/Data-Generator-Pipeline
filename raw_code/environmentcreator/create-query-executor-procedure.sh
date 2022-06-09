#!/bin/bash

for db in "$@"
do
mysql -u root <<EOF
        USE $db;
        DROP PROCEDURE IF EXISTS PR_QUERY_EXECUTOR;

        DELIMITER &&
        CREATE PROCEDURE PR_QUERY_EXECUTOR(QUERY LONGTEXT)
        BEGIN
            PREPARE SMT FROM QUERY;
            EXECUTE SMT;
            DEALLOCATE PREPARE SMT;
        END &&
        DELIMITER ;
EOF
if [ $? -eq 0 ]
then
        echo 'Creation of Query Executor Procedure in' $db 'database was successfull.'
else
        echo 'Creation of Query Executor Procedure in' $db 'database was not performed.'
fi
done