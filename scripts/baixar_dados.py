from pathlib import Path
import pandas as pd
import requests

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": -23.5505,
    "longitude": -46.6333,
    "start_date": "2026-10-01",
    "end_date": "2026-10-31",
    "hourly": "temperature_2m,precipitation,wind_speed_10m",
    "timezone": "America/Sao_Paulo",
}

resposta = requests.get(url, params=params, timeout=30)
resposta.raise_for_status()
dados_json = resposta.json()

df = pd.DataFrame(dados_json["hourly"])
df = df.rename(columns={
    "time": "data_hora",
    "temperature_2m": "temperatura_c",
    "precipitation": "chuva_mm",
    "wind_speed_10m": "vento_kmh",
})

caminho_saida = Path("dados/bruto/clima_sp_out_2026.csv")
df.to_csv(caminho_saida, index=False, encoding="utf-8")

print(f"Salvo em {caminho_saida} com {len(df)} linhas.")
print(df.head())