## Questao 1.1

SELECT
COUNT(_) as total_linhas,
(SELECT COUNT(_) FROM information_schema.columns WHERE table_name = 'vendas') AS total_colunas,
MIN(sale_date) AS data_minima,
MAX(sale_date) AS data_maxima,
MIN(total) AS valor_minimo,
MAX(total) AS valor_maximo,
ROUND(AVG(total)::numeric, 2) AS valor_medio
FROM vendas;

## Questao 1.2

2222973

## Questao 1.3

Diagnóstico de Confiabilidade — vendas_2023_2024.csv

Outliers: Pelo método IQR, 1.018 registros (10,29%) estão acima de R$ 813.028, com o valores aparecendo repetidas vezes, o que é suspeito e exige verificação com o time de negócio antes de qualquer tratamento.

Qualidade dos dados: Nenhum valor nulo foi encontrado, ponto positivo. Porém, a coluna sale_date mistura dois formatos (YYYY-MM-DD e DD-MM-YYYY), o que pode corromper análises temporais silenciosamente.

Não pronto para análises. Exige dois tratamentos prévios: padronização do formato de datas e investigação dos outliers.

Recomendo uma conversa antes de qualquer ajuste nos outliers, os valores repetidos podem ser um contrato corporativo legítimo ou um erro de importação. Só o time de negócio pode confirmar.
