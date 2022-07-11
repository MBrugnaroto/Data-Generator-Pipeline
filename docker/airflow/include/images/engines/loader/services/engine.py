import os
from os.path import join
from pathlib import Path
from datetime import datetime
from operators.invoice_import_operator import InvoiceImportGenerator
from hooks.mariadb_hook import MariaDBHook


SOURCE_FOLDER=str(Path(__file__).resolve().parents[1])
PATH_DATALAKE=join(
            SOURCE_FOLDER,
            "datalake",
            "{layer}",
            "{db}",           
)


def get_connection():
    return MariaDBHook(
                        database=os.environ["DB"],
                        host=os.environ["HOST"],
                        port=os.environ["PORT"],
                        user=os.environ["USER"],
                        password=os.environ['PASSWORD']
        )


def execute():
    #hook = get_connection()
    
    #import_start = datetime.now()
    InvoiceImportGenerator(
                            database=os.environ["DB"],
                            host=os.environ["HOST"],
                            port=os.environ["PORT"],
                            user=os.environ["USER"],
                            password=os.environ['PASSWORD'],
                            path_dump=PATH_DATALAKE\
                                        .format(layer="silver", db=os.environ["DB"]),
                            id=id)\
                            .executor()
    #import_end = datetime.now()
    #total = (import_end-import_start).total_seconds()
    
    #hook.update_data("round_statistics", "operator_total_time", total, id, "import")
    

if __name__=='__main__':
    execute()