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

| Arquivo                  | Tipo | Descrição                                            |
| ------------------------ | ---- | ---------------------------------------------------- |
| `vendas_2023_2024.csv`   | CSV  | Histórico de vendas de 2023 a 2024                   |
| `produtos_raw.csv`       | CSV  | Catálogo de produtos com preços e categorias         |
| `clientes_crm.json`      | JSON | Base de clientes com nome, email e localização       |
| `custos_importacao.json` | JSON | Histórico de custos de importação em USD por produto |

---

## 🔬 Frentes de Análise

### 1. EDA — Análise Exploratória

- Visão geral do dataset (linhas, colunas, intervalo de datas)
- Estatísticas descritivas
- Identificação de outliers pelo método IQR
- Diagnóstico de qualidade dos dados

**Principais achados em vendas_2023_2024.csv**

- 9.895 registros | 6 colunas | período: 01/01/2023 a 31/12/2024
- Coluna `sale_date` com dois formatos misturados (`YYYY-MM-DD` e `DD-MM-YYYY`)
- 1.018 outliers (10,29%) acima de R$ 813.028 na coluna `total`
- Nenhum valor nulo encontrado

---

### 2. Tratamento de Dados

**`produtos_raw.csv`**

- Padronização de `actual_category`: 39 variações normalizadas para 3 categorias (`eletrônicos`, `propulsão`, `ancoragem`)
- Conversão de `price`: removido prefixo `R$` e convertido para `float64`
- Remoção de duplicatas: 7 registros removidos pelo campo `code` → 157 para 150 linhas

**`custos_importacao.json`**

- Estrutura aninhada expandida em linhas individuais via `explode` + `json_normalize`
- 150 produtos → 1.260 registros (média de 8,4 entradas por produto)
- `start_date` convertida para `datetime` | `usd_price` convertido para `float`

**`vendas_2023_2024.csv`**

- Padronização de `sale_date`: dois formatos unificados para `YYYY-MM-DD`
- Adicionada coluna `cambio` com a cotação de venda do dólar do dia (API PTAX/BCB)

---

### 3. Dados Públicos — Análise de Prejuízo

Cruzamento entre custos de importação (USD) e vendas (BRL) usando câmbio real do Banco Central para identificar transações vendidas abaixo do custo.

**Metodologia:**

```
custo_total_brl = usd_price_vigente × câmbio_do_dia × qtd
prejuízo = custo_total_brl − total_venda  →  se > 0, houve prejuízo
```

**Resultados:**

| Métrica                        | Valor                     |
| ------------------------------ | ------------------------- |
| Total de transações analisadas | 9.895                     |
| Transações com prejuízo        | 6.179 (62,4%)             |
| Transações sem prejuízo        | 3.716 (37,6%)             |
| Prejuízo total acumulado       | R$ 182.226.478,73         |
| Produto com maior % de perda   | ID 72 — 63,15% da receita |

- Câmbio obtido via API PTAX do Banco Central — média da cotação de venda do dia
- Para feriados e fins de semana: utilizado o câmbio do último dia útil anterior

**Insight:** 62,4% das transações operaram abaixo do custo de importação — indicando um problema sistêmico de precificação, não casos isolados. Com impostos e frete desconsiderados conforme premissa, o prejuízo real operacional pode ser ainda maior. A prioridade imediata deve ser a revisão da política de precificação, especialmente para os produtos com maior percentual de perda.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia            | Uso                                       |
| --------------------- | ----------------------------------------- |
| **Python 3**          | EDA, tratamento, modelos e visualizações  |
| **Pandas**            | Manipulação e análise de dados            |
| **Matplotlib**        | Visualizações e gráficos                  |
| **Requests**          | Consumo da API PTAX do Banco Central      |
| **PostgreSQL**        | Banco de dados e queries SQL              |
| **Docker**            | Ambiente isolado do banco de dados        |
| **VSCode + SQLTools** | Desenvolvimento e consultas SQL           |
| **Jupyter Notebook**  | Desenvolvimento interativo e documentação |

---

## ⚠️ Decisões técnicas relevantes

- **Outliers:** identificados pelo método IQR — mais robusto para dados assimétricos como vendas. Decisão de remover ou manter depende de validação com o time de negócio
- **Formato de datas:** dois padrões coexistentes no dataset — padronização obrigatória antes de qualquer análise temporal
- **Câmbio:** cacheado por data única para evitar 9.895 chamadas à API — apenas as datas únicas são consultadas
- **Custo vigente:** utilizado o último `usd_price` com `start_date ≤ sale_date` — sem interpolação entre datas
- **SQL:** queries escritas para PostgreSQL com CTE para maior legibilidade e auditabilidade

---

_Projeto desenvolvido como parte do Desafio Lighthouse — Indicium Data & AI_
