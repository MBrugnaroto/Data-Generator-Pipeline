import os
from os.path import join
from pathlib import Path
from datetime import datetime
from operators.invoice_generator_operator import InvoiceGeneratorOperator
from hooks.mariadb_hook import MariaDBHook


SOURCE_FOLDER=str(Path(__file__).parents[2])
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


def execute_dag(max_invoices, max_items, quantity):
    #hook = get_connection()
    
    generator_start = datetime.now()
    InvoiceGeneratorOperator(
                            database=os.environ["DB"],
                            host=os.environ["HOST"],
                            port=os.environ["PORT"],
                            user=os.environ["USER"],
                            password=os.environ['PASSWORD'],
                            max_invoices=max_invoices, 
                            max_items=max_items,
                            quantity=quantity,
                            path_file=PATH_DATALAKE\
                                        .format(layer="silver", db=os.environ.get("DB"))
                            )\
                            .executor()
    generator_end = datetime.now()
    total = (generator_end-generator_start).total_seconds()
    
    #hook.update_data("round_statistics", "operator_total_time", total, "generator")
    