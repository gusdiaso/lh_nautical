from sqlalchemy import create_engine
from utils.populate_table_database import populate_table_database

try:
  engine = create_engine("postgresql://postgres:postgres@localhost:5432/lh_nauticals")

  populate_table_database(engine=engine, name_table="vendas", name_file="raw/vendas_2023_2024.csv")
  populate_table_database(engine=engine, name_table="produtos_raw", name_file="raw/produtos_raw.csv")
  populate_table_database(engine=engine, name_table="clientes_crm", name_file="raw/clientes_crm.json")
  populate_table_database(engine=engine, name_table="custos_importacao", name_file="raw/custos_importacao.json")

  populate_table_database(engine=engine, name_table="vendas_processed", name_file="processed/vendas_2023_2024_processed.csv")
  populate_table_database(engine=engine, name_table="custos_importacao_processed", name_file="processed/custos_importacao_processed.csv")
  populate_table_database(engine=engine, name_table="produtos_processed", name_file="processed/produtos_processed.csv")
  populate_table_database(engine=engine, name_table="clientes_crm_processed", name_file="processed/clientes_crm_processed.csv")

except Exception as e:
  print("Erro ao carregar dados para banco!", e)
