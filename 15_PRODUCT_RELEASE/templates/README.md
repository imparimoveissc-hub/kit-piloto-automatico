# Templates

Destino oficial dos templates da release V30. Organizados por **persona** (quem usa) e por **funcao** (gestao operacional).

## Estrutura

### Por persona

- `geral/` - templates que servem pra qualquer profissional
- `gestor-trafego/` - templates pra quem cuida de Meta Ads / Google Ads
- `social-media/` - templates pra quem produz conteudo / gerencia perfil
- `designer/` - templates pra quem entrega visual
- `videomaker/` - templates pra quem produz video

### Por funcao (gestao operacional)

- `gestao/` - templates de gestao do negocio:
  - `dre/` - entrega mensal de DRE pros clientes finais (5 artefatos)
  - `financeiro/` - controle financeiro do proprio negocio (5 artefatos)
  - `dashboard/` - KPIs e relatorio executivo (4 artefatos)
  - `landing-pages/` - estrutura de copy + arquitetura de LP (5 artefatos)
  - `operacao/` - SOPs, handoffs, reunioes, onboarding (5 artefatos)

## Total

| Categoria | Pastas | Templates |
|---|---|---|
| Por persona | 5 | 17 |
| Por funcao (gestao) | 5 | 24 |
| **Total** | **10** | **41** |

## Regra de uso

Copie a estrutura quando iniciar trabalho real. Preencha lacunas com `[A PREENCHER]` em vez de inventar.

Cada subpasta tem seu proprio `README.md` explicando uso especifico, variaveis e fluxo.

## Como escolher entre persona e funcao

- Se voce e UM ROLE especifico (designer, gestor de trafego, social media), comece pela pasta de persona
- Se voce e DONO de negocio ou socio gerenciando operacao, comece por `gestao/`
- Os dois caminhos se cruzam: voce pode ser social media usando `gestao/landing-pages/` pra fazer LP de cliente

## Padrao de variaveis

Todos os templates usam `{{MAIUSCULA_COM_UNDERSCORE}}` pra variaveis e `[A PREENCHER]` pra blocos de texto que voce escreve manualmente.

Quando o valor real ainda nao existe, manter o marcador ao inves de inventar.
