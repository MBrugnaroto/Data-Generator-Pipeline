#!/bin/bash
DB='DB_TEST'

/bin/bash clean_db.sh $DB
/bin/bash create-database.sh $DB
/bin/bash up-dump-database.sh $DB
/bin/bash create-table.sh $DB "round_statistics"
