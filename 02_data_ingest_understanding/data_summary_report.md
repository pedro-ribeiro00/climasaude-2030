# Data Summary Report - ClimaSaúde 2030

## Fontes utilizadas

| Fonte | Obtenção | Uso |
|---|---|---|
| Open-Meteo | API pública em JSON | Previsão de sete dias e indicadores |
| Ministério da Saúde | Requests e Beautiful Soup | Orientações sobre calor e saúde |
| Organização Mundial da Saúde (OMS) | Requests e Beautiful Soup | Textos complementares sobre calor e saúde |
| CSV do usuário | Upload durante a sessão | Exploração e análise textual complementar |

A previsão é consultada para São Paulo, Rio de Janeiro, Belo Horizonte, Brasília e Porto Alegre. Os campos usados da Open-Meteo são time, temperature_2m_max, apparent_temperature_max, uv_index_max e precipitation_sum.

## Coleta e organização

O script scripts/scrape_heat_content.py extrai títulos, parágrafos e itens de lista das páginas públicas. Remove elementos como navegação e scripts e descarta trechos curtos ou duplicados. Os resultados ficam em data/raw/conteudo_calor_saude.csv e data/raw/conteudo_calor_saude.txt.

O CSV conserva as seguintes colunas:

| Coluna | Significado |
|---|---|
| fonte | Instituição que publicou o texto |
| url | Endereço da página |
| tipo_elemento | Tag HTML de origem |
| texto | Conteúdo coletado |
| coletado_em_utc | Horário da coleta |

Na execução de **23/11/2026** foram coletados **61 trechos**: 13 do Ministério da Saúde e 48 da OMS. O scraping é executado separadamente, portanto a abertura do painel não atualiza o CSV.

## Processamento e uso da IA

A FastAPI organiza os dados da Open-Meteo e calcula estatísticas textuais. O Streamlit apresenta os resultados em tabelas e gráficos, além da nuvem de palavras.

No TP5, o usuário escolhe cidade e fontes. A previsão e os textos selecionados são enviados à FastAPI. Os trechos são divididos de acordo com o limite de tokens do Qwen, que escolhe evidências textuais de cada grupo. A aplicação apresenta até três trechos preservando o idioma original.

O arquivo de upload é usado na página de exploração de CSV. Ele não substitui dados meteorológicos nem alimenta automaticamente a síntese do TP5.

## Qualidade e limitações

- As previsões da Open-Meteo podem mudar a cada atualização e não equivalem a alertas oficiais.
- O horário da coleta não é necessariamente a data de publicação dos textos.
- Os textos podem conter informações antigas ou não aplicáveis à cidade selecionada.
- Mudanças no HTML podem exigir ajustes no scraper.
- Os textos da OMS permanecem em inglês.
- A síntese seleciona trechos relevantes, mas não cobre necessariamente todos os temas das fontes.

Os resultados precisam ser conferidos nas páginas originais. O IBGE foi cogitado no planejamento, mas não integrou a versão final.
