"""Síntese dos textos públicos coletados para o painel final."""

from climasaude.llm import resumir_texto


def _agrupar_textos(textos: list[str], limite: int = 2800) -> list[str]:
    """Agrupa os trechos sem descartar conteúdo quando passam do limite."""
    blocos = []
    atual = ""
    for item in textos:
        texto = " ".join(item.split())
        while texto:
            espaco = limite - len(atual) - (1 if atual else 0)
            if espaco < 100:
                blocos.append(atual)
                atual = ""
                continue
            if len(texto) <= espaco:
                atual = f"{atual}\n{texto}" if atual else texto
                break
            corte = texto.rfind(" ", 0, espaco + 1)
            if corte < 100:
                corte = espaco
            parte, texto = texto[:corte].strip(), texto[corte:].strip()
            atual = f"{atual}\n{parte}" if atual else parte
            blocos.append(atual)
            atual = ""
    if atual:
        blocos.append(atual)
    return blocos


def gerar_sintese(textos: list[str], contexto: str) -> tuple[str, int]:
    """Resume todos os trechos coletados e contextualiza com a previsão climática."""
    validos = [texto.strip() for texto in textos if texto.strip()]
    if not validos:
        raise ValueError("Não há textos para resumir")

    blocos = _agrupar_textos(validos)
    notas = [resumir_texto(bloco) for bloco in blocos]
    if not all(notas):
        raise ValueError("O modelo não conseguiu resumir todos os blocos")

    # Consolida os resumos parciais, inclusive quando há muitos blocos.
    for _ in range(4):
        conjunto = "\n".join(notas)
        if len(conjunto) <= 2800:
            break
        notas = [resumir_texto(bloco) for bloco in _agrupar_textos(notas)]
        if not all(notas):
            raise ValueError("Falha ao consolidar resumos")
    else:
        raise ValueError("Os resumos não couberam no contexto do modelo")

    instrucao = (
        "Elabore uma síntese curta, em português, usando somente os dados abaixo. "
        "Em até três tópicos, apresente: (1) a previsão climática informada; "
        "(2) o que as fontes públicas dizem sobre calor e saúde; "
        "(3) uma conclusão educativa conectando os dois temas. "
        "Não crie alertas oficiais, limites de risco, números ou recomendações "
        "que não apareçam nos dados. Não apresente diagnóstico médico.\n\n"
        f"PREVISÃO OPEN-METEO:\n{contexto}\n\n"
        f"RESUMOS DAS FONTES:\n{conjunto}"
    )
    resultado = resumir_texto(instrucao)
    if not resultado:
        raise ValueError("O modelo retornou síntese vazia")
    return resultado, len(blocos)
