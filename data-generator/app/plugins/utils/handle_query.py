from . import jinja_templates
from jinjasql import JinjaSql
from six import string_types
from copy import deepcopy

def quote_sql_string(value):
    if isinstance(value, string_types):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return "'{}'".format(new_value)
    return value

def get_sql_from_template(query, bind_params):
    if not bind_params:
        return query
    params = deepcopy(bind_params)
    for key, val in params.items():
        params[key] = quote_sql_string(val)
    return query % params

def apply_sql_template(template, parameters):
    j = JinjaSql(param_style='pyformat')
    query, bind_params = j.prepare_query(template, parameters)
    return get_sql_from_template(query, bind_params)

def get_tables_from_db( conn):
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES;')
    tables = cursor.fetchall()
    cursor.close()
    return tables

def get_select_table_sql(table, show_columns=None):    
    data = {
        "table": table,
        "show_columns": show_columns
    }
    return apply_sql_template(jinja_templates._SIMPLE_SELECT_TEMPLATE, data)

def upload_data_from_file(path_file, table):
    data = {
        "path_file": path_file,
        "table": table
    }
    return apply_sql_template(jinja_templates._UPLOAD_FROM_FILE, data) 

def insert_data(table, data, columns=None):
    data = {
        "table": table,
        "values": data,
        "in_columns": columns
    }
    return apply_sql_template(jinja_templates._INSERT_DATA, data)

def update_data(table, value, id, operator):
    data = {
        "table": table,
        "value": value,
        "id": id,
        "operator": operator
    }
    return apply_sql_template(jinja_templates._UPDATE_DATE, data)

def truncate_table(table):
    data = {
        "table": table
    }
    return apply_sql_template(jinja_templates._TRUNCATE_TABLE, data)

def table_statistics(table, operator, column):
    data = {
        "table": table,
        "operator": operator,
        "column": column
    }
    return apply_sql_template(jinja_templates._TABLE_STATISTICS, data)
