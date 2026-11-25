from pathlib import Path
import duckdb
import pandas as pd

arquivo_bruto = Path("dados/bruto/clima_sp_out_2026.csv")
df = pd.read_csv(arquivo_bruto)

dt = pd.to_datetime(df["data_hora"])
df["data"] = dt.dt.date.astype(str)
df["hora"] = dt.dt.hour
df["temperatura_c"] = pd.to_numeric(df["temperatura_c"], errors="coerce")
df["chuva_mm"] = pd.to_numeric(df["chuva_mm"], errors="coerce").fillna(0.0)
df["vento_kmh"] = pd.to_numeric(df["vento_kmh"], errors="coerce")

df = df[["data_hora", "data", "hora", "temperatura_c", "chuva_mm", "vento_kmh"]]

csv_tratado = Path("dados/tratado/clima_sp_out_2026_tratado.csv")
df.to_csv(csv_tratado, index=False, encoding="utf-8")

banco_path = Path("dados/tratado/clima_sp.duckdb")
con = duckdb.connect(str(banco_path))
con.execute("CREATE OR REPLACE TABLE clima_outubro AS SELECT * FROM df")
resumo = con.execute("""
    SELECT
        COUNT(*) AS total_registros,
        MIN(temperatura_c) AS temp_min,
        MAX(temperatura_c) AS temp_max,
        ROUND(SUM(chuva_mm), 1) AS chuva_total_mm,
        MAX(vento_kmh) AS vento_max_kmh
    FROM clima_outubro
""").fetchdf()
con.close()

print(f"Tratado salvo em {csv_tratado} e banco em {banco_path}.")
print(resumo.to_string(index=False))