# Plano de integração futura com LLM

## Objetivo

Na etapa seguinte, o ClimaSaúde 2030 poderá usar um Large Language Model (LLM) para explicar dados climáticos e sintetizar conteúdo público sobre calor e saúde em linguagem acessível. O recurso terá caráter informativo e não deverá produzir diagnóstico, prescrição ou recomendação médica personalizada.

## Caso de uso prioritário

O usuário seleciona uma cidade e faz uma pergunta, por exemplo: "O que merece atenção nesta semana?". A aplicação combina a previsão estruturada com trechos relevantes das fontes públicas e solicita ao modelo um resumo curto. A resposta deve indicar as fontes utilizadas, separar fatos de orientações gerais e repetir que alertas oficiais têm prioridade.

## Arquitetura proposta

`Pergunta + cidade → FastAPI → recuperação de dados climáticos e trechos → prompt estruturado → LLM → validação → Streamlit`

A FastAPI continuará como camada de integração. Dessa forma, credenciais nunca serão expostas no navegador ou no código da interface, e o provedor do modelo poderá ser substituído sem reescrever as páginas Streamlit.

## Preparação dos dados

O scraping do TP3 já preserva `fonte`, `url`, `idioma`, `hash_conteudo` e `coletado_em_utc`. Esses campos permitem:

- remover duplicidades e detectar mudanças;
- dividir textos em trechos mantendo sua proveniência;
- criar embeddings e um índice vetorial;
- recuperar conteúdo por similaridade;
- citar a fonte original na resposta.

Antes da indexação serão aplicados limpeza, segmentação, identificação de idioma e validação de URLs. Conteúdos enviados pelo usuário só poderão entrar no índice após consentimento e não serão persistidos por padrão.

## Estratégia RAG

Será adotado Retrieval-Augmented Generation (RAG), em vez de enviar toda a base ao modelo. Para cada pergunta, a aplicação recuperará poucos trechos relevantes e incluirá esses trechos no contexto. A resposta deverá ser limitada ao contexto recuperado; quando não houver evidência suficiente, o modelo deverá declarar a limitação.

## Contrato de entrada e saída

Entrada planejada:

- pergunta do usuário;
- cidade e período selecionados;
- indicadores climáticos normalizados;
- trechos recuperados com fonte e URL;
- idioma desejado.

Saída planejada:

- resumo em linguagem simples;
- indicadores que sustentam o resumo;
- lista de fontes e links;
- aviso de uso informativo;
- sinalização explícita quando a evidência for insuficiente.

## Segurança e qualidade

- Chaves de API serão fornecidas por variável de ambiente e nunca versionadas.
- Entradas terão limite de tamanho e tratamento contra instruções maliciosas presentes nas fontes.
- O modelo não receberá dados pessoais desnecessários.
- Respostas serão avaliadas quanto a fidelidade, presença de citações, clareza e recusa de diagnóstico médico.
- Logs não armazenarão segredos nem arquivos enviados pelo usuário.
- Custos, latência e falhas do provedor serão tratados pela API.

## Avaliação antes de liberar

Será criado um conjunto de perguntas representativas com respostas esperadas e fontes conhecidas. Os critérios mínimos serão: informação apoiada pelas fontes, citação correta, ausência de aconselhamento médico indevido, linguagem compreensível e comportamento seguro quando os dados estiverem incompletos.

## Etapas futuras

1. Normalizar e segmentar o corpus textual.
2. Criar índice de recuperação com metadados.
3. Implementar uma interface de provedor na FastAPI.
4. Criar endpoint autenticado para perguntas.
5. Adicionar guardrails e validação de saída.
6. Executar avaliação offline antes de habilitar a funcionalidade no Streamlit.
