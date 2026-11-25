-- 1. Chuva acumulada e quantidade de horas com chuva por hora do dia (0 a 23)
SELECT
    hora,
    ROUND(SUM(chuva_mm), 1) AS chuva_total_mm,
    COUNT(*) FILTER (WHERE chuva_mm > 0) AS horas_com_chuva,
    ROUND(AVG(temperatura_c), 1) AS temp_media_c
FROM clima_outubro
GROUP BY hora
ORDER BY hora;

-- 2. Dias com maior volume de chuva no mês
SELECT
    data,
    ROUND(SUM(chuva_mm), 1) AS chuva_dia_mm,
    MIN(temperatura_c) AS temp_min_c,
    MAX(temperatura_c) AS temp_max_c
FROM clima_outubro
GROUP BY data
HAVING SUM(chuva_mm) > 0
ORDER BY chuva_dia_mm DESC
LIMIT 10;