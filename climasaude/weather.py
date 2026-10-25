"""Acesso aos dados climaticos da Open-Meteo."""

from datetime import datetime, timezone

import requests

from climasaude.config import Cidade


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def obter_previsao(cidade: Cidade) -> dict:
    """Consulta a Open-Meteo e normaliza a previsao de sete dias."""
    parametros = {
        "latitude": cidade.latitude,
        "longitude": cidade.longitude,
        "daily": (
            "temperature_2m_max,apparent_temperature_max,"
            "uv_index_max,precipitation_sum"
        ),
        "timezone": "America/Sao_Paulo",
        "forecast_days": 7,
    }
    resposta = requests.get(OPEN_METEO_URL, params=parametros, timeout=20)
    resposta.raise_for_status()
    diario = resposta.json()["daily"]

    previsao = [
        {
            "data": diario["time"][indice],
            "temperatura_max_c": diario["temperature_2m_max"][indice],
            "sensacao_max_c": diario["apparent_temperature_max"][indice],
            "uv_max": diario["uv_index_max"][indice],
            "precipitacao_mm": diario["precipitation_sum"][indice],
        }
        for indice in range(len(diario["time"]))
    ]

    return {
        "cidade_id": cidade.id,
        "cidade": cidade.nome,
        "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
        "previsao": previsao,
    }
