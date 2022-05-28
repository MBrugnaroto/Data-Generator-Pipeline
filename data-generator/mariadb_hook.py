import os
import pandas as pd
import mysql.connector as MariaDB
from utils import handle_query as HQ

class MariaDBHook():
    def __init__(self, database=None, host=None, port=None, user=None, password=None) -> None:
        self.database = database or "DB_TEST"
        self.host = host or "127.0.0.1"
        self.port = port or 3306
        self.user = user or os.environ.get("USER") or 'root'
        self.pw = password or os.environ.get('PASSWORD') or '' 
        
    def get_conn(self):
        return MariaDB.connect(
            host=self.host,
            user=self.user,
            passwd=self.pw,
            db=self.database,
            port=self.port
        )
        
    def get_tables(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return tables

    def bulk_dump(self, table):
        conn = self.get_conn()
        dump = pd.read_sql(HQ.get_select_table_sql(table), conn)
        conn.close()
        return dump
    
    def bulk_load(self, path_file, table):
        conn = self.get_conn()
        cursor = conn.cursor()
        bulk_query = HQ.upload_data_from_file(path_file, table)
        cursor.execute(bulk_query)
        cursor.commit()
        cursor.close()
        conn.close()