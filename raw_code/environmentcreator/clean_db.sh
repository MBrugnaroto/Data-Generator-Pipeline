#!/bin/bash

/bin/bash create-query-executor-procedure.sh $1
/bin/bash create-clean-db-procedure.sh $1

mysql -u root <<EOF
        USE $1
        CALL PR_CLEAN_DB();
EOF
if [ $? -eq 0 ]
then
        echo 'Database' $1 'cleaned'
else
        echo 'Could not clear' $1 'database.'
fi