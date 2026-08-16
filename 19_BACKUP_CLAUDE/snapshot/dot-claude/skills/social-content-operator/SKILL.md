---
name: social-content-operator
description: >
  Planejar, criar, adaptar e preparar conteúdo short-form para TikTok, Instagram Reels e
  Instagram Stories, do cronograma à publicação. Use quando o usuário pedir: "cronograma de
  postagem", "calendário editorial", "plano de conteúdo", "roteiro de reels", "conteúdo pro
  tiktok", "copy pra postar", "briefing de edição", "reaproveitar conteúdo", "adaptar reels
  pra tiktok", "hashtags", "agendar posts", "postar no instagram/tiktok", "estratégia de
  tiktok", "alavancar com tiktok", ou qualquer variação. Trata TikTok como canal de
  descoberta/alavancagem e adapta os melhores formatos para Reels e Stories. Entrega pacote
  pronto para postar manualmente e deixa o caminho de auto-post documentado em draft.
---

# Social Content Operator

Estrategista e operador de conteúdo short-form. Você cobre o ciclo inteiro:
**estratégia → calendário → roteiro → copy → criativo → edição → publicação.**

**Princípio-mãe: TikTok primeiro.** TikTok é o canal de descoberta (alavancagem de audiência
fria). Crie o conteúdo **nativo para TikTok** e depois **adapte** os vencedores para Reels
(conversão/autoridade) e Stories (relacionamento/venda com a base morna). Nunca poste o mesmo
vídeo com marca d'água de um app no outro — sempre adapte.

Skill **genérica multi-cliente**: não assuma nicho. Sempre carregue ou construa o `brief` do
canal antes de produzir. Se o brief já existe, leia e siga; se não, rode o intake (Passo 1).

---

## Localização dos arquivos (padrão V30)

Substitua `<cliente>` pelo slug do canal/marca (ex.: `impar`, `marca-pessoal`). Se for o
próprio usuário, use `<cliente>` = slug curto que ele indicar.

| O quê | Onde |
|---|---|
| Brief do canal (contexto vivo) | `05_WORKSPACE/clientes/<cliente>/social/brief.md` |
| Calendário mensal | `05_WORKSPACE/clientes/<cliente>/social/calendario-mensal.md` |
| Plano semanal | `05_WORKSPACE/clientes/<cliente>/social/plano-semanal.md` |
| Board de estado dos posts (fonte da verdade) | `05_WORKSPACE/clientes/<cliente>/social/posts.csv` |
| Kit por post (roteiro, copy, adaptações) | `05_WORKSPACE/clientes/<cliente>/social/posts/<id>/` |
| Criativos editados | `05_WORKSPACE/clientes/<cliente>/social/criativos/` |
| Entregável final (calendário aprovado, relatório) | `06_OUTPUTS/social-<cliente>/` |
| Rastro operacional | `07_LOGS/social-<cliente>.md` |
| Automação de auto-post (draft) | `18_AUTOMATION_STACK/social-autopost/` |

Templates ficam em `templates/` dentro desta skill. Reaproveite-os, não reinvente.

---

## Passo 1 — Intake (só se o brief não existir ou estiver desatualizado)

Leia `templates/brief.md`. Preencha com o que o usuário já deu; para o resto, pergunte o
**mínimo** em uma rodada. O que não vier, marque `[A PREENCHER]` e siga (política full-auto).

Perguntas essenciais (não pergunte o que já sabe):
- Nicho / o que vende (oferta principal).
- Público (ICP) e a dor nº 1 que ele resolve.
- 3–5 **pilares de conteúdo** (se não tiver, proponha a partir do nicho).
- Voz/tom da marca e o que **nunca** falar.
- Cadência desejada (ex.: TikTok 1x/dia, Reels 4x/semana, Stories diário).
- Ativos existentes (banco de vídeos, fotos, depoimentos, ofertas ativas).
- Slug `<cliente>` e handles de cada canal.

Salve em `05_WORKSPACE/clientes/<cliente>/social/brief.md`.

---

## Passo 2 — Estratégia + Calendário mensal

1. Leia `reference/estrategia-tiktok-alavancagem.md` para a lógica TikTok-first, o mix de
   formatos e a regra de proporção descoberta/nutrição/conversão.
2. Defina os **objetivos do mês** (ex.: crescer seguidores, aquecer base, vender oferta X).
3. Distribua os **pilares** pelas semanas.
4. Gere o calendário usando `templates/calendario-mensal.md`: para cada semana, tema,
   pilares, objetivo e a oferta/CTA dominante.

Entregue o calendário e **peça validação** antes de detalhar o diário (evita retrabalho).

---

## Passo 3 — Plano semanal + Board de posts

1. Quebre a semana validada em posts por canal, respeitando a cadência do brief.
2. Para cada post, crie uma linha no `posts.csv` (cabeçalho em `templates/posts.csv`):
   `id,data,canal,formato,pilar,ideia,hook,cta,status`
   - `id`: `YYYYMMDD-canal-nn` (ex.: `20260710-tiktok-01`).
   - `status`: `ideia → roteiro → gravar → editar → pronto → agendado → publicado`.
3. O `posts.csv` é a **fonte da verdade** do pipeline. Sempre atualize o status ao avançar
   uma etapa. Espelhe o resumo em `plano-semanal.md`.

---

## Passo 4 — Kit por post

Para cada post priorizado, gere a pasta `posts/<id>/` a partir de `templates/post.md`.
O kit **sempre separa** estes campos (nunca misture):

- **Ideia** — o insight/ângulo em uma frase.
- **Hook** — os 3 primeiros segundos (fala + texto de tela). Use `reference/formatos-e-hooks.md`.
- **Roteiro** — beat a beat, com timing (0–3s, 3–8s, corpo, CTA).
- **Visual** — enquadramento, cenas, b-roll, o que aparece na tela.
- **Edição** — briefing para o editor: cortes, ritmo, legendas, trilha, overlays, duração-alvo.
- **Legenda** — copy da caption (com quebra de linha e CTA no fim).
- **Texto de tela** — o que fica escrito no vídeo (por trecho).
- **CTA** — a ação única do post.
- **Canal** — tiktok / reels / stories.
- **Data / Status** — sincronizados com o `posts.csv`.
- **Hashtags** — bloco por canal.
- **Adaptação Reels** — o que muda do TikTok pro Reels (capa, duração, CTA, hashtags).
- **Adaptação Stories** — desmembramento em sequência de stories (enquete/caixinha/link/CTA).
- **Checklist de publicação** — ver Passo 6.

**Gate de copy (V30):** copy sem VOC, mecanismo, prova e nível de consciência identificados
fica como **rascunho**, não final. Marque `[draft]` até fechar esses 4.

---

## Passo 5 — Edição

Nesta máquina o pipeline de vídeo é **FFmpeg** (Remotion não renderiza aqui).

- Para editar de fato (cortes, legendas queimadas, color, overlays), acione a skill
  **`video-use`**, passando o briefing de edição do kit do post e o arquivo bruto.
- Salve o resultado em `05_WORKSPACE/clientes/<cliente>/social/criativos/<id>.mp4`.
- Especs por canal (proporção, duração, capa) estão em `reference/formatos-e-hooks.md`.
- Atualize o `status` do post para `pronto` no `posts.csv`.

---

## Passo 6 — Publicação

Dois modos. **Default = Modo A (pacote pronto).** O Modo B só ativa com credenciais e
confirmação explícita. Detalhes e setup em `reference/publicacao.md`.

### Modo A — Pacote pronto para postar (começa hoje, zero setup)
Monte o "cartão de publicação" do post: vídeo final + legenda + hashtags + texto de tela +
horário sugerido + CTA. Entregue pronto para o usuário publicar/agendar no app nativo (ou no
Meta Business Suite / TikTok). Marque `status = agendado`. Quando confirmar que saiu, `publicado`.

Regra de ouro do TikTok-first: **poste primeiro no TikTok**, avalie o desempenho das primeiras
horas, e só então dispare a adaptação para Reels/Stories dos que engancharam.

### Modo B — Auto-post via API (draft até validar)
Reels via **Instagram Graph API** (conta Business + app Meta) e TikTok via **Content Posting
API**. Documentado em `18_AUTOMATION_STACK/social-autopost/` em **modo draft**. Conforme a
política full-auto do kit: **publicação real, API write e disparo exigem confirmação explícita**
do usuário — nunca publique sozinho. Ative apenas quando as credenciais estiverem no `.env` e o
usuário mandar rodar.

---

## Regras

- **TikTok nativo primeiro**, adaptação depois. Nunca reposte com marca d'água.
- **Nunca publique de verdade sem confirmação** (Modo B). Sem credenciais → só Modo A.
- Atualize o `posts.csv` a cada mudança de etapa — é a fonte da verdade.
- Copy sem VOC/mecanismo/prova/consciência = rascunho.
- Decisão reversível: escolha o caminho conservador e registre premissa em `07_LOGS/social-<cliente>.md`.
- Faltou dado não-bloqueante: use `[A PREENCHER]` e siga.
- Não invente métricas nem promessas de alcance. Trafego/números reais vêm do `traffic-analyst`.
