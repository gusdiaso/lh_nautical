
-- Top 10 clientes fiéis

WITH metricas_clientes AS (
    SELECT
        v.id_client,
        SUM(v.total)                        AS faturamento_total,
        COUNT(v.id)                         AS frequencia,
        SUM(v.total) / COUNT(v.id)          AS ticket_medio,
        COUNT(DISTINCT p.actual_category)   AS diversidade_categorias
    FROM vendas_processed v
    JOIN produtos_processed p
        ON p.code = v.id_product
    GROUP BY v.id_client
),
clientes_elite AS (
    SELECT *
    FROM metricas_clientes
    WHERE diversidade_categorias >= 3
    ORDER BY ticket_medio DESC, id_client ASC
    LIMIT 10
)
SELECT
    e.id_client,
    cl.full_name,
    cl.cidade,
    cl.estado,
    ROUND(e.faturamento_total::numeric, 2)  AS faturamento_total,
    e.frequencia,
    ROUND(e.ticket_medio::numeric, 2)       AS ticket_medio,
    e.diversidade_categorias
FROM clientes_elite e
JOIN clientes_crm_processed cl
    ON cl.code = e.id_client
ORDER BY ticket_medio DESC, id_client ASC;

-- Categoria dominante do grupo elite

WITH metricas_clientes AS (
    SELECT
        v.id_client,
        SUM(v.total)                        AS faturamento_total,
        COUNT(v.id)                         AS frequencia,
        SUM(v.total) / COUNT(v.id)          AS ticket_medio,
        COUNT(DISTINCT p.actual_category)   AS diversidade_categorias
    FROM vendas_processed v
    JOIN produtos_processed p
        ON p.code = v.id_product
    GROUP BY v.id_client
),
clientes_elite AS (
    SELECT *
    FROM metricas_clientes
    WHERE diversidade_categorias >= 3
    ORDER BY ticket_medio DESC, id_client ASC
    LIMIT 10
)
SELECT
    p.actual_category,
    SUM(v.qtd) AS total_itens
FROM vendas_processed v
JOIN produtos_processed p
    ON p.code = v.id_product
WHERE v.id_client IN (SELECT id_client FROM clientes_elite)
GROUP BY p.actual_category
ORDER BY total_itens DESC
LIMIT 1;