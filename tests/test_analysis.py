from climasaude.analysis import analisar_textos


def test_analisar_textos_remove_stopwords_e_respeita_limite():
    resultado = analisar_textos(
        ["Calor extremo exige cuidado", "Calor e saude exigem cuidado"],
        limite=2,
    )

    assert resultado["total_textos"] == 2
    assert resultado["total_palavras"] == 9
    assert resultado["palavras_frequentes"] == [
        {"palavra": "calor", "frequencia": 2},
        {"palavra": "cuidado", "frequencia": 2},
    ]


def test_analisar_textos_ignora_valores_vazios():
    resultado = analisar_textos(["", "   ", "Temperatura elevada"])

    assert resultado["total_textos"] == 1
    assert resultado["total_palavras"] == 2
