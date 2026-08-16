# Meta Ads (Facebook + Instagram)

## Recomendacao por uso

| Uso | Ferramenta |
|---|---|
| Gerenciar campanhas pagas (criar, pausar, escalar) | **Meta Ads CLI nativo** (`/meta-cli-install`) |
| Postar conteudo organico no Instagram/Facebook | **Composio Rube** |
| Ler insights de campanha + posts | **Meta Ads CLI** (mais granular) ou **Rube** (mais facil) |
| Espionar concorrentes (Ad Library) | **@competitor-spy** da Traffic Stack |

## Meta Ads CLI (gestao de campanhas)

Ja documentado em:

- `11_TRAFFIC_STACK/PLAYBOOK.html` (manual operacional)
- `11_TRAFFIC_STACK/skills/meta-cli-install/SKILL.md` (skill V30)
- Comando: `/meta-cli-install`

Instalacao cobre Windows (WSL Ubuntu) + macOS + Linux. OAuth via browser. Sem App Review, sem token manual.

## Composio Rube (organico)

Pra postagens organicas:

```text
Cria post no Instagram da [empresa] com texto: [...].
Confirma antes de postar.
```

Cobre:
- Posts (feed)
- Stories
- Reels (upload)
- Resposta a comentarios
- Resposta a DMs
- Insights basicos

## Estrategia recomendada pro mentorado

1. Se mentorado faz **trafego pago**: instala Meta Ads CLI via `/meta-cli-install`.
2. Se mentorado faz **conteudo organico** ou **gestao social**: usa Rube.
3. Se faz **os dois**: ambos rodam paralelo, cada um com seu escopo.

## Seguranca

- **Token do CLI Meta** vive no `~/.profile` do WSL/shell. NUNCA no kit.
- **Token Rube** vive na Composio. NUNCA no kit.
- **Confirmar antes de:** pausar campanha, mudar budget >20%, postar organico publico, responder DM em nome da empresa.
