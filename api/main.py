"""FastAPI que fornece clima e analise textual para a interface Streamlit."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

from climasaude.analysis import analisar_textos
from climasaude.config import CIDADES
from climasaude.weather import obter_previsao


app = FastAPI(
    title="ClimaSaude 2030 API",
    description="API de apoio ao monitoramento de clima, calor e saude.",
    version="3.0.0",
)


class AnaliseTextoEntrada(BaseModel):
    textos: list[str] = Field(min_length=1, max_length=500)
    limite: int = Field(default=12, ge=1, le=50)


@app.get("/health", tags=["servico"])
def health_check() -> dict:
    return {"status": "ok", "versao": app.version}


@app.get("/cidades", tags=["clima"])
def listar_cidades() -> list[dict]:
    return [
        {
            "id": cidade.id,
            "nome": cidade.nome,
            "latitude": cidade.latitude,
            "longitude": cidade.longitude,
        }
        for cidade in CIDADES.values()
    ]


@app.get("/previsao/{cidade_id}", tags=["clima"])
def consultar_previsao(cidade_id: str) -> dict:
    cidade = CIDADES.get(cidade_id)
    if cidade is None:
        raise HTTPException(status_code=404, detail="Cidade nao cadastrada")

    try:
        return obter_previsao(cidade)
    except (requests.RequestException, KeyError, IndexError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="A fonte climatica externa nao respondeu corretamente",
        ) from exc


@app.post("/analises/texto", tags=["analise"])
def criar_analise_textual(entrada: AnaliseTextoEntrada) -> dict:
    """Analisa textos enviados no corpo JSON e devolve metricas agregadas."""
    return analisar_textos(entrada.textos, entrada.limite)
