import pandas as pd
import mysql.connector as MariaDB
from ..utils import handle_query as HQ
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
    
    
    def insert_data(self, table, columns, data) -> None:
        conn = self.get_conn()
        cursor = conn.cursor()
        bulk_query = HQ.insert_data(table, data, columns)
        cursor.execute(bulk_query)
        conn.commit()
        cursor.close()
        conn.close()
        
        
    def update_data(self, table, value, id, operator) -> None:
        conn = self.get_conn()
        cursor = conn.cursor()
        bulk_query = HQ.update_data(table, value, id, operator)
        cursor.execute(bulk_query)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def truncate_table(self, table) -> None:
        conn = self.get_conn()
        cursor = conn.cursor()
        bulk_query = HQ.truncate_table(table)
        cursor.execute(bulk_query)
        conn.commit()
        cursor.close()
        conn.close()
        
        
    def table_statistic(self, table, operator, column) -> None:
        conn = self.get_conn()
        cursor = conn.cursor()
        bulk_query = HQ.table_statistics(table, operator, column)
        cursor.execute(bulk_query)
        value = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return value[0]