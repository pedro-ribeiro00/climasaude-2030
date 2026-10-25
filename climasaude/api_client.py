"""Cliente HTTP usado pelo Streamlit para consumir a FastAPI do projeto."""

import requests

from climasaude.config import API_URL


class APIIndisponivel(RuntimeError):
    """Indica que a interface nao conseguiu consultar a API local."""


def _mensagem_erro(exc: Exception) -> str:
    return (
        f"Nao foi possivel acessar a API em {API_URL}: {exc}. "
        "Inicie-a com `uvicorn api.main:app --reload`."
    )


def obter_previsao_api(cidade_id: str) -> dict:
    try:
        resposta = requests.get(f"{API_URL}/previsao/{cidade_id}", timeout=25)
        resposta.raise_for_status()
        return resposta.json()
    except (requests.RequestException, ValueError) as exc:
        raise APIIndisponivel(_mensagem_erro(exc)) from exc


def analisar_textos_api(textos: list[str], limite: int = 12) -> dict:
    try:
        resposta = requests.post(
            f"{API_URL}/analises/texto",
            json={"textos": textos, "limite": limite},
            timeout=20,
        )
        resposta.raise_for_status()
        return resposta.json()
    except (requests.RequestException, ValueError) as exc:
        raise APIIndisponivel(_mensagem_erro(exc)) from exc
