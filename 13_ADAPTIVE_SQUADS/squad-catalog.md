# Squad Catalog V30

## Papeis operacionais

| Papel | Ativa quando | Inputs | Output | Gate |
|---|---|---|---|---|
| CoS | qualquer pedido | pedido, contexto, ledger | task, rota, premissas | GATE-INTAKE |
| Product Auditor | promessa publica vs entrega | LP, oferta, onboarding, suporte | mapa de gap produto | GATE-PRODUCT |
| Researcher | sem VOC/prova/mercado claro | fontes, publico, concorrentes | VOC e hipoteses | GATE-RESEARCH |
| Strategist | promessa/mecanismo/oferta | VOC, provas, contexto | DRE, MUP, MUS, promessa | GATE-STRATEGY |
| Copy Director | copy, LP, ads, scripts | estrategia, VOC, prova | copy nucleus e pecas | GATE-COPY |
| Production Lead | pagina, criativos, specs | copy aprovada, marca | assets/specs | GATE-PRODUCTION |
| Traffic Analyst | campanha e metricas | oferta, assets, dados | plano/leitura | GATE-TRAFFIC |
| WhatsApp Orchestrator | conversa/bot/atendimento | oferta, contexto, restricoes | mapa de bots | GATE-WHATSAPP |
| SDR Attendant | lead interessado | criterios de fit, objeções | fluxo SDR | GATE-WHATSAPP |
| CS Bot | onboarding/suporte/churn | promessa, marcos, SLA | fluxo CS | GATE-WHATSAPP |
| Follow-up Bot | oportunidade parada | estagio, objeção, timing | sequencia follow-up | GATE-WHATSAPP |
| Cowork Architect | runtime/automacao | fluxos, estados, tags | docs Cowork | GATE-WHATSAPP |
| QA Editor | entrega relevante | output, gate, contexto | issues/fixes/verdict | gate correspondente |

## Comandos adaptativos por squad

### `whatsapp-revenue`

```yaml
commands:
  "*mapa-whats": "mapear bots, estados e handoffs"
  "*sdr": "criar ou revisar fluxo SDR"
  "*follow": "criar follow-up por estagio"
  "*cowork": "gerar docs Cowork"
  "*qa-whats": "validar fluxo WhatsApp"
```

### `product-hardening`

```yaml
commands:
  "*auditar-lp": "comparar LP/promessas com entrega real"
  "*gap-produto": "listar lacunas de produto"
  "*roadmap-robusto": "priorizar melhorias por impacto"
  "*gate-promessa": "validar claims e provas"
```

### `growth-diagnostic`

```yaml
commands:
  "*onde-quebrou": "diagnostico de funil"
  "*tracking": "auditoria pixel/CAPI"
  "*criativos": "analise de DNA criativo"
  "*escala": "plano de escala"
```

## Regra de adaptacao

O CoS pode criar comandos curtos especificos do cliente quando:

- o comando aparece 2 vezes em tarefas reais;
- o output e previsivel;
- existe gate;
- existe owner;
- o comando reduz perguntas futuras.

Comandos especificos do cliente ficam no `squad-manifest.yaml`, nao no core do kit.

