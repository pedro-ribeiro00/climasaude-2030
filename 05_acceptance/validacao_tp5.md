# Validação - TP5

## Funcionalidade entregue

O painel final apresenta a previsão da Open-Meteo, gráficos e textos públicos sobre calor e saúde. O modelo Qwen local é chamado pela FastAPI para resumir automaticamente os textos selecionados e produzir uma síntese com contexto climático.

## Checklist de aceite

1. Iniciar os serviços seguindo o README.
2. Conferir previsão, métricas e gráfico nas cinco cidades.
3. Filtrar as fontes e confirmar que os textos exibidos são os coletados no CSV.
4. Acionar **Gerar síntese**, conferir se o modelo realmente responde e se mostra o total de trechos e blocos.
5. Conferir se as afirmações geradas são sustentadas pelos textos originais e pelos indicadores.
6. Verificar se as funcionalidades anteriores seguem operacionais.
7. Conferir tratamentos de erros quando a API/modelo não estão disponíveis.

## Situação dos testes

O algoritmo de divisão e sumarização em blocos foi exercitado com função simulada, sem testar a qualidade factual do Qwen. Testes de sintaxe e integração devem ser confirmados após atualizar o repositório. A execução visual completa do Streamlit e a inferência com o modelo real permanecem pendentes da instalação das dependências e pesos num computador de teste. Não registrar esses itens como aprovados antes de executá-los.

## Limitações

A geração com Qwen pequeno pode ser lenta e imprecisa. O CSV reflete a última coleta por scraping. A ferramenta não produz alertas oficiais nem orientação médica.
