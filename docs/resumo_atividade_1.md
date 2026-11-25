# Resumo da Atividade 1 — Dados Climáticos de São Paulo (Outubro/2026)

## Objetivo
Coletar e analisar os dados meteorológicos de São Paulo referentes a outubro de 2026 para identificar horários e dias críticos de chuva e temperatura, relacionando essas informações com a rotina de entregadores de aplicativo na cidade.

## Etapas realizadas
- **Organização do projeto:** criação da estrutura de pastas em `clima-sp` (`dados`, `scripts`, `sql` e `docs`), além dos arquivos `.gitignore` e `README.md`.
- **Ambiente de trabalho:** configuração do ambiente virtual em Python com os pacotes `duckdb`, `pandas` e `requests`.
- **Coleta de dados:** desenvolvimento do script `baixar_dados.py` para extrair os registros horários de outubro de 2026 (`744` linhas no total), salvando o resultado bruto em `dados/bruto/clima_sp_out_2026.csv`.
- **Tratamento e armazenamento:** criação do script `tratar_dados.py` para padronizar a tabela, separar data e hora e gravar os dados tratados na tabela `clima_outubro` dentro do banco `dados/tratado/clima_sp.duckdb`.
- **Análise em SQL:** elaboração de consultas em `sql/consultas_entregas.sql` para avaliar o comportamento da chuva por faixa de horário e listar os dias com maior acumulado.

## Principais resultados
- **Panorama do mês:** a temperatura variou entre **12,5 °C** e **31,7 °C**, o acumulado total de chuva foi de **241,0 mm** e a rajada máxima de vento chegou a **19,6 km/h**.
- **Distribuição por horário:** o maior volume de chuva concentrou-se no período da tarde, entre **13h e 17h**, com pico às **15h** (**24,4 mm**). Entre **9h e 14h** houve alta frequência de registros de chuva fraca ou garoa (`15` a `23` ocorrências por horário). A partir das **18h**, o volume caiu até às 22h (**5,9 mm** a **8,4 mm**), com leve aumento às 23h (**12,0 mm**).
- **Dias mais críticos:** o dia **25/10** registrou o maior volume (**35,5 mm**), seguido por **11/10** (**23,6 mm**), **16/10** (**21,4 mm**) e **29/10** (**20,2 mm**). O dia **09/10** também chamou atenção pela máxima de **31,7 °C** combinada com **12,5 mm** de chuva.

## Aplicação prática na rotina de entregas
Os dados mostram que a janela entre **13h e 17h** concentra o maior risco de chuva forte, exigindo mais cautela com trânsito lento e piso molhado. Já o início da noite apresenta menor volume acumulado, oferecendo condições mais previsíveis para rodar.