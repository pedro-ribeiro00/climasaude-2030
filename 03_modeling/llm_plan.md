# Modelo de linguagem - ClimaSaúde 2030

## Modelo escolhido

O projeto usa o **Qwen2.5-0.5B-Instruct**, disponível no Hugging Face. Por ser pequeno, pode ser executado em CPU, sem contratar uma API paga. Ele é carregado localmente com PyTorch e Transformers depois do download inicial.

## TP4 e TP5

No **TP4**, a rota `POST /processar_texto` passou a gerar resumos livres de textos informados pelo usuário. Essa função continua disponível, mas pode conter imprecisões.

No **TP5**, a rota `POST /sintese` utiliza os textos que foram coletados do Ministério da Saúde e da OMS. O modelo recebe trechos numerados e a previsão da cidade selecionada como contexto. O prompt pede a escolha dos trechos mais relevantes sobre calor, saúde e prevenção, preferindo orientações gerais a alertas antigos ou referências bibliográficas.

O programa limita a resposta do Qwen aos números dos trechos existentes. Depois, exibe os parágrafos originais selecionados, sem reescrevê-los. Esse procedimento é chamado **sumarização extrativa**. As informações da OMS permanecem em inglês.

A mudança foi feita após testes em que o resumo livre afirmou uma emergência climática sem respaldo na previsão. A seleção extrativa reduz o risco de frases inventadas, mas a fonte e a data ainda devem ser conferidas.

## Processamento e limites

Os textos são divididos conforme os tokens aceitos pelo modelo, sem descartar silenciosamente o final. O processamento é sequencial e pode demorar em CPU. A API informa erro quando os dados são inválidos, quando o modelo não está instalado ou quando não é possível concluir a geração.

Em **23/11/2026**, foram testadas sínteses com o Qwen real em três cenários: apenas Ministério da Saúde, apenas OMS e ambas as fontes. Os resultados foram confrontados com o CSV. Os tempos e saídas estão em `05_acceptance/evidencias/api_real.json`.

Fonte: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
