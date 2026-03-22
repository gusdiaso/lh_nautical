WITH custo_por_transacao AS (
    SELECT
        v.id_product,
        v.total                                          AS receita,
        (c.usd_price * v.cambio * v.qtd)                AS custo_total_brl,
        (c.usd_price * v.cambio * v.qtd) - v.total      AS prejuizo
    FROM vendas_processed v
    -- Pega o custo vigente na data da venda (último start_date <= sale_date)
    JOIN custos_importacao_processed c
        ON c.product_id = v.id_product
        AND c.start_date = (
            SELECT MAX(start_date)
            FROM custos_importacao_processed
            WHERE product_id = v.id_product
            AND start_date <= v.sale_date
        )
)

SELECT
    id_product,
    ROUND(SUM(receita)::numeric, 2)                                         AS receita_total,
    ROUND(SUM(CASE WHEN prejuizo > 0 THEN prejuizo ELSE 0 END)::numeric, 2) AS prejuizo_total,
    ROUND(
        (SUM(CASE WHEN prejuizo > 0 THEN prejuizo ELSE 0 END) / 
         NULLIF(SUM(receita), 0) * 100)::numeric, 2
    )                                                                        AS percentual_perda
FROM custo_por_transacao
GROUP BY id_product
HAVING SUM(CASE WHEN prejuizo > 0 THEN prejuizo ELSE 0 END) > 0
ORDER BY prejuizo_total DESC;