# Validação do TP5 - 23/11/2026

## Testes realizados

Foram registradas **20 verificações HTTP** e **19 interações com AppTest**, com previsões reais da Open-Meteo, textos públicos e o modelo Qwen2.5-0.5B-Instruct local.

A coleta gerou 61 trechos: 13 do Ministério da Saúde e 48 da OMS. As previsões foram consultadas nas cinco cidades disponíveis. O modelo foi executado em três configurações:

| Configuração | Trechos / blocos | Tempo da API |
|---|---:|---:|
| São Paulo + Ministério da Saúde | 13 / 1 | 4,088 s |
| Rio de Janeiro + OMS | 48 / 3 | 10,379 s |
| São Paulo + ambas | 61 / 4 | 20,490 s |

As saídas foram comparadas aos textos do CSV. Também foram verificados dados inválidos (HTTP 422), cidade inexistente (404), modelo ausente (503), falha climática induzida (502) e divisão de textos longos sem perda de caracteres.

## Conferência das rubricas

| Rubrica | Situação |
|---|---|
| 1. Sumarização integrada ao painel | Verificada funcionalmente |
| 2. Dados de API e scraping no contexto ESG/ODS | Demonstrados com dados reais |
| 3. Coleta, preparação, análise e apresentação | Fluxo implementado e exercitado |
| 4. Justificativa do problema de negócio e ESG/ODS | Documentada no Charter e no PDF |
| 5. Uso eficiente do LLM | Testado com o Qwen real |
| 6. Visualizações claras e organizadas | Parcial: falta inspeção visual |
| 7. Project Charter e Data Summary Report completos | Atualizados |
| 8. Simplicidade e fluidez de uso | Parcial: falta avaliação no navegador |

Esses resultados indicam o que foi verificado, e não uma nota atribuída pelo professor.

## Evidências guardadas

- `evidencias/api_real.json`: chamadas à API, respostas e tempos;
- `evidencias/streamlit_interacoes.json`: páginas e controles testados com AppTest;
- `evidencias/divisao_tokens.json`: reconstrução dos textos divididos;
- `evidencias/erros_servicos.json`: tratamento de indisponibilidade;
- `evidencias/abstrativo_reprovado.json`: exemplos que motivaram a síntese extrativa;
- `evidencias/ambiente_modelo.json`: ambiente e pesos usados.

Os scripts para repetir as verificações são `scripts/validar_tp5.py` e `scripts/validar_interface_tp5.py`. O README descreve como preparar o ambiente.

## Pendente

O navegador do Work não conseguiu acessar a aplicação local. Por isso, **não foram comprovados visualmente o layout, o menu, as capturas de tela e os botões de upload/download**. O AppTest executou o código da interface, mas não substitui essa avaliação.

O painel é educativo: não identifica oficialmente ondas de calor nem oferece aconselhamento médico. Os trechos escolhidos ainda devem ser conferidos nas páginas originais.
