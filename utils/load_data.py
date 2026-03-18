import pandas as pd
from sqlalchemy import create_engine

# Algo que se repete, é possivel fazer uma função

try:
  engine = create_engine("postgresql://postgres:postgres@localhost:5432/lh_nautical")

  df1 = pd.read_csv("data/vendas_2023_2024.csv")
  df1.to_sql("vendas", engine, if_exists="replace", index=False)

  df2 = pd.read_csv("data/produtos_raw.csv")
  df2.to_sql("produtos_raw", engine, if_exists="replace", index=False)
  
  df3 = pd.read_json("data/clientes_crm.json")
  df3.to_sql("clientes_crm", engine, if_exists="replace", index=False)

  df4 = pd.read_json("data/custos_importacao.json")
  df4.to_sql("custos_importacao", engine, if_exists="replace", index=False)

  print("Dados carregados com sucesso!")

except Exception as e:
  print("Erro ao carregar dados para banco!", e)

# ERRO: Erro ao carregar dados para banco! Execution failed on sql 'INSERT INTO custos_importacao...'