import json
from datetime import datetime
from pathlib import Path
import requests

# Recorte do projeto: São Paulo (SP), 30+ dias de outubro/2026
LOCALIDADE = "São Paulo - SP"
LATITUDE = -23.5505
LONGITUDE = -46.6333
DATA_INICIO = "2026-10-01"
DATA_FIM = "2026-10-31"
TIMEZONE = "America/Sao_Paulo"
VARIAVEIS_HORARIAS = [
    "temperature_2m",
    "precipitation",
    "wind_speed_10m",
]

URL_OPEN_METEO = "https://archive-api.open-meteo.com/v1/archive"

PASTA_BRUTO = Path("dados/bruto")
ARQUIVO_JSON = PASTA_BRUTO / "open_meteo_sp_2026_10.json"
ARQUIVO_METADADOS = PASTA_BRUTO / "metadados_coleta.json"


def coletar_dados_open_meteo() -> dict:
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": DATA_INICIO,
        "end_date": DATA_FIM,
        "hourly": ",".join(VARIAVEIS_HORARIAS),
        "timezone": TIMEZONE,
    }
    response = requests.get(URL_OPEN_METEO, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def main() -> None:
    PASTA_BRUTO.mkdir(parents=True, exist_ok=True)
    data_coleta = datetime.now().isoformat(timespec="seconds")

    payload = coletar_dados_open_meteo()

    # Preserva exatamente a resposta original em JSON
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    metadados = {
        "fonte": "Open-Meteo Historical Weather API",
        "url_base": URL_OPEN_METEO,
        "localidade": LOCALIDADE,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "periodo_inicio": DATA_INICIO,
        "periodo_fim": DATA_FIM,
        "timezone": TIMEZONE,
        "variaveis_horarias": VARIAVEIS_HORARIAS,
        "data_hora_coleta_local": data_coleta,
        "arquivo_json_preservado": str(ARQUIVO_JSON),
    }

    with open(ARQUIVO_METADADOS, "w", encoding="utf-8") as f:
        json.dump(metadados, f, ensure_ascii=False, indent=2)

    total_horas = len(payload.get("hourly", {}).get("time", []))
    print(f"Coleta concluída em {data_coleta}. Registros horários: {total_horas}")
    print(f"JSON original salvo em: {ARQUIVO_JSON}")


if __name__ == "__main__":
    main()