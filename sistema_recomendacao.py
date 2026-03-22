import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df_vendas   = pd.read_csv('./data/processed/vendas_2023_2024_processed.csv')
df_produtos = pd.read_csv('./data/processed/produtos_processed.csv')

df_interacao = df_vendas.groupby(['id_client', 'id_product'])['qtd'].sum().reset_index()

df_interacao['comprou'] = 1

# Pivota: linhas = clientes, colunas = produtos, valor = 0 ou 1
matriz = df_interacao.pivot_table(
    index='id_client',
    columns='id_product',
    values='comprou',
    fill_value=0
)

matriz_T = matriz.T

sim = cosine_similarity(matriz_T)

df_similares = pd.DataFrame(
    sim,
    index=matriz_T.index,
    columns=matriz_T.index
)

produto_referencia = 'GPS Garmin Vortex Maré Drift'
id_ref = df_produtos[df_produtos['name'] == produto_referencia]['code'].values[0]
print(f"\nProduto de referência: {produto_referencia} (ID: {id_ref})")

similares = df_similares[id_ref].drop(id_ref)  

top5 = similares.sort_values(ascending=False).head(5).reset_index()
top5.columns = ['id_product', 'similaridade']
top5 = top5.merge(df_produtos[['code', 'name']], left_on='id_product', right_on='code')

print("Top 3 produtos recomendados")
print(top5[['code', 'name', 'similaridade']].to_string(index=False))