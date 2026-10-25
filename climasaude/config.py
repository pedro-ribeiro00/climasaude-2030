"""Configuracoes e catalogos usados pela API e pelo Streamlit."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Cidade:
    id: str
    nome: str
    latitude: float
    longitude: float


CIDADES = {
    cidade.id: cidade
    for cidade in (
        Cidade("sao-paulo", "Sao Paulo - SP", -23.5505, -46.6333),
        Cidade("rio-de-janeiro", "Rio de Janeiro - RJ", -22.9068, -43.1729),
        Cidade("belo-horizonte", "Belo Horizonte - MG", -19.9167, -43.9345),
        Cidade("brasilia", "Brasilia - DF", -15.7939, -47.8828),
        Cidade("porto-alegre", "Porto Alegre - RS", -30.0346, -51.2177),
    )
}

API_URL = os.getenv("CLIMASAUDE_API_URL", "http://127.0.0.1:8000").rstrip("/")
