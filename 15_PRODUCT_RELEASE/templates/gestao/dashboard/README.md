# Templates Dashboard

Dashboards de gestao pro dono do negocio (ou socio, ou gestor). Sao templates de RELATORIO + INTERPRETACAO, nao templates de design BI. Servem como base do que voce vai montar no Google Sheets, Notion, Looker ou Excel.

## O que tem aqui

| Arquivo | O que e | Frequencia |
|---|---|---|
| `dashboard-operacional-semanal.md` | Foto da semana: vendas, marketing, financeiro, operacao | Toda segunda de manha (30 min) |
| `kpis-por-area.md` | Catalogo dos KPIs por area do negocio + benchmarks | Definir 1x, revisar trimestralmente |
| `relatorio-executivo-mensal.md` | Relatorio mensal pra socios / investidores / equipe | Todo dia 10 (apos fechar DRE) |

## Pra quem e

- Dono de pequena/media empresa que precisa visibilidade rapida sem ter time de BI
- Socio de agencia/escritorio querendo cruzar 4 areas (vendas, marketing, financeiro, operacao) em uma tela
- Gestor de filial / unidade respondendo pra socio principal
- Operador de e-commerce/infoproduto rodando perfomance media

## Filosofia

**Menos numero, mais decisao.** Dashboard que mostra 50 metricas e dashboard que ninguem olha. Dashboard que mostra 5 numeros e 1 conclusao e dashboard que vira reuniao de 15 min toda segunda.

### Regras de bom dashboard:

1. **No maximo 1 tela** (uma rolagem de scroll, nao mais)
2. **3-5 numeros principais** em destaque, resto detalhe
3. **Cada numero tem comparacao** (vs semana passada / mes passado / ano passado)
4. **Cada numero tem status visual** (verde / amarelo / vermelho)
5. **Termina com acao**, nao com numero

## Como combinar

1. Define seus KPIs com `kpis-por-area.md` (1x)
2. Monta dashboard operacional semanal com `dashboard-operacional-semanal.md`
3. Roda toda segunda em 30 min
4. Todo dia 10 fecha o mes com `relatorio-executivo-mensal.md` (consolidado)

## Ferramentas sugeridas pra implementar

| Stack | Ideal pra | Complexidade |
|---|---|---|
| Google Sheets | Comecar, ate 50k linhas, gratis | Baixa |
| Notion (databases + views) | Visualizar misturado com docs/processos | Baixa-media |
| Looker Studio (Data Studio) | Visual bonito, conecta Sheets/MySQL gratis | Media |
| Power BI | Empresa media, conecta SAP/dados grandes | Alta |
| Metabase / Redash (self-hosted) | Time tech, dados em SQL | Alta |

Comece em Sheets. Migra quando tiver dor.
