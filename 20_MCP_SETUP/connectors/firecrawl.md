# Firecrawl — Scraping com IA

## Setup

```bash
claude mcp add firecrawl --command "npx -y @firecrawl/mcp-server"
```

API key obrigatoria:

```bash
# No .env local (nao commitar):
FIRECRAWL_API_KEY=fc-...
```

Conta em https://firecrawl.dev

## Tools

| Tool | Funcao |
|---|---|
| `firecrawl_scrape` | Scrape pagina unica |
| `firecrawl_crawl` | Crawl site inteiro |
| `firecrawl_search` | Busca web semantica |
| `firecrawl_extract` | Extrai dado estruturado de pagina |

## Casos de uso

### Pesquisa de concorrente

```text
Procura na web: "[concorrente do meu cliente]".
Resume: produto, posicionamento, preco, publico, claims, prova social.
Salva em `05_WORKSPACE/clientes/[cliente]/_intel/[concorrente].md`.
```

### Mapeamento de mercado

```text
Faz crawl de https://[blog-de-referencia-do-nicho].com.
Extrai: topicos mais publicados, palavras-chave, formatos.
Me lista 10 ideias de conteudo pro meu cliente.
```

### Coleta de prova social

```text
Procura "[nicho do cliente] depoimentos" e
"[nicho do cliente] reviews".
Compila 20 frases reais que pessoas falam.
Categoriza em: dor / desejo / objecao / linguagem.
Salva como `voc-ouro.md`.
```

## Seguranca

- **Respeitar robots.txt** do site.
- **Rate limit** moderado pra nao ser bloqueado.
- **Nao scrape de site com login** (viola TOS quase sempre).

## Alternativa: Exa

Exa (https://exa.ai) tem proposta similar. Usar 1 dos 2, nao ambos.
