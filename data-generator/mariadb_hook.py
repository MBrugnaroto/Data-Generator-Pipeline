import pandas as pd
import mysql.connector as MariaDB
from utils import handle_query as HQ
from typing import List


class MariaDBHook():
    def __init__(self, 
                 database=None, 
                 host=None, 
                 port=None, 
                 user=None, 
                 password=None) -> None:
        self.database = database
        self.host = host
        self.port = port 
        self.user = user 
        self.pw = password
        
        
    def get_conn(self) -> MariaDB.connect:
        return MariaDB.connect(
            host=self.host,
            user=self.user,
            passwd=self.pw,
            db=self.database,
            port=self.port
        )
        
        
    def get_tables(self) -> List:
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return tables


    def bulk_dump(self, table) -> pd.DataFrame:
        conn = self.get_conn()
        dump = pd.read_sql(HQ.get_select_table_sql(table), conn)
        conn.close()
        return dump
    
    
    def bulk_load(self, path_file, table) -> None:
        conn = self.get_conn()
        cursor = conn.cursor()
        bulk_query = HQ.upload_data_from_file(path_file, table)
        cursor.execute(bulk_query)
        conn.commit()
        cursor.close()
        conn.close()
        