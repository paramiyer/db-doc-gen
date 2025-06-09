import pandas as pd
from sqlalchemy import create_engine, inspect

def fetch_all_tables(db_uri, schema):
    engine = create_engine(db_uri)
    inspector = inspect(engine)
    # For most DBs: 'schema' argument is optional but recommended for non-default schemas
    tables = inspector.get_table_names(schema=schema)
    return tables

def fetch_table_metadata(db_uri, schema, tables):
    engine = create_engine(db_uri)
    inspector = inspect(engine)
    records = []

    for table in tables:
        columns = inspector.get_columns(table, schema=schema)
        primary_keys = inspector.get_pk_constraint(table, schema=schema)['constrained_columns']
        foreign_keys = inspector.get_foreign_keys(table, schema=schema)
        indexes = inspector.get_indexes(table, schema=schema)

        for col in columns:
            col_name = col['name']
            data_type = str(col['type'])

            # Determine key type
            if col_name in primary_keys:
                key_type = 'PK'
            elif any(col_name in fk['constrained_columns'] for fk in foreign_keys):
                key_type = 'FK'
            else:
                key_type = ''

            # Determine index status
            is_indexed = any(col_name in idx.get('column_names', []) for idx in indexes)
            index_flag = 'Yes' if is_indexed else 'No'

            records.append({
                'Table': table,
                'Col': col_name,
                'Data Type': data_type,
                'Key': key_type,
                'Index': index_flag,
                'Description': None
            })

    df_schema = pd.DataFrame(records)
    return df_schema
