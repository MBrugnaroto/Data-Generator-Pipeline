import os
from os.path import join
from pathlib import Path
from datetime import datetime
from plugins.operators.invoice_generator_operator import InvoiceGeneratorOperator
from plugins.operators.invoice_import_operator import InvoiceImportGenerator
from plugins.hooks.mariadb_hook import MariaDBHook


SOURCE_FOLDER=str(Path(__file__).parents[2])
PATH_DATALAKE=join(
            SOURCE_FOLDER,
            "datalake",
            "{layer}",
            "{db}",           
)


def get_connection():
    return MariaDBHook(
            database="DB_TEST",
            host="127.0.0.1",
            port=3306,
            user=os.environ.get("USER"),
            password=os.environ.get('PASSWORD')
        )


def invoice_dag(id):
    hook = get_connection()
    
    generator_start = datetime.now()
    InvoiceGeneratorOperator(
        max_invoices=100000, 
        max_items=1,
        quantity=10,
        path_file=PATH_DATALAKE\
                    .format(layer="silver", db="DB_TEST"),
        id=id)\
        .executor()
    generator_end = datetime.now()
    total = (generator_end-generator_start).total_seconds()
    
    hook.update_data("round_statistics", "operator_total_time", total, id, "generator")
    
    import_start = datetime.now()
    InvoiceImportGenerator(
        path_dump=PATH_DATALAKE\
                    .format(layer="silver", db="DB_TEST"),
        id=id)\
        .executor()
    import_end = datetime.now()
    total = (import_end-import_start).total_seconds()
    
    hook.update_data("round_statistics", "operator_total_time", total, id, "import")
    