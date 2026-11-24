# Project Charter - ClimaSaúde 2030

## Problema e objetivo

Previsões do tempo e orientações sobre calor e saúde estão em fontes diferentes. O ClimaSaúde 2030 foi criado para reunir essas informações e facilitar sua consulta em uma interface simples.

O público principal é formado por pessoas interessadas nas condições climáticas de sua cidade. O projeto também pode ser usado como exemplo educativo por estudantes e pessoas que trabalham com temas ambientais.

## Solução

A aplicação usa Streamlit e FastAPI para apresentar:

- previsão de sete dias em cinco cidades brasileiras, consultada na Open-Meteo;
- temperatura máxima, sensação térmica, índice UV, precipitação e gráficos;
- textos do Ministério da Saúde e da OMS, coletados com Beautiful Soup;
- estatísticas textuais, nuvem de palavras e upload/download de CSV;
- resumo livre com o Qwen local (TP4);
- painel final com seleção automática de trechos coletados (TP5).

No TP5 foi escolhida a **opção 2: sumarização automática com LLM**. O usuário seleciona a cidade e as fontes. O Qwen recebe o contexto climático, escolhe os trechos mais relevantes e a aplicação apresenta os textos originais. Essa abordagem foi adotada após erros observados na geração livre.

## Escopo e limites

O projeto oferece informações educativas. Ele não emite alertas oficiais, não classifica ondas de calor, não prevê doenças nem substitui orientação médica.

O IBGE foi considerado no início, mas não foi integrado à versão final. Também não são medidos indicadores de governança ou desempenho ESG de empresas.

## Metas e critérios de sucesso

| Meta | Verificação |
|---|---|
| Reunir dados de fontes distintas | Previsão e textos públicos acessíveis no mesmo painel |
| Organizar as informações | Indicadores, tabelas e gráficos por cidade |
| Aplicar LLM a dados coletados | FastAPI, Qwen real e síntese no painel |
| Identificar a origem dos textos | URL e horário de coleta |
| Permitir reprodução | Código, dependências e instruções no GitHub |

Em 23/11/2026 houve testes funcionais com dados externos e Qwen local. A interface também foi executada pelo AppTest; a avaliação visual no navegador ficou pendente.

## ESG, ODS e metodologia

O projeto se relaciona ao pilar **Ambiental**, por usar dados climáticos, e ao **Social**, por apresentar informações públicas sobre saúde. O **ODS 13** é o principal, com conexões aos **ODS 3 e 11**. Espera-se facilitar o acesso à informação, mas não foi medido impacto social ou clínico.

A organização segue o TDSP: compreensão do problema, obtenção e preparação dos dados, modelagem, implantação e aceite. O CRISP-DM foi usado como referência complementar.

O desenvolvimento ocorreu em etapas: TP1 (protótipo climático), TP2 (interatividade e scraping), TP3 (FastAPI e páginas), TP4 (Qwen local) e TP5 (síntese automática no painel). As versões anteriores permanecem no histórico do GitHub.
