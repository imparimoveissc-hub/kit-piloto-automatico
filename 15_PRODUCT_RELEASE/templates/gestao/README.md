# Templates de Gestao

Categoria de templates para gestao operacional do negocio. Diferente das pastas por persona (designer, gestor-trafego, social-media, videomaker), aqui sao templates por **funcao** — uteis pra qualquer profissional que rode operacao propria ou de cliente.

## O que tem aqui

| Pasta | Pra que serve | Quando usar |
|---|---|---|
| `dre/` | Entrega mensal de DRE (Demonstracao do Resultado) com analise + insights pro cliente final | Escritorio contabil, financeiro de cliente B2B, controladoria terceirizada |
| `financeiro/` | Controle financeiro do proprio negocio (fluxo de caixa, contas, pro-labore) | Dono de pequena empresa, freelancer, agencia em crescimento |
| `dashboard/` | Dashboards semanais e mensais (KPIs por area + relatorio executivo) | Quem precisa visibilidade de operacao pra decidir |
| `landing-pages/` | Estruturas de copy + sessoes pra LPs (servico B2B, captura, vendas) | Quem cria pagina pra cliente ou pro proprio negocio |
| `operacao/` | SOPs, handoffs, reuniao semanal, onboarding de time | Quem ta organizando operacao interna |

## Como usar

1. Entra na subpasta da funcao desejada.
2. Le o `README.md` da subpasta — explica fluxo + variaveis.
3. Copia o template pro local de trabalho do projeto/cliente.
4. Preenche placeholders `{{VARIAVEL}}` e `[A PREENCHER]`.
5. Roda o `checklist-*.md` (quando existe) antes de entregar.

## Regra de variaveis

Padrao consistente em todos os templates desta categoria:

- `{{NOME_EMPRESA}}` — empresa cliente final
- `{{NOME_ESCRITORIO}}` — quem ta entregando (sua agencia/escritorio)
- `{{PRIMEIRO_NOME_CLIENTE}}` — vocativo no email
- `{{MES_REFERENCIA}}` — "abril/2026" formato extenso
- `{{ANO_MES}}` — "2026-04" formato curto
- `{{CONTADOR_RESPONSAVEL}}`, `{{CRC}}`, etc — campos profissionais

Quando o valor real ainda nao existe, manter `[A PREENCHER]` ao inves de inventar.

## Voz dos templates

Profissional + humano. Numero antes da palavra. Acao concreta (verbo + objeto + prazo). Zero jargao tecnico em comunicacao com cliente (jargao pode no anexo tecnico, nao no corpo do email).

Ver rule global de voz: `~/.claude/rules/voz-humana-pt-br.md`.
