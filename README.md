# Observatório Climático Local — São Paulo (Outubro/2026)

Projeto de extensão voltado à análise de dados meteorológicos históricos de São Paulo para apoiar entregadores de aplicativo na leitura de horários e dias com maior incidência de chuva, variações térmicas e vento.

## Objetivo e público-alvo
- **Objetivo:** coletar, tratar, armazenar em DuckDB e consultar dados climáticos horários de outubro de 2026 para gerar indicadores práticos sobre as condições na rua.
- **Público-alvo:** entregadores de aplicativo que atuam em São Paulo e dependem das condições de tempo e trânsito para planejar turnos e cuidados de segurança.

## Fonte, localidade, período e variáveis
- **Fonte:** API histórica Open-Meteo (`https://archive-api.open-meteo.com/v1/archive`).
- **Localidade:** São Paulo - SP (coordenadas aproximadas `-23.5505` de latitude e `-46.6333` de longitude; fuso `America/Sao_Paulo`).
- **Período:** 1º a 31 de outubro de 2026 (31 dias consecutivos / 744 registros horários).
- **Variáveis:** temperatura do ar a 2 m (`temperatura_c`), precipitação (`precipitacao_mm`) e velocidade máxima/de referência do vento a 10 m (`vento_kmh`).

## Estrutura dos arquivos
- `coleta.py`: faz a requisição à Open-Meteo e salva o JSON bruto original e os metadados da coleta em `dados/bruto/`.
- `banco.py`: lê o JSON, valida e padroniza os dados com `pandas`, salva o CSV tratado em `dados/tratado/` e carrega a tabela `clima_sp_outubro` no banco `dados/clima_sp.duckdb` sem duplicar linhas.
- `consultas.sql`: consultas SQL para indicadores gerais, distribuição por hora do dia e dias com maior chuva e extremos de temperatura.
- `requirements.txt`: bibliotecas Python necessárias para rodar o projeto.
- `.gitignore`: evita versionar ambiente virtual, arquivos temporários e dados sensíveis.
- `docs/escopo-1/AE2/`: pasta sugerida para armazenar o relatório da atividade.