# Plano simples para uso futuro de LLM

## Possibilidade de uso

Nas proximas etapas, os textos coletados do Ministerio da Saude e da WHO poderao ser utilizados por um Large Language Model (LLM) para gerar resumos e responder perguntas simples relacionadas a calor extremo e saude.

Um exemplo seria permitir que o usuario perguntasse quais cuidados gerais aparecem nas fontes coletadas. O modelo receberia os textos relevantes e produziria uma resposta curta em linguagem acessivel.

## Integracao com a aplicacao

A FastAPI podera servir como camada de integracao entre o modelo e a interface Streamlit:

`Pergunta no Streamlit → FastAPI → LLM → resposta no Streamlit`

Essa ideia aproveita a estrutura ja criada no TP3. Nesta etapa, nenhum modelo foi conectado e nenhuma chave de API e necessaria.

## Cuidados basicos

- indicar as fontes usadas na resposta;
- informar quando os textos nao forem suficientes;
- deixar claro que o conteudo e informativo;
- nao substituir orientacao medica ou alertas oficiais.

O objetivo deste plano e apenas preparar conceitualmente a proxima evolucao do projeto.
