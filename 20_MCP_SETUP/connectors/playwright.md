# Playwright — Browser automation

## Setup

```bash
claude mcp add playwright --command "npx -y @modelcontextprotocol/server-playwright"
```

## Tools

| Tool | Funcao |
|---|---|
| `browser_navigate` | Abre URL |
| `browser_snapshot` | Captura screenshot |
| `browser_click` | Click em elemento |
| `browser_type` | Digita em campo |
| `browser_wait_for` | Espera elemento |
| `browser_evaluate` | Roda JS no contexto da pagina |

## Casos de uso

### Auditar LP do mentorado

```text
Abre [URL da LP do mentorado].
Captura screenshot da fold acima.
Mede tempo de carregamento.
Verifica se Pixel/CAPI esta firing.
Audita: tem CTA visivel? Headline clara? Prova social?
```

### Espionar funil concorrente

```text
Abre [URL do concorrente].
Captura screenshot fold + secoes principais.
Salva em `05_WORKSPACE/clientes/[cliente]/_swipe/[concorrente]/`.
Documenta: oferta, preco, garantia, CTA, prova social.
```

### Testar fluxo de compra

```text
Abre [LP do cliente].
Simula compra:
1. Click CTA principal
2. Preenche checkout teste
3. Captura cada step
4. Reporta onde travou
```

## Seguranca

- **Nunca preencher dados reais de cartao** em fluxo de teste.
- **Headless mode** por padrao (sem janela visivel).
- **Cuidado com sites que detectam bot** — pode dar ban.
