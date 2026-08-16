# Access Preflight V30

## Objetivo

Pedir e validar acessos no inicio para evitar travar a execucao a cada etapa. O usuario final nao deve precisar entender terminal, WSL, PATH, bash, token, pasta ou permissao tecnica.

## Principio

Full-auto depende de preflight. O CoS deve pedir o pacote de acessos uma vez, organizar o que falta e seguir sem interromper quando a acao for reversivel.

## O que validar no inicio

| Area | O que pedir | Uso |
|---|---|---|
| Pasta do kit | caminho local do V30 | leitura/escrita de outputs, logs e workspace |
| Pasta do cliente | arquivos de briefing, provas, assets, historico | contexto do cliente |
| LP/site | URL, acesso editor ou export | auditar promessa e funil |
| WhatsApp/Cowork | acesso ao workspace, canais, templates, logs | criar e instalar bots |
| Automacoes | ferramentas usadas, dono do processo, permissoes, ambiente de teste | blueprints, SOPs e ativacao segura |
| CRM/agenda | acesso ou export de campos | SDR, follow-up e handoff |
| Meta Ads | `act_id`, pixel, CLI autenticado | diagnostico e trafego |
| Checkout | plataforma, eventos, produtos, abandono | funil e follow-up |
| Analytics | GA4, Hotjar, VSL, quiz | leitura de gargalos |
| Provas | depoimentos, numeros, prints permitidos | copy e objeções |
| Regras comerciais | preco, garantia, SLA, descontos | evitar bot inventar |

## Classificacao de permissao

| Tipo | Pode full-auto? | Regra |
|---|---|---|
| leitura local | sim | se estiver dentro do workspace permitido |
| escrita em outputs/workspace/logs | sim | registrar arquivos criados |
| install/tooling | pedir no inicio | depende do ambiente e pode alterar maquina |
| login/OAuth | pedir no inicio | usuario faz login, agente valida |
| acao em campanha real | nao | confirmar antes de pausar, ativar, editar budget ou publicar |
| disparo WhatsApp real | nao | confirmar antes de enviar em massa ou ativar runtime |
| automacao com escrita real | nao | confirmar antes de API write, CRM update, envio, budget, publicacao ou webhook ativo |
| alteracao de site/LP publicada | nao | confirmar antes de publicar |
| segredo/token | nunca pedir no chat | usar `.env` local, OAuth ou variavel de ambiente |

## Pacote minimo para comecar

```yaml
cliente:
objetivo:
pasta_cliente:
lp_url:
workspace_cowork:
whatsapp_numero:
crm:
agenda:
meta_act_id:
pixel_id:
checkout:
analytics:
responsavel_humano:
limites_de_automacao:
ferramentas_automacao:
ambiente_teste:
```

Se faltar algo, o CoS deve criar task com status `blocked` apenas para o item que realmente impede execucao. O restante avanca com `[A PREENCHER]`.

## Saida do preflight

```yaml
preflight_status: pass | partial | blocked
ready_now:
missing:
risky_actions_need_confirmation:
safe_defaults:
next_task:
```
