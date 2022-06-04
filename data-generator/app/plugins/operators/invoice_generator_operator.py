import os
import pandas as pd
from os.path import join
from datetime import datetime
from ..utils import random_value_generators as RVG
from ..utils import file_manager as FM
from ..hooks.mariadb_hook import MariaDBHook
from typing import Dict, List
    

class InvoiceGeneratorOperator():
    def __init__(self, max_invoices, id,
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
        self.id = id 
        self.total_items = 0
    
        
    def generate_new_items(self, number_invoice) -> Dict[str, List]:
        new_items_invoices = {}
        
        for i in range(self.max_items):
            key = RVG.get_rand_key(self.dict_customers)
            product_code = self.dict_products[key]['CODIGO_DO_PRODUTO']
            item_key = f'{number_invoice}{product_code}'

            if item_key not in new_items_invoices:
                self.total_items += 1
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
        path_items = FM.make_dir(join(self.path_file, "items"))
        path_invoices = FM.make_dir(join(self.path_file, "invoices"))
        self.export_csv(new_invoices, path_invoices)
        self.export_csv(new_items_invoices, path_items)
    
    
    def generate_new_invoices(self, hook) -> None:
        last_invoice = hook.table_statistic("notas_fiscais", "MAX", "NUMERO") + 1
        tax_median = hook.table_statistic("notas_fiscais", "AVG", "IMPOSTO") 
        new_invoices = {}
        new_items_invoices = {}
        
        for i in range(self.max_invoices):
            number_invoice = last_invoice + i
            customer_cpf = RVG.get_rand_value_dict(self.dict_customers, 'CPF')
            seller_id = RVG.get_rand_value_dict(self.dict_sellers, 'MATRICULA')
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
        dump_tables = {table[0]:hook.bulk_dump(table[0]) for table in tables if table[0] != 'round_statistics' and \
                                                                                table[0] != 'itens_notas_fiscais' and \
                                                                                table[0] != 'notas_fiscais'}
        self.set_tables(dump_tables)
        generate_start = datetime.now()
        self.generate_new_invoices(hook)
        generate_end = datetime.now()
        total = (generate_end - generate_start).total_seconds()
        
        hook.insert_data("round_statistics", 
                         ["id", "quantity", "function_total_time", "operator"], 
                         [self.id, self.max_invoices, total, "generator"])
        
        hook.insert_data("round_statistics", 
                         ["id", "quantity", "operator"], 
                         [self.id, self.total_items, "import"])
        