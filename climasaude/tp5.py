"""Síntese extrativa: seleção pelo Qwen e preservação dos textos originais."""

from climasaude.llm import carregar_modelo, dividir_texto, selecionar_trecho


def _agrupar_trechos(textos: list[str], limite: int) -> list[list[str]]:
    tokenizer, _ = carregar_modelo()
    grupos, atual = [], []
    for texto in textos:
        # Mesmo um parágrafo muito grande é dividido, sem truncamento.
        for parte in dividir_texto(texto, limite=limite - 20):
            candidato = atual + [parte]
            enumerado = "\n".join(f"{i}: {t}" for i, t in enumerate(candidato, 1))
            if atual and len(tokenizer.encode(enumerado, add_special_tokens=False)) > limite:
                grupos.append(atual)
                atual = []
            atual.append(parte)
    if atual:
        grupos.append(atual)
    return grupos


def gerar_sintese(textos: list[str], contexto: str) -> tuple[str, int]:
    """Processa todos os textos; o LLM seleciona evidências, sem reescrevê-las.

    A previsão é reproduzida do contexto recebido, não estimada pelo modelo.
    Os trechos mantêm o idioma da fonte. Não há resposta simulada ou fallback.
    """
    validos = [texto.strip() for texto in textos if texto.strip()]
    if not validos or not contexto.strip():
        raise ValueError("Não há textos ou contexto para resumir")
    tokenizer, _ = carregar_modelo()
    limite = min(1100, 2048 - len(tokenizer.encode(contexto)) - 250)
    if limite < 100:
        raise ValueError("O contexto climático excede o espaço disponível")
    grupos = _agrupar_trechos(validos, limite)
    notas = [selecionar_trecho(grupo, contexto) for grupo in grupos]
    # Seleciona até três evidências entre os candidatos de todos os blocos.
    for _ in range(10):
        if len(notas) <= 3:
            break
        novos_grupos = _agrupar_trechos(notas, limite)
        if len(novos_grupos) == 1:
            candidatos = novos_grupos[0].copy()
            notas = []
            for _ in range(min(3, len(candidatos))):
                escolhido = selecionar_trecho(candidatos, contexto)
                notas.append(escolhido)
                candidatos.remove(escolhido)
            break
        if len(novos_grupos) == len(notas):
            # Não descarta trechos por corte arbitrário: pede uma entrada menor.
            raise ValueError("Trechos selecionados excedem o espaço para consolidação")
        notas = [selecionar_trecho(grupo, contexto) for grupo in novos_grupos]
    else:
        raise ValueError("Falha ao consolidar os trechos")
    resultado = (
        f"**Previsão Open-Meteo (contexto recebido)**\n\n{contexto}\n\n"
        "**Síntese extrativa — trechos selecionados pelo Qwen**\n\n"
        + "\n\n".join(f"- {nota}" for nota in notas)
    )
    return resultado, len(grupos)
