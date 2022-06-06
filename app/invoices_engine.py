import os
from dags.invoices_dag import invoice_dag
from plugins.hooks.mariadb_hook import MariaDBHook

def get_connection():
    return MariaDBHook(
            database="DB_TEST",
            host="127.0.0.1",
            port=3306,
            user=os.environ.get("USER"),
            password=os.environ.get('PASSWORD')
        )
    
if __name__=='__main__':
    hook = get_connection()
    hook.truncate_table("round_statistics")
    
    for i in range(1, 51):
        invoice_dag(i)
        