# Router V30

## Roteamento primario

| Tipo | Entrada comum | Saida esperada | Agente |
|---|---|---|---|
| Intake | pedido cru, ideia solta | task clara + premissas | CoS |
| Research | publico, mercado, concorrentes | mapa de VOC + hipoteses | Researcher |
| Strategy | oferta, Big Idea, mecanismo | tese + MUP + MUS + promessa | Strategist |
| Copy | LP, VSL, ads, email | nucleo de copy + pecas | Copy Director |
| WhatsApp | chatbot, SDR, prospeccao, follow-up, sucesso, Cowork | fluxos + specs de automacao | WhatsApp Orchestrator |
| Automacao | automatizar processo, SOP, n8n, Make, Zapier, Cowork generico, workflow | blueprint + SOP + teste + rollback | Automation Architect |
| Production | pagina, design, criativo, video | assets e specs | Production Lead |
| Traffic | campanhas, metricas, otimizacao | plano e diagnostico | Traffic Analyst |
| Product Hardening | LP, promessa, produto robusto, entrega | mapa de gaps + roadmap | Product Auditor |
| Adaptive Squad | squads, comandos por cliente, adaptar agentes | squad-manifest atualizado | CoS |
| Builder | criar agente, skill, task, diretriz nova | arquivo novo + indice atualizado | Forge (`21_BUILDER_KIT/`) |
| MCP Setup | conectar Drive/WhatsApp/Slack/Meta/Composio | conector configurado + .env atualizado | CoS + `20_MCP_SETUP/` |
| QA | revisar, validar, melhorar | issues + fixes + verdict | QA Editor |

## Edge cases

| Caso | Decisao |
|---|---|
| Copy sem pesquisa | Research leve antes, depois Copy |
| Oferta sem mecanismo | Strategy antes de Copy |
| WhatsApp sem oferta/contexto | Context pack + WhatsApp draft com `[A PREENCHER]` |
| Automacao sem processo claro | Criar SOP primeiro, depois blueprint em `draft` |
| Automacao com envio/API/CRM/budget | Bloquear ativacao real em `GATE-AUTOMATION` ate confirmacao |
| Bot pronto mas sem handoff humano | Bloquear em GATE-WHATSAPP |
| Usuario leigo / muitas permissoes | Rodar `/preflight-acessos` antes |
| LP prometendo mais que produto entrega | T08 Product Hardening antes de escalar copy/trafego |
| Pedido de "squad especifico" | Criar/atualizar `squad-manifest.yaml` do cliente |
| Pedido de "funil completo" | Pipeline V30 completo |
| Pedido de novo agente/skill/task | Acionar Forge em `21_BUILDER_KIT/` |
| Pedido de conexao com ferramenta externa | Consultar `20_MCP_SETUP/` antes de prometer |
| Cliente especifico | Ler context pack do cliente, nao historico inteiro |
| Peca avulsa simples | Skill mental direta via agente certo, sem pipeline completo |
| Falha em gate 2 vezes | Upgrade de modelo e QA Editor |
| Falha em gate 3 vezes | Voltar etapa anterior, nao insistir na mesma abordagem |

## Uma rota por vez

O CoS pode enfileirar multiplas tasks, mas so ativa uma rota principal por vez. Paralelismo so entra em producao quando dependencias estao claras: paginas, criativos e videos podem rodar depois de copy + direcao visual aprovadas.
