"""Funcoes puras para limpeza e analise exploratoria de texto."""

from collections import Counter
import re


STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "entre", "é", "essa", "esse", "esta", "este", "foi", "mais",
    "na", "nas", "no", "nos", "o", "os", "ou", "para", "pela", "pelas",
    "pelo", "pelos", "por", "que", "se", "sem", "ser", "sua", "suas", "um",
    "uma", "the", "and", "of", "to", "in", "is", "are", "for", "on", "with",
    "from", "by", "can", "be", "an", "at", "or", "that", "this",
}


def analisar_textos(textos: list[str], limite: int = 12) -> dict:
    """Retorna estatisticas deterministicas, reutilizaveis pela API e por testes."""
    textos_limpos = [str(texto).strip() for texto in textos if str(texto).strip()]
    palavras = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", " ".join(textos_limpos).lower())
    frequencias = Counter(p for p in palavras if p not in STOPWORDS)

    return {
        "total_textos": len(textos_limpos),
        "total_palavras": sum(len(texto.split()) for texto in textos_limpos),
        "palavras_frequentes": [
            {"palavra": palavra, "frequencia": frequencia}
            for palavra, frequencia in frequencias.most_common(limite)
        ],
    }
