import os
import pandas as pd
from os.path import join
from pathlib import Path
from datetime import datetime
from utils import random_value_generators as RVG
from mariadb_hook import MariaDBHook
from typing import Dict, List


SOURCE_FOLDER=str(Path(__file__).parents[0])
PATH_DATALAKE=join(
            SOURCE_FOLDER,
            "datalake",
            "{layer}",
            "{db}"           
)


class InvoiceGeneratorOperator():
    def __init__(self, max_invoices, 
                 max_items, quantity,
                 path_file, host=None, 
                 port=None, user=None, 
                 password=None) -> None:
        self.date =  datetime.today().strftime('%Y-%m-%d')
        self.dict_customers = {}
        self.dict_sellers = {}
        self.dict_products = {}
        self.max_invoices = max_invoices
        self.max_items = max_items
        self.quantity = quantity
        self.path_file = path_file
        self.database = "DB_TEST"
        self.host = host or "127.0.0.1"
        self.port = port or 3306
        self.user = user or os.environ.get("USER") or 'root'
        self.pw = password or os.environ.get('PASSWORD') or '' 
    
    
    def make_dir(self, path_file) -> str:
        if not os.path.exists(path_file):
            os.makedirs(path_file)
        return path_file
    
    
    def generate_new_items(self, number_invoice) -> Dict[str, List]:
        new_items_invoices = {}
        
        for i in range(self.max_items):
            key = RVG.get_rand_key(self.dict_customers)
            product_code = self.dict_products[key]['CODIGO_DO_PRODUTO']
            item_key = f'{number_invoice}{product_code}'

            if item_key not in new_items_invoices:
                product_price = self.dict_products[key]['PRECO_DE_LISTA']
                quantity = RVG.generate_rand_number(0, self.quantity)
                new_items_invoices[item_key] = [number_invoice, 
                                                product_code, 
                                                quantity, 
                                                product_price]
        return new_items_invoices
    
    
    def export_csv(self, df, path_dest) -> None:
        pd.DataFrame.from_dict(df, orient='index')\
                    .reset_index(drop=True)\
                    .to_csv(
                        join(
                            path_dest,
                            f"generate_date={self.date}.csv"
                        ),
                        index=False, 
                        header=False)    
    
    
    def dict_to_csv(self, new_invoices, new_items_invoices) -> None:
        path_items = self.make_dir(join(self.path_file, "items"))
        path_invoices = self.make_dir(join(self.path_file, "invoices"))
        self.export_csv(new_invoices, path_invoices)
        self.export_csv(new_items_invoices, path_items)
        
    
    def generate_new_invoices(self, df_invoices) -> None:
        last_invoice  = df_invoices['NUMERO'].max() + 1
        tax_median = df_invoices['IMPOSTO'].median()
        new_invoices = {}
        new_items_invoices = {}
        
        for i in range(self.max_invoices):
            number_invoice = last_invoice + i
            customer_cpf = RVG.get_rand_value(self.dict_customers, 'CPF')
            seller_id = RVG.get_rand_value(self.dict_sellers, 'MATRICULA')
            new_invoices[number_invoice] = [customer_cpf, 
                                            seller_id, 
                                            self.date, 
                                            number_invoice, 
                                            tax_median]
            
            new_items_invoices.update(
                self.generate_new_items(number_invoice)
                )
        self.dict_to_csv(new_invoices, new_items_invoices)
    
    
    def set_tables(self, dump_tables) -> None:
        self.dict_customers = dump_tables['tabela_de_clientes']\
                                            .to_dict('index')
        self.dict_sellers = dump_tables['tabela_de_vendedores']\
                                            .to_dict('index')
        self.dict_products = dump_tables['tabela_de_produtos']\
                                            .to_dict('index')
    
    def executor(self, context=None) -> None:
        hook = MariaDBHook(
                    database=self.database,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.pw
        )
        
        tables = hook.get_tables()
        dump_tables = {table[0]:hook.bulk_dump(table[0]) for table in tables}
        self.set_tables(dump_tables)
        df_invoices = dump_tables['notas_fiscais']
        self.generate_new_invoices(df_invoices)
        
        
if __name__=='__main__':
    InvoiceGeneratorOperator(
            max_invoices=100000, 
            max_items=1,
            quantity=100,
            path_file=PATH_DATALAKE\
                        .format(layer="silver", db="DB_TEST")
            )\
            .executor()