import pandas as pd
from datetime import datetime
from utils import random_value_generators as RVG
from mariadb_hook import MariaDBHook

class InvoiceGeneratorOperator():
    def __init__(self, max_invoices, max_items, quantity) -> None:
        self.date =  datetime.today().strftime('%Y-%m-%d')
        self.dict_customers = {}
        self.dict_sellers = {}
        self.dict_products = {}
        self.max_invoices = max_invoices
        self.max_items = max_items
        self.quantity = quantity

    def generate_new_items(self, number_invoice):
        new_items_invoices = {}
        
        for i in range(self.max_items):
            key = RVG.get_rand_key(self.dict_customers)
            product_code = self.dict_products[key]['CODIGO_DO_PRODUTO']
            item_key = f'{number_invoice}{product_code}'

            if item_key not in new_items_invoices:
                product_price = self.dict_products[key]['PRECO_DE_LISTA']
                quantity = RVG.generate_rand_number(0, self.quantity)
                new_items_invoices[item_key] = [number_invoice, product_code, quantity, product_price]
                
        return new_items_invoices
    
    def dict_to_csv(self, new_invoices, new_items_invoices):
        df_new_itens_invoices = pd.DataFrame.from_dict(new_invoices, orient='index').reset_index(drop=True)
        df_new_invoices = pd.DataFrame.from_dict(new_items_invoices, orient='index').reset_index(drop=True)
        df_new_invoices.to_csv('/home/mbrugnar/workspace/data-engineering-studies/data-generator/datalake/df_new_invoices.csv', index=False, header=False)    
        df_new_itens_invoices.to_csv('/home/mbrugnar/workspace/data-engineering-studies/data-generator/datalake/df_new_itens_invoices.csv', index=False, header=False)    
        
    def generate_new_invoices(self, df_invoices):
        last_invoice  = df_invoices['NUMERO'].max() + 1
        tax_median = df_invoices['IMPOSTO'].median()
        new_invoices = {}
        new_items_invoices = {}
        
        for i in range(self.max_invoices):
            number_invoice = last_invoice + i
            customer_cpf = RVG.get_rand_value(self.dict_customers, 'CPF')
            seller_id = RVG.get_rand_value(self.dict_sellers, 'MATRICULA')
            new_invoices[number_invoice] = [customer_cpf, seller_id, self.date, number_invoice, tax_median]
            
            new_items_invoices.update(self.generate_new_items(number_invoice))
        
        self.dict_to_csv(new_invoices, new_items_invoices)
    
    def executor(self, context=None):
        hook = MariaDBHook()
        tables = hook.get_tables()
        dump_tables = {table[0]:hook.bulk_dump(table[0]) for table in tables}
        self.dict_customers = dump_tables['tabela_de_clientes'].to_dict('index')
        self.dict_sellers = dump_tables['tabela_de_vendedores'].to_dict('index')
        self.dict_products = dump_tables['tabela_de_produtos'].to_dict('index')
        df_invoices = dump_tables['notas_fiscais']
        self.generate_new_invoices(df_invoices)
        #hook.bulk_load('/home/mbrugnar/workspace/data-engineering-studies/data-generator/datalake')
        
if __name__=='__main__':
    InvoiceGeneratorOperator(10, 10, 10).executor()