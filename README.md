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

## 🛠️ Tecnologias utilizadas

| Tecnologia               | Uso                                      |
| ------------------------ | ---------------------------------------- |
| **Python**               | EDA, tratamento, modelos e visualizações |
| **Pandas**               | Manipulação e análise de dados           |
| **Matplotlib / Seaborn** | Visualizações                            |
| **PostgreSQL**           | Banco de dados e queries SQL             |
| **Docker**               | Ambiente do banco de dados               |
| **VSCode + SQLTools**    | Desenvolvimento e consultas SQL          |

---

_Projeto desenvolvido como parte do Desafio Lighthouse — Indicium Data & AI_
