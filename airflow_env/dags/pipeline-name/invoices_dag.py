import os
from os.path import join
from pathlib import Path
from datetime import datetime
from plugins.airflow_operators.invoice_generator_operator import InvoiceGeneratorOperator
from plugins.airflow_operators.invoice_import_operator import InvoiceImportGenerator
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


def invoice_dag(id, max_invoices, max_items, quantity):
    hook = get_connection()
    
    generator_start = datetime.now()
    InvoiceGeneratorOperator(
        max_invoices=max_invoices, 
        max_items=max_items,
        quantity=quantity,
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
    