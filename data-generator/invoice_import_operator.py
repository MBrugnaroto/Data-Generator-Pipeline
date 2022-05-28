import os
from os.path import join
from pathlib import Path
from datetime import datetime
from mariadb_hook import MariaDBHook


SOURCE_FOLDER=str(Path(__file__).parents[0])
PATH_DATALAKE=join(
            SOURCE_FOLDER,
            "datalake",
            "{layer}",
            "{db}",
            "{table}",
            "{filename}"           
)


class InvoiceImportGenerator():
    def __init__(self,
                 host=None, 
                 port=None, 
                 user=None, 
                 password=None) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.database = "DB_TEST"
        self.host = host or "127.0.0.1"
        self.port = port or 3306
        self.user = user or os.environ.get("USER") or 'root'
        self.pw = password or os.environ.get('PASSWORD') or '' 

    def call_dump(self, hook, table, dl_table):
        hook.bulk_load(PATH_DATALAKE.format(layer="silver", 
                                    db="DB_TEST", 
                                    table=f"{dl_table}",
                                    filename=f"generate_date={self.date}.csv"),
                       table)

    def executor(self):
        hook = MariaDBHook(
                    database=self.database,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.pw
        )
        self.call_dump(hook, "notas_fiscais", "invoices")
        self.call_dump(hook, "itens_notas_fiscais", "items")
        

if __name__=='__main__':
    InvoiceImportGenerator().executor()
