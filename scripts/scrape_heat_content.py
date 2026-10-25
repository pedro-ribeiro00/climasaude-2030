import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


FONTES = [
    {
        "fonte": "Ministerio da Saude",
        "url": "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/o/ondas-de-calor",
        "idioma": "pt-BR",
    },
    {
        "fonte": "World Health Organization",
        "url": "https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health",
        "idioma": "en",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
    )
}


def extrair_conteudo(fonte: str, url: str, idioma: str) -> list[dict]:
    """Baixa uma pagina publica e extrai blocos textuais com Beautiful Soup."""
    resposta = requests.get(url, timeout=30, headers=HEADERS)
    resposta.raise_for_status()
    resposta.encoding = resposta.apparent_encoding or resposta.encoding

    soup = BeautifulSoup(resposta.text, "html.parser")

    # Remove elementos que normalmente nao fazem parte do conteudo principal.
    for tag in soup(["script", "style", "nav", "footer", "noscript", "svg"]):
        tag.decompose()

    area_principal = (
        soup.select_one("main article")
        or soup.find("article")
        or soup.find("main")
        or soup.body
        or soup
    )
    titulo_pagina = soup.title.get_text(" ", strip=True) if soup.title else ""
    coletado_em = datetime.now(timezone.utc).isoformat()

    registros = []
    vistos = set()

    for elemento in area_principal.find_all(["h1", "h2", "h3", "p", "li"]):
        texto = " ".join(elemento.get_text(" ", strip=True).split())

        # Evita fragmentos vazios, muito pequenos e duplicados.
        if len(texto) < 35 or texto in vistos:
            continue

        vistos.add(texto)
        registros.append(
            {
                "fonte": fonte,
                "titulo_pagina": titulo_pagina,
                "url": url,
                "tipo_elemento": elemento.name,
                "texto": texto,
                "idioma": idioma,
                "hash_conteudo": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
                "coletado_em_utc": coletado_em,
            }
        )

    return registros


def main() -> None:
    todos_registros = []
    falhas = []

    for item in FONTES:
        print(f"Coletando: {item['fonte']}")
        try:
            registros = extrair_conteudo(item["fonte"], item["url"], item["idioma"])
            print(f"  {len(registros)} blocos textuais coletados")
            todos_registros.extend(registros)
        except requests.RequestException as exc:
            falhas.append(f"{item['fonte']}: {exc}")
            print(f"  Falha na coleta: {exc}")

    if not todos_registros:
        print("\nNenhuma fonte foi coletada. Verifique sua conexao com a internet.")
        sys.exit(1)

    df = pd.DataFrame(todos_registros).drop_duplicates(
        subset=["fonte", "hash_conteudo"]
    )

    pasta_saida = Path("data/raw")
    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho_csv = pasta_saida / "conteudo_calor_saude.csv"
    caminho_txt = pasta_saida / "conteudo_calor_saude.txt"

    df.to_csv(caminho_csv, index=False, encoding="utf-8")

    texto_completo = "\n\n".join(
        f"[{row.fonte}] {row.texto}" for row in df.itertuples(index=False)
    )
    caminho_txt.write_text(texto_completo, encoding="utf-8")

    print("\nColeta concluida.")
    print(f"Total: {len(df)} registros")
    print(f"CSV: {caminho_csv}")
    print(f"TXT: {caminho_txt}")

    if falhas:
        print("\nAvisos: uma ou mais fontes falharam, mas os dados disponiveis foram salvos.")
        for falha in falhas:
            print(f"- {falha}")


if __name__ == "__main__":
    main()
