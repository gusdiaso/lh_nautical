# 🚢 Desafio Lighthouse — LH Nautical

> Desafio técnico de Dados e IA — Indicium

---

## 📌 Contexto

A **LH Nautical** é uma empresa de varejo de peças e acessórios para embarcações que enfrenta um cenário de "caos dos dados": controle de estoque em planilhas manuais, sistemas desconectados e decisões baseadas em feeling.

O objetivo deste projeto é atuar como profissional de dados responsável por transformar esse cenário — realizando desde a limpeza e modelagem até a geração de insights preditivos e sistemas de recomendação.

---

## 👥 Stakeholders

| Nome               | Papel               | Prioridade                                       |
| ------------------ | ------------------- | ------------------------------------------------ |
| **Gabriel Santos** | Tech Lead           | Organização, documentação e clareza técnica      |
| **Marina Costa**   | Gerente de Negócios | Resultados práticos, margens e performance       |
| **Sr. Almir**      | Fundador            | Convencido por dados sólidos e linguagem simples |

---

## 📂 Datasets utilizados

| Arquivo                  | Tipo | Descrição                                            | Registros                      |
| ------------------------ | ---- | ---------------------------------------------------- | ------------------------------ |
| `vendas_2023_2024.csv`   | CSV  | Histórico de vendas de 2023 a 2024                   | 9.895                          |
| `produtos_raw.csv`       | CSV  | Catálogo de produtos com preços e categorias         | 157 → 150 após limpeza         |
| `clientes_crm.json`      | JSON | Base de clientes com nome, email e localização       | 49                             |
| `custos_importacao.json` | JSON | Histórico de custos de importação em USD por produto | 150 produtos → 1.260 registros |

### Relacionamento entre datasets

```
clientes_crm.json         vendas_2023_2024.csv        produtos_raw.csv
    code (id_client)  →→→  id_client | id_product  ←←←  code (id_product)
                                                                ↓
                                                    custos_importacao.json
                                                          product_id
```

---

## 🗂️ Estrutura do Projeto

```
project-root/
├── docker-compose.yml              ← Ambiente Docker para o banco de dados
├── load_data.py                    ← Script de carga no PostgreSQL
├── requirements.txt                ← Dependências Python
├── sistema_recomendacao.py         ← Sistema de recomendação
├── vendas_predict_mm.py            ← Modelo de previsão de demanda
├── README.md
│
├── data/
│   ├── raw/                        ← Dados originais (nunca modificar)
│   │   ├── vendas_2023_2024.csv
│   │   ├── produtos_raw.csv
│   │   ├── clientes_crm.json
│   │   └── custos_importacao.json
│   └── processed/                  ← Dados tratados
│       ├── vendas_2023_2024_processed.csv
│       ├── produtos_processed.csv
│       ├── clientes_crm_processed.csv
│       └── custos_importacao_processed.csv
│
├── notebooks/
│   ├── 01_eda_vendas.ipynb
│   ├── 02_etl_produtos.ipynb
│   ├── 03_etl_custos_importacao.ipynb
│   ├── 04_etl_vendas.ipynb
│   ├── 04_analise_prejuizo.ipynb
│   ├── 05_etl_clientes.ipynb
│   ├── 05_analise_fidelidade.ipynb
│   ├── 06_analise_venda_dia.ipynb
│   ├── 07_demanda_predict.ipynb
│   └── 08_sistema_recomendacao.ipynb
│
├── reports/                        ← Gráficos e visualizações gerados
│
├── sql/
│   ├── question_01.sql
│   ├── question_04.sql
│   ├── question_05.sql
│   └── question_06.sql
│
└── utils/
    ├── parse_date.py
    ├── dollar_sales_quote.py
    └── populate_table_database.py
```

---

## 🔬 Frentes de Análise

### 1. EDA — Análise Exploratória

Análise inicial dos dados brutos sem qualquer tratamento — apenas observar, agregar e descrever.

**Principais achados por dataset:**

`vendas_2023_2024.csv`

- 9.895 registros | 6 colunas | período: 01/01/2023 a 31/12/2024
- Coluna `sale_date` com dois formatos misturados (`YYYY-MM-DD` e `DD-MM-YYYY`)
- 1.018 outliers (10,29%) acima de R$ 813.028 pelo método IQR
- Valor R$ 2.222.973 aparece repetido — suspeito, requer validação com o negócio
- Nenhum valor nulo encontrado

`produtos_raw.csv`

- 157 linhas | coluna `price` armazenada como string com `R$`
- 7 códigos de produto duplicados
- Coluna `actual_category` com 39 variações para apenas 3 categorias reais

`clientes_crm.json`

- 49 clientes | 30 emails inválidos (61%) com `#` no lugar de `@`
- Coluna `location` sem padrão — mistura de separadores e ordem cidade/estado

`custos_importacao.json`

- 150 produtos com histórico de preços em USD
- Estrutura aninhada (`historic_data`) — requer normalização
- Datas no formato `DD/MM/YYYY` — diferente dos demais datasets

---

### 2. Tratamento de Dados

**`produtos_raw.csv`**

- Padronização de `actual_category`: 39 variações normalizadas para 3 categorias via dicionário de mapeamento (`eletrônicos`, `propulsão`, `ancoragem`)
- Conversão de `price`: removido prefixo `R$` e convertido para `float64`
- Remoção de 7 duplicatas pelo campo `code` → 157 para 150 linhas

**`custos_importacao.json`**

- Estrutura aninhada expandida em linhas individuais via `explode` + `json_normalize`
- 150 produtos → 1.260 registros (média de 8,4 entradas por produto)
- `start_date` convertida para `datetime` | `usd_price` convertido para `float`

**`vendas_2023_2024.csv`**

- Padronização de `sale_date`: dois formatos unificados para `YYYY-MM-DD`
- Adicionada coluna `cambio` com a cotação de venda do dólar do dia (API PTAX/BCB)

**`clientes_crm.json`**

- Emails corrigidos: `#` substituído por `@` e acentos removidos via `unidecode`
- Coluna `location` separada em `cidade` e `estado`

---

### 3. Dados Públicos — Análise de Prejuízo

Cruzamento entre custos de importação (USD) e vendas (BRL) usando câmbio real do Banco Central para identificar transações vendidas abaixo do custo.

**Metodologia:**

```
custo_total_brl = usd_price_vigente × câmbio_do_dia × qtd
prejuízo        = custo_total_brl − total_venda  →  se > 0, houve prejuízo
```

**Resultados:**

| Métrica                        | Valor                     |
| ------------------------------ | ------------------------- |
| Total de transações analisadas | 9.895                     |
| Transações com prejuízo        | 6.179 (62,4%)             |
| Transações sem prejuízo        | 3.716 (37,6%)             |
| Prejuízo total acumulado       | R$ 182.226.478,73         |
| Produto com maior % de perda   | ID 72 — 63,15% da receita |

**Insight:** 62,4% das transações operaram abaixo do custo de importação — indicando um problema sistêmico de precificação, não casos isolados. Com impostos e frete desconsiderados conforme premissa, o prejuízo real operacional pode ser ainda maior. A prioridade imediata deve ser a revisão da política de precificação, especialmente para os produtos com maior percentual de perda.

---

### 4. Análise de Clientes — Clientes Fiéis

Identificação dos clientes de elite com base em ticket médio alto e diversidade de categorias consumidas.

**Critérios de elegibilidade:**

- Ticket médio = faturamento total / número de transações
- Diversidade mínima de 3 categorias distintas compradas

**Resultados:**

- Top 10 clientes fiéis identificados com ticket médio e diversidade de categorias
- Categoria dominante do grupo elite mapeada para estratégia de campanhas

---

### 5. Dimensão de Calendário — Vendas por Dia da Semana

Construção de uma dimensão de datas para corrigir a média de vendas por dia da semana — incluindo dias sem venda com valor zero.

**Problema identificado:** agrupamento direto sobre a tabela de vendas ignora dias sem transação, inflando artificialmente a média.

**Solução:** geração de calendário completo via `generate_series` + `LEFT JOIN` + `COALESCE` para substituir nulos por zero.

---

### 6. Previsão de Demanda — Baseline com Média Móvel

Modelo baseline para previsão diária de vendas do produto `Motor de Popa Yamaha Evo Dash 155HP`.

**Configuração:**

| Parâmetro            | Valor                          |
| -------------------- | ------------------------------ |
| Período de treino    | 01/01/2023 a 31/12/2023        |
| Período de teste     | Janeiro de 2024                |
| Método               | Média móvel dos últimos 7 dias |
| Métrica de avaliação | MAE (Mean Absolute Error)      |

**Cuidados técnicos:**

- `shift(1)` aplicado antes do `rolling` para evitar data leakage
- Calendário diário completo com zeros nos dias sem venda

---

### 7. Sistema de Recomendação — Similaridade de Cosseno

Motor de recomendação baseado em comportamento de compra para a vitrine "Quem comprou isso, também levou".

**Metodologia:**

1. Matriz binária Usuário × Produto (1 = comprou, 0 = não comprou)
2. Transposição da matriz para Produto × Cliente
3. Cálculo de similaridade de cosseno entre todos os pares de produtos
4. Ranking dos 5 produtos mais similares ao `GPS Garmin Vortex Maré Drift`

---

## 🛠️ Tecnologias utilizadas

| Tecnologia            | Uso                                        |
| --------------------- | ------------------------------------------ |
| **Python 3**          | EDA, tratamento, modelos e visualizações   |
| **Pandas**            | Manipulação e análise de dados             |
| **Matplotlib**        | Visualizações e gráficos                   |
| **Scikit-learn**      | Similaridade de cosseno e métricas de ML   |
| **Requests**          | Consumo da API PTAX do Banco Central       |
| **Unidecode**         | Normalização de texto e remoção de acentos |
| **PostgreSQL**        | Banco de dados e queries SQL               |
| **Docker**            | Ambiente isolado do banco de dados         |
| **VSCode + SQLTools** | Desenvolvimento e consultas SQL            |
| **Jupyter Notebook**  | Desenvolvimento interativo e documentação  |

---

## ⚙️ Como executar

### Pré-requisitos

- Python 3.9+
- Docker com PostgreSQL configurado

### Instalação das dependências

```bash
pip install -r requirements.txt
```

### Subindo o banco de dados

```bash
docker-compose up -d
python load_data.py
```

### Conectando ao banco via Python

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql://usuario:senha@localhost:5432/nome_do_banco")
```

### Importando funções utilitárias nos notebooks

```python
import sys
sys.path.append('..')

from utils.parse_date import parse_date
from utils.dollar_sales_quote import get_cambio_util
```

---

## ⚠️ Decisões técnicas relevantes

- **Outliers:** identificados pelo método IQR — mais robusto para dados assimétricos como vendas. Decisão de remover ou manter depende de validação com o time de negócio
- **Formato de datas:** dois padrões coexistentes no dataset — padronização obrigatória antes de qualquer análise temporal
- **Câmbio:** cacheado por data única para evitar 9.895 chamadas à API — apenas as datas únicas são consultadas
- **Custo vigente:** utilizado o último `usd_price` com `start_date ≤ sale_date` — sem interpolação entre datas
- **Data leakage:** `shift(1)` aplicado antes do `rolling` na média móvel — garante que nenhum dado futuro entra no treino
- **Matriz de recomendação:** binária (presença/ausência) — quantidade ignorada para focar no padrão de co-ocorrência
- **SQL:** queries escritas para PostgreSQL com CTEs para maior legibilidade e auditabilidade

---

## 📊 Visualizações geradas

| Gráfico                            | Descrição                                     |
| ---------------------------------- | --------------------------------------------- |
| `prejuizo_por_produto.png`         | Top 20 produtos com maior prejuízo total      |
| `percentual_perda_por_produto.png` | Top 20 produtos com maior percentual de perda |
| `top10_ticket_medio.png`           | Top 10 clientes fiéis por ticket médio        |
| `top10_faturamento_total.png`      | Top 10 clientes por faturamento acumulado     |
| `categorias_grupo_elite.png`       | Categorias dominantes do grupo elite          |
| `media_vendas_dia_semana.png`      | Média de vendas por dia da semana (com zeros) |
| `comparativo_media_vendas.png`     | Comparativo com e sem dias de zero venda      |
| `previsao_demanda.png`             | Previsão vs real — Janeiro 2024               |

---

_Projeto desenvolvido como parte do Desafio Lighthouse — Indicium Data & AI_
