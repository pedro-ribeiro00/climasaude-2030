from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_check():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_lista_cidades():
    resposta = client.get("/cidades")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 5
    assert resposta.json()[0]["id"] == "sao-paulo"


def test_previsao_rejeita_cidade_desconhecida():
    resposta = client.get("/previsao/cidade-inexistente")

    assert resposta.status_code == 404


def test_previsao_repassa_dados_normalizados(monkeypatch):
    previsao = {
        "cidade_id": "sao-paulo",
        "cidade": "Sao Paulo - SP",
        "gerado_em_utc": "2026-01-01T00:00:00+00:00",
        "previsao": [],
    }
    monkeypatch.setattr("api.main.obter_previsao", lambda cidade: previsao)

    resposta = client.get("/previsao/sao-paulo")

    assert resposta.status_code == 200
    assert resposta.json() == previsao


def test_post_analise_textual():
    resposta = client.post(
        "/analises/texto",
        json={"textos": ["calor extremo", "calor intenso"], "limite": 3},
    )

    assert resposta.status_code == 200
    assert resposta.json()["total_textos"] == 2
    assert resposta.json()["palavras_frequentes"][0] == {
        "palavra": "calor",
        "frequencia": 2,
    }


def test_post_analise_exige_textos():
    resposta = client.post("/analises/texto", json={"textos": []})

    assert resposta.status_code == 422
