# Observatório Climático Local — São Paulo (`clima-sp`)

Repositório do projeto **Observatório Climático Local**, focado no acompanhamento meteorológico diário de **São Paulo** (coordenadas `-23.5505`, `-46.6333`) para apoiar a análise de condições climáticas e o planejamento de deslocamentos e atividades ao ar livre para o público beneficiário.

## Estágio atual do projeto

O projeto está na **fase pré-implementação da AE2-2**, com o desenho técnico da solução de dados planejado antes da implementação definitiva dos scripts, da carga completa do banco ou da publicação final do dashboard. O recorte definido para esta etapa contempla **30 dias consecutivos** (`2026-10-01` a `2026-10-30`) e **três variáveis meteorológicas diárias** (`temperatura_max_c`, `temperatura_min_c` e `precipitacao_mm`).

As entregas e evidências anteriores permanecem mantidas na estrutura do repositório conforme o escopo do projeto.

## Desenho da solução (AE2-2 — Visão geral)

1. **Fonte de dados:** API histórica **Open-Meteo**.
2. **Coleta e preservação:** requisições em **Python** com `requests`, salvando a resposta original em **JSON** antes de transformações.
3. **Tratamento e validação:** organização, tipagem e verificações de qualidade com **pandas**, mantendo a separação entre valores ausentes e zero real.
4. **Armazenamento e análise:** tabela principal `clima_diario` no **DuckDB** (com unicidade por `cidade` e `data`) e consultas **SQL** para cálculo de indicadores.
5. **Visualização:** painel em **Streamlit** com três indicadores/KPIs, dois gráficos, tabela de registros diários, fonte/unidades e espaço para limitações e explicações ao público.

## Estrutura do repositório

* `README.md` — visão geral, estágio atual e desenho da solução
* `.gitignore` — regras de arquivos ignorados pelo Git
* `dados/` — dados e banco local
* `src/` — códigos-fonte do projeto
* `sql/` — consultas e definições SQL
* `docs/escopo-1/AE1/` — documentação e entregas da AE1
* `docs/escopo-1/AE2-2/` — desenho técnico (com diagrama e wireframe) e registros da AE2-2

## Próximos passos (Issues planejadas)

A implementação futura será organizada em issues no repositório:

* Implementar a coleta pela API histórica Open-Meteo
* Preservar a resposta original em JSON
* Implementar o tratamento e as checagens de qualidade com `pandas`
* Criar a tabela `clima_diario` e a carga no DuckDB
* Implementar as consultas SQL e os indicadores/KPIs
* Construir o dashboard em Streamlit
* Revisar a documentação e preparar a devolutiva