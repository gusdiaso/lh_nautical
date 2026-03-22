
WITH intervalo AS (
    SELECT
        MIN(sale_date::date) AS data_min,
        MAX(sale_date::date) AS data_max
    FROM vendas_processed
),
calendario AS (
    SELECT generate_series(
        (SELECT data_min FROM intervalo),
        (SELECT data_max FROM intervalo),
        '1 day'::interval
    )::date AS data
),
dim_calendario AS (
    SELECT
        data,
        EXTRACT(DOW FROM data) AS num_dia_semana,
        CASE EXTRACT(DOW FROM data)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana
    FROM calendario
),
vendas_diarias AS (
    SELECT
        sale_date::date AS data,
        SUM(total) AS total_vendas
    FROM vendas_processed
    GROUP BY sale_date::date
)


SELECT
    d.dia_semana,
    COUNT(d.data) AS total_dias,
    ROUND(AVG(COALESCE(v.total_vendas, 0))::numeric, 2) AS media_vendas
FROM dim_calendario d
LEFT JOIN vendas_diarias v
    ON v.data = d.data
GROUP BY d.dia_semana
ORDER BY ROUND(AVG(COALESCE(v.total_vendas, 0))::numeric, 2);