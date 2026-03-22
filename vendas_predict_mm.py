import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

df_vendas  = pd.read_csv('./data/processed/vendas_2023_2024_processed.csv', parse_dates=["sale_date"])
df_produtos = pd.read_csv('./data/processed/produtos_processed.csv')

produto_nome = "Motor de Popa Yamaha Evo Dash 155HP"
id_produto = df_produtos[df_produtos['name'] == produto_nome]['code'].values[0]

df_produto = df_vendas[df_vendas['id_product'] == id_produto].copy()

datas = pd.date_range(start=min(df_vendas["sale_date"]), end=max(df_vendas["sale_date"]), freq='D')
df_calendario = pd.DataFrame({'data': datas})

vendas_dia = df_produto.groupby('sale_date')['qtd'].sum().reset_index()
vendas_dia.columns = ['data', 'qtd']

df_venda_produto = df_calendario.merge(vendas_dia, on='data', how='left')
df_venda_produto['qtd'] = df_venda_produto['qtd'].fillna(0)

df_venda_produto['previsao'] = (
    df_venda_produto['qtd']
    .shift(1)                          
    .rolling(window=7, min_periods=7)
    .mean()
)

df_venda_produto = df_venda_produto.dropna()

treino = df_venda_produto[df_venda_produto['data'] <= '2023-12-31'].copy()
teste = df_venda_produto[
    (df_venda_produto['data'] >= '2024-01-01') &
    (df_venda_produto['data'] <= '2024-01-31')
].copy()

mae = mean_absolute_error(teste['qtd'], teste['previsao'])
print(f"MAE: {mae:.4f} unidades/dia")



# GRAFICO
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(teste['data'], teste['qtd'],
        label='Real', color='steelblue', linewidth=2, marker='o', markersize=4)
ax.plot(teste['data'], teste['previsao'],
        label='Previsto (Média Móvel 7d)', color='orange',
        linewidth=2, linestyle='--', marker='x', markersize=4)

ax.fill_between(teste['data'], teste['qtd'], teste['previsao'],
                alpha=0.1, color='red', label='Erro')

ax.set_title(f'Previsão de demanda — {produto_nome}\nJaneiro 2024 | MAE: {mae:.4f}',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Data', fontsize=11)
ax.set_ylabel('Quantidade vendida', fontsize=11)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.grid(True, linestyle='--', alpha=0.5)
ax.set_axisbelow(True)
plt.xticks(rotation=30)

plt.tight_layout()
plt.savefig('./reports/previsao_demanda.png', dpi=150, bbox_inches='tight')
plt.show()