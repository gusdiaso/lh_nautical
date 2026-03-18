import pandas as pd
import json
from sqlalchemy.types import JSON

def populate_database(engine, name_table, name_file):

    file_type = name_file.split(".")[-1]

    if file_type == "csv":
        df = pd.read_csv(f"data/{name_file}")

    elif file_type == "json":
        df = pd.read_json(f"data/{name_file}")

    else:
        raise ValueError(f"Formato de arquivo '{file_type}' não reconhecido. Use CSV ou JSON.")

    # Verifica se tem colunas com dicionario ou listas em uma amostra aleatória dos meus dados
    ## Evita uso computacional desnecessário

    json_columns = []
    sample = df.sample(n=10, random_state=42)

    for column in df.columns:
        if sample[column].apply(lambda x: isinstance(x, (dict, list))).any():
            df[column] = df[column].apply(json.dumps)
            json_columns.append(column)

    dtype = {column: JSON for column in json_columns}
    
    # ------------------------------

    df.to_sql(
        name_table,
        engine,
        if_exists="replace",
        index=False,
        dtype=dtype
    )

    print(f"Tabela '{name_table}' populada com sucesso usando '{name_file}'")