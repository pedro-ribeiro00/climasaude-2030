# Modelo local - TP4 e TP5

O projeto usa o modelo `Qwen/Qwen2.5-0.5B-Instruct`, da família Qwen, para resumir textos. Ele foi escolhido por ser pequeno (cerca de 0,5 bilhão de parâmetros), seguir instruções e oferecer suporte ao português. Modelos maiores podem produzir respostas melhores, mas demandam mais memória e processamento. O modelo menor pode cometer erros e não foi validado para decisões de saúde; a resposta deve ser conferida na fonte.

O modelo é público no Hugging Face e carregado com Transformers e PyTorch. Depois do download inicial, a aplicação usa somente os arquivos locais (`local_files_only=True`), sem enviar o texto para uma API externa. A inferência usa CPU; GPU não é obrigatória. A memória e o tempo necessários dependem da máquina, da instalação e do tamanho do texto. Os pesos ocupam aproximadamente 1 GB em formato de 16 bits, enquanto a execução pode usar mais memória. Verifique o espaço livre e teste na máquina que será utilizada.

O usuário envia um texto pelo Streamlit. A rota `POST /processar_texto` recebe o texto, carrega o modelo local e retorna o resumo em JSON. As respostas são validadas com Pydantic; entradas inválidas retornam 422, modelo indisponível retorna 503 e falha durante a geração retorna 500. O texto é limitado a 6.000 caracteres e a entrada do modelo a 2.048 tokens. Textos longos são divididos pelo tokenizer real; o código rejeita entradas que excedam o limite em vez de truncá-las silenciosamente. Se uma geração livre atingir o limite de saída sem terminar, retorna erro explícito. A rota não substitui orientação médica ou alertas oficiais.

Para instalação, download e execução, consulte o README. Fonte: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct

## Verificação local

Em um ambiente Linux com Python 3.12, PyTorch em CPU e sem conexão do modelo com a internet, a rota retornou um resumo em cerca de 10 segundos para um texto curto, incluindo o carregamento inicial. O tempo varia conforme o hardware e o texto. O modelo apresentou redação imperfeita e, em uma tentativa anterior, acrescentou informações que não constavam no texto. Mesmo com instruções para evitar isso, não há garantia de fidelidade; é necessária revisão humana.


## Síntese automática - TP5

O mesmo modelo Qwen2.5-0.5B-Instruct foi mantido para evitar outro serviço ou dependências pagas. A nova rota `POST /sintese` recebe os trechos coletados e um contexto com os indicadores climáticos. O modelo seleciona os trechos relevantes de cada bloco e consolida até três evidências, mantendo seu texto original. O contexto climático é incluído em cada seleção.

A engenharia de prompts orienta o modelo a usar apenas os dados recebidos e a não inventar medições, alertas oficiais ou diagnósticos médicos. A geração utiliza `do_sample=False`, mas ainda pode produzir erros. São aceitos até 150 trechos e 40 mil caracteres; o contexto tem limite de 1.200 caracteres. A rota retorna o resumo, o identificador do modelo e as quantidades de trechos e blocos utilizados.

A validação real mostrou que o modo abstrativo acrescentava uma “emergência climática” não demonstrada pela previsão. O TP5 passou a usar sumarização extrativa: o Qwen gera índices de trechos com decodificação restrita aos índices válidos. A resposta apresenta os trechos originais selecionados e o contexto climático recebido. Não há textos de reserva, inferência simulada ou substituição por outro modelo. As fontes em inglês permanecem em inglês.

Todos os trechos entram nos blocos, limitados por tokens e pelo espaço ocupado pelo contexto. A seleção descarta conteúdo por relevância, como parte normal da sumarização; não há corte silencioso por estouro da janela. A consolidação usa os candidatos dos blocos, até três evidências. O resultado não confirma a validade atual de alertas eventualmente presentes nas páginas coletadas.

Os pesos locais são resolvidos com `snapshot_download(local_files_only=True)` e passados como caminho ao Transformers. Isso evita uma consulta de metadados que, na versão instalada, ocorria mesmo com `local_files_only=True` ao passar apenas o identificador do modelo. Consulte os tempos e as respostas reais em `05_acceptance/evidencias/`.
