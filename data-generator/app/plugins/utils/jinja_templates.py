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
    
_INSERT_DATA = \
    """
    {% if in_columns %}
        {% set columns = ', '.join(in_columns) %}
    {% endif %}
    INSERT INTO {{ table | sqlsafe }} 
    {% if columns %}
        ({{ columns | sqlsafe }})
    {% endif %}
    VALUES {{ values | inclause}}
    """
    
_UPDATE_DATE = \
    """
    UPDATE {{ table | sqlsafe}}
    SET 
        {{ column | sqlsafe }} = {{ value }}
    WHERE
        id={{ id }} AND operator={{ operator }} 
    """
    
_TRUNCATE_TABLE = \
    """
    TRUNCATE TABLE {{ table | sqlsafe}}
    """
    
_TABLE_STATISTICS = \
    """
    SELECT
        {{ operator | sqlsafe }}({{ column | sqlsafe }})
    FROM
        {{ table | sqlsafe }}
    """