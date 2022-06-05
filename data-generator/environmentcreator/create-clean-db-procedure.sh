#!/bin/bash

mysql -u root <<EOF
    USE $1

    DELIMITER $$
    CREATE PROCEDURE IF NOT EXISTS PR_CLEAN_DB()
    BEGIN
        CALL PR_QUERY_EXECUTOR('SET FOREIGN_KEY_CHECKS = 0;');
        CALL PR_QUERY_EXECUTOR('TRUNCATE TABLE itens_notas_fiscais;');
        CALL PR_QUERY_EXECUTOR('TRUNCATE TABLE notas_fiscais;');
        CALL PR_QUERY_EXECUTOR('SET FOREIGN_KEY_CHECKS = 1;');  
    END $$
    DELIMITER ;
EOF
if [ $? -eq 0 ]
then
        echo 'Creation of Clean DB procedure in' $1 'was successfull.'
else
        echo 'Creation of Clean DB procedure in' $1 'was not performed.'
fi