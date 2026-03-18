from sqlalchemy import create_engine
from utils.populate_database import populate_database

try:
  engine = create_engine("postgresql://postgres:postgres@localhost:5432/lh_nauticals")

  populate_database(engine=engine, name_table="vendas", name_file="produtos_raw.csv")
  populate_database(engine=engine, name_table="produtos_raw", name_file="vendas_2023_2024.csv")
  populate_database(engine=engine, name_table="clientes_crm", name_file="clientes_crm.json")
  populate_database(engine=engine, name_table="custos_importacao", name_file="custos_importacao.json")

except Exception as e:
  print("Erro ao carregar dados para banco!", e)
