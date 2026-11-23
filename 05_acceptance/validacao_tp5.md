# Validação final do TP5 — 23/11/2026

## Resultado

A API e as interações do Streamlit foram executadas com dados externos reais e o Qwen2.5-0.5B-Instruct local. A validação funcional passou após as correções descritas abaixo. O aceite completo permanece pendente da inspeção visual no navegador e das capturas de tela; não há evidência visual da aplicação funcionando nesta execução.

Referência inicial: branch `main`, commit `c0d2a4c`. Consulte [as evidências](evidencias/) e os dois scripts de validação em `scripts/`.

## Ambiente e dados

- Python 3.12, PyTorch CPU e Transformers; versões e SHA-256 dos pesos em `evidencias/ambiente_modelo.json`.
- Pesos reais: 988.097.824 bytes, revisão `7ae557604adf67be50417f59c2c2f167def9a775` do Qwen. Não foram usadas respostas de LLM simuladas.
- Coleta real de 61 trechos: 13 do Ministério da Saúde e 48 da OMS. CSV/TXT atualizados, mantendo URL e horário da coleta.
- Previsões reais de sete dias nas cinco cidades. A amostra de upload não é usada como previsão nem como fonte da síntese TP5.

## Testes executados

| Verificação | Resultado | Evidência |
|---|---|---|
| `/health`, `/cidades`, previsão e análise textual | Respostas válidas | `api_real.json` |
| `/processar_texto` com trecho coletado | Qwen real, HTTP 200 | `api_real.json` |
| `/sintese` com SP/MS, RJ/OMS e SP/ambas | Qwen real, HTTP 200; trechos conferidos com o CSV | `api_real.json` |
| Cidade inexistente | HTTP 404 | `api_real.json` |
| Textos vazios, limites inválidos, contexto só com espaços e excesso de tamanho | HTTP 422 | `api_real.json` |
| Modelo ausente em processo com cache vazio | HTTP 503 nas duas rotas de inferência | `erros_servicos.json` |
| Timeout externo induzido | HTTP 502, sem previsão de reserva | `erros_servicos.json` |
| Início e funções das cinco demais páginas | Executadas sem exceção pelo AppTest | `streamlit_interacoes.json` |
| Seleção das cinco cidades | Métricas reais carregadas | `streamlit_interacoes.json` |
| Filtros, ausência de fontes e botão de síntese | Mensagens e resultados esperados | `streamlit_interacoes.json` |
| Síntese após novo rerun com a mesma configuração | Resultado preservado | `streamlit_interacoes.json` |
| CSV de exemplo já colocado na sessão e limpeza | Tabelas processadas e sessão limpa | `streamlit_interacoes.json` |
| Texto longo, Unicode e marcador no fim | Reconstrução exata dos blocos, sem perda de caracteres | `divisao_tokens.json` |
| Inspeção de pixels, menu no navegador e capturas | **Pendente** | Bloqueio descrito abaixo |
| Seletor de upload e download pelo navegador | **Pendente** | AppTest não comprova essas interações nativas |

Os arquivos de evidência ficam em `05_acceptance/evidencias/`. Os testes de indisponibilidade são separados dos testes positivos: apenas o timeout climático foi induzido com substituição que lança exceção. Nenhuma resposta climática ou resposta de modelo simulada foi registrada como funcionamento real.

## Problemas encontrados e correções

1. **Carregamento offline:** o tokenizer tentava buscar metadados no Hugging Face e recebeu HTTP 429, apesar dos arquivos já baixados. O carregamento agora resolve o snapshot em cache e usa seu caminho local.
2. **Truncamento silencioso:** as entradas eram cortadas em 2.048 tokens, embora a divisão considerasse caracteres. A divisão agora usa o tokenizer real, reserva espaço para instruções/contexto e rejeita excessos sem descartar o fim do texto.
3. **Fidelidade da geração:** a versão abstrativa retornou uma suposta “emergência climática” em São Paulo sem respaldo na previsão. Uma tentativa com a OMS também excedeu o limite de saída. As tentativas reprovadas estão em `abstrativo_reprovado.json`.
4. **Síntese extrativa:** para manter o modelo pequeno e os fatos rastreáveis, o Qwen passou a escolher índices de trechos com geração restrita aos índices válidos. A aplicação mostra o texto selecionado sem reescrevê-lo e reproduz o contexto climático recebido. O modelo é realmente executado; não há resposta fixa de reserva. O texto da OMS permanece em inglês.
5. **Estado do painel:** a síntese é mantida na sessão para a mesma cidade, fontes e versão dos dados, sem reaparecer como resultado de outra configuração. O horário da coleta é exibido.
6. **API e documentação:** contexto só com espaços retorna 422; versão da API atualizada para 5.0.0; README e documentos TDSP refletem o funcionamento testado.

A rota legada `/processar_texto` continua abstrativa e pode conter imprecisões. Sua disponibilidade foi testada, mas isso não certifica a fidelidade de toda resposta livre. O painel TP5 usa a síntese extrativa em `/sintese`.

## Tempo e conteúdo

Os tempos completos por chamada estão nos JSONs. Nos cenários medidos, uma fonte levou aproximadamente 4 a 11 segundos pela API; duas fontes levaram mais tempo por exigir consolidação. A chamada inicial de resumo livre, incluindo carregamento, levou aproximadamente 8 segundos. Esses tempos são compatíveis com uma demonstração acadêmica neste ambiente, sem garantia para outro hardware.

Todos os trechos entram nos grupos processados. Uma síntese seleciona uma parte do conteúdo por relevância; não promete reproduzir todos os fatos. A validação compara os trechos selecionados com o CSV e o contexto com a previsão enviada. As afirmações copiadas continuam sujeitas à data e às limitações da fonte original. As máximas previstas, por si só, não demonstram onda de calor, emergência ou risco individual.

## Relação com as rubricas recebidas

| Rubrica | Evidência e limite |
|---|---|
| Integração da sumarização ao dashboard | Botão → FastAPI → Qwen real → resultado e fontes, exercitado por AppTest; aparência no navegador pendente |
| Uso de API e scraping para ESG/ODS | Previsões reais e textos públicos processados; Ambiental/ODS 13 e Social/ODS 3, com aplicação educativa às cidades/ODS 11; não mede impacto ESG nem desempenho corporativo |
| Ciclo completo de Ciência de Dados | Coleta atualizada, limpeza/deduplicação, métricas e gráficos, seleção com LLM, apresentação e avaliação registradas |
| Quarta rubrica | A mensagem recebida terminou em “Justificativa clara de como”; critério completo não disponível para conferir |

## Limite do navegador e pendências de aceite

A conexão à extensão do navegador expirou. O navegador do Work recusou acesso a `http://127.0.0.1:8501`; ao investigar a falha, sua política de segurança impediu prosseguir. O bloqueio não foi contornado. Os serviços iniciaram, mas não foi possível comprovar layout, navegação e downloads em uma página visível nem capturar imagens reais do dashboard.

Para encerrar o aceite: abrir FastAPI e Streamlit em um ambiente acessível pelo navegador, percorrer o menu e os controles, testar upload/download e capturar o painel com uma síntese. O AppTest é evidência de execução da interface Python, não substitui essa inspeção visual.
