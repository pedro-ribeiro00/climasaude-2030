"""FastAPI que fornece clima e analise textual para a interface Streamlit."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

from climasaude.analysis import analisar_textos
from climasaude.config import CIDADES
from climasaude.weather import obter_previsao
from climasaude.llm import MODEL_ID, carregar_modelo, resumir_texto


app = FastAPI(
    title="ClimaSaude 2030 API",
    description="API de apoio ao monitoramento de clima, calor e saude.",
    version="4.0.0",
)


class AnaliseTextoEntrada(BaseModel):
    textos: list[str] = Field(min_length=1, max_length=500)
    limite: int = Field(default=12, ge=1, le=50)


class StatusResposta(BaseModel):
    status: str
    versao: str


class CidadeResposta(BaseModel):
    id: str
    nome: str
    latitude: float
    longitude: float


class DiaPrevisao(BaseModel):
    data: str
    temperatura_max_c: float | None
    sensacao_max_c: float | None
    uv_max: float | None
    precipitacao_mm: float | None


class PrevisaoResposta(BaseModel):
    cidade_id: str
    cidade: str
    gerado_em_utc: str
    previsao: list[DiaPrevisao]


class Frequencia(BaseModel):
    palavra: str
    frequencia: int


class AnaliseResposta(BaseModel):
    total_textos: int
    total_palavras: int
    palavras_frequentes: list[Frequencia]


class TextoEntrada(BaseModel):
    texto: str = Field(min_length=1, max_length=6000)


class ResumoResposta(BaseModel):
    tipo_analise: str
    texto_original: str
    resultado: str
    modelo: str


@app.get("/health", tags=["servico"], response_model=StatusResposta)
def health_check() -> dict:
    return {"status": "ok", "versao": app.version}


@app.get("/cidades", tags=["clima"], response_model=list[CidadeResposta])
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


@app.get("/previsao/{cidade_id}", tags=["clima"], response_model=PrevisaoResposta)
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


@app.post("/analises/texto", tags=["analise"], response_model=AnaliseResposta)
def criar_analise_textual(entrada: AnaliseTextoEntrada) -> dict:
    """Analisa textos enviados no corpo JSON e devolve metricas agregadas."""
    return analisar_textos(entrada.textos, entrada.limite)


@app.post("/processar_texto", tags=["analise"], response_model=ResumoResposta)
def processar_texto(entrada: TextoEntrada) -> dict:
    texto = entrada.texto.strip()
    if not texto:
        raise HTTPException(status_code=422, detail="Informe um texto que nao esteja vazio.")
    try:
        carregar_modelo()
    except (OSError, ImportError, RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail="Modelo local indisponivel. Instale as dependencias e baixe o modelo conforme o README.") from exc
    try:
        resumo = resumir_texto(texto)
        if not resumo:
            raise ValueError("O modelo retornou uma resposta vazia")
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=500, detail="Nao foi possivel gerar o resumo com o modelo local.") from exc
    return {"tipo_analise": "resumo", "texto_original": texto, "resultado": resumo, "modelo": MODEL_ID}
