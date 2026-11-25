import json
from pathlib import Path
import duckdb
import pandas as pd

ARQUIVO_JSON = Path("dados/bruto/open_meteo_sp_2026_10.json")
PASTA_TRATADO = Path("dados/tratado")
ARQUIVO_CSV_TRATADO = PASTA_TRATADO / "clima_sp_2026_10_tratado.csv"
ARQUIVO_DUCKDB = Path("dados/clima_sp.duckdb")
TABELA_PRINCIPAL = "clima_sp_outubro"


def carregar_e_tratar_dados(caminho_json: Path) -> pd.DataFrame:
    if not caminho_json.exists():
        raise FileNotFoundError(
            f"Arquivo JSON original não encontrado em '{caminho_json}'. Execute coleta.py antes."
        )

    with open(caminho_json, "r", encoding="utf-8") as f:
        raw = json.load(f)

    hourly = raw.get("hourly", {})
    df = pd.DataFrame(
        {
            "data_hora_str": hourly.get("time", []),
            "temperatura_c": hourly.get("temperature_2m", []),
            "precipitacao_mm": hourly.get("precipitation", []),
            "vento_kmh": hourly.get("wind_speed_10m", []),
        }
    )

    # Conversão e validação de datas e tipos numéricos
    df["data_hora"] = pd.to_datetime(df["data_hora_str"], errors="coerce")
    for col in ["temperatura_c", "precipitacao_mm", "vento_kmh"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    nulos_antes = df[["data_hora", "temperatura_c", "precipitacao_mm", "vento_kmh"]].isna().sum().to_dict()

    # Remove linhas sem timestamp válido
    df = df.dropna(subset=["data_hora"]).copy()

    # Ordena e remove duplicidades exatas por data_hora (mantém a primeira ocorrência)
    df = df.sort_values("data_hora").drop_duplicates(subset=["data_hora"], keep="first")

    # Validação de inconsistências físicas básicas (ex.: chuva negativa)
    inconsistentes_chuva = int((df["precipitacao_mm"] < 0).sum())
    if inconsistentes_chuva > 0:
        df.loc[df["precipitacao_mm"] < 0, "precipitacao_mm"] = pd.NA

    df["data"] = df["data_hora"].dt.date
    df["hora"] = df["data_hora"].dt.hour
    df["localidade"] = "São Paulo - SP"

    df_final = df[
        [
            "data_hora",
            "data",
            "hora",
            "localidade",
            "temperatura_c",
            "precipitacao_mm",
            "vento_kmh",
        ]
    ].reset_index(drop=True)

    print("Validação de nulos (antes da limpeza):", nulos_antes)
    print("Inconsistências de chuva negativa encontradas:", inconsistentes_chuva)
    print("Total de registros únicos válidos:", len(df_final))
    print("Cobertura de datas:", df_final["data"].min(), "até", df_final["data"].max())

    return df_final


def salvar_no_duckdb(df: pd.DataFrame, caminho_db: Path, tabela: str) -> None:
    caminho_db.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(caminho_db))
    try:
        con.register("df_tratado", df)
        # Garante idempotência: reexecutar banco.py não duplica registros
        con.execute(
            f"""
            CREATE OR REPLACE TABLE {tabela} AS
            SELECT
                CAST(data_hora AS TIMESTAMP) AS data_hora,
                CAST(data AS DATE) AS data,
                CAST(hora AS INTEGER) AS hora,
                CAST(localidade AS VARCHAR) AS localidade,
                CAST(temperatura_c AS DOUBLE) AS temperatura_c,
                CAST(precipitacao_mm AS DOUBLE) AS precipitacao_mm,
                CAST(vento_kmh AS DOUBLE) AS vento_kmh
            FROM df_tratado
            ORDER BY data_hora;
            """
        )
        total_db = con.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
        print(f"Tabela '{tabela}' atualizada em '{caminho_db}'. Linhas na tabela: {total_db}")
    finally:
        con.close()


def main() -> None:
    PASTA_TRATADO.mkdir(parents=True, exist_ok=True)
    df_tratado = carregar_e_tratar_dados(ARQUIVO_JSON)
    df_tratado.to_csv(ARQUIVO_CSV_TRATADO, index=False, encoding="utf-8")
    salvar_no_duckdb(df_tratado, ARQUIVO_DUCKDB, TABELA_PRINCIPAL)


if __name__ == "__main__":
    main()