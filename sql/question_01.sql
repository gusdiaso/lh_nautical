SELECT
COUNT(*) as total_linhas,
(SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'vendas') AS total_colunas,
MIN(sale_date) AS data_minima,
MAX(sale_date) AS data_maxima,
MIN(total) AS valor_minimo,
MAX(total) AS valor_maximo,
ROUND(AVG(total)::numeric, 2) AS valor_medio
FROM vendas;