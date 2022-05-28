_SIMPLE_SELECT_TEMPLATE = \
    """
    {% if show_columns %}
        {% set columns = '\n    ,'.join(show_columns) %}
    {% endif %}
    SELECT
        {% if columns %}
            {{ columns | sqlsafe }}
        {% else %}
            * 
        {% endif %}
    FROM 
        {{ table | sqlsafe }}
    """
    
_UPLOAD_FROM_FILE = \
    """
    LOAD DATA INFILE {{ path_file }}
    INTO TABLE {{ table | sqlsafe}}
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    """