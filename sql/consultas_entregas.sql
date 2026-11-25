-- 1. Indicadores gerais do período (KPIs de síntese)
-- Pergunta: Qual o panorama geral de chuva, temperatura e vento para planejar a rotina?
SELECT
    COUNT(*) AS total_registros_horarios,
    COUNT(DISTINCT data) AS total_dias_cobertos,
    ROUND(SUM(precipitacao_mm), 1) AS chuva_acumulada_mm,
    ROUND(AVG(temperatura_c), 1) AS temp_media_c,
    ROUND(MIN(temperatura_c), 1) AS temp_min_c,
    ROUND(MAX(temperatura_c), 1) AS temp_max_c,
    ROUND(MAX(vento_kmh), 1) AS vento_max_kmh
FROM clima_sp_outubro;

-- 2. Chuva e temperatura por hora do dia
-- Pergunta: Em quais horários do dia há maior concentração de chuva e maior frequência de horas chuvosas?
SELECT
    hora,
    ROUND(SUM(precipitacao_mm), 1) AS chuva_total_mm,
    COUNT(*) FILTER (WHERE precipitacao_mm > 0) AS horas_com_chuva,
    ROUND(AVG(temperatura_c), 1) AS temp_media_c
FROM clima_sp_outubro
GROUP BY hora
ORDER BY hora;

-- 3. Dias com maior acumulado de chuva e extremos térmicos
-- Pergunta: Quais dias concentraram maior volume de chuva e maiores amplitudes/extremos de temperatura?
SELECT
    data,
    ROUND(SUM(precipitacao_mm), 1) AS chuva_dia_mm,
    ROUND(MIN(temperatura_c), 1) AS temp_min_c,
    ROUND(MAX(temperatura_c), 1) AS temp_max_c,
    ROUND(MAX(vento_kmh), 1) AS vento_max_kmh
FROM clima_sp_outubro
GROUP BY data
ORDER BY chuva_dia_mm DESC, data ASC
LIMIT 10;