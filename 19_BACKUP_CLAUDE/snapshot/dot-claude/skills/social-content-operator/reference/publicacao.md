# Publicação — Modo A (pacote pronto) e Modo B (auto-post draft)

## Modo A — Pacote pronto para postar (default, zero setup)

Entregue por post um "cartão de publicação" copiável:

```
POST <id> — <canal> — <data> <horário sugerido>

🎬 Vídeo: 05_WORKSPACE/clientes/<cliente>/social/criativos/<id>.mp4
📝 Legenda:
<copy da caption, com quebras e CTA no fim>

#️⃣ Hashtags:
<bloco de hashtags do canal>

🖊️ Texto de tela: <resumo do que aparece no vídeo>
🎯 CTA: <ação única>
📌 Capa (Reels): <arquivo/descrição>
```

Fluxo recomendado:
1. Publique **primeiro no TikTok**.
2. Leia o sinal das primeiras 1–2h (views vs. média do perfil).
3. Só então dispare a adaptação Reels/Stories dos que engancharam.
4. Atualize `status` no `posts.csv`: `agendado` → `publicado`.

Horários default (calibre pelos insights do perfil): TikTok 12h e 19h; Reels 12h e 18h;
Stories manhã + fim de tarde.

---

## Modo B — Auto-post via API (draft até validar)

**Só documentar/rodar sob confirmação explícita.** Publicação real, API write e disparo
exigem OK do usuário (política full-auto V30). Estrutura em
`18_AUTOMATION_STACK/social-autopost/` (criar como draft quando o usuário pedir).

### Instagram Reels — Graph API
Requisitos:
- Conta **Instagram Business ou Creator** vinculada a uma Página do Facebook.
- App no Meta for Developers com produto **Instagram Graph API** e permissões
  `instagram_content_publish`, `instagram_basic`, `pages_read_engagement`.
- Long-lived access token no `.env`.

Fluxo (2 passos): criar container de mídia (`POST /{ig-user-id}/media` com `media_type=REELS`,
`video_url`, `caption`) → publicar (`POST /{ig-user-id}/media_publish` com o `creation_id`).
O vídeo precisa estar em URL pública (hospedar antes). Stories usam `media_type=STORIES`.

### TikTok — Content Posting API
Requisitos:
- App aprovado no **TikTok for Developers** com escopo `video.publish` / `video.upload`.
- Conta habilitada (Content Posting API tem allowlist/aprovação por caso de uso).
- OAuth do usuário + refresh token no `.env`.

Fluxo: iniciar upload (`/v2/post/publish/video/init/`) → enviar o arquivo → publicar com
metadados (título, privacidade). Direct Post exige conta aprovada; caso contrário só rascunho
que o usuário confirma no app.

### Regras do Modo B
- Nasce em `DRY_RUN=true` (simula, não publica).
- Nunca dispara sem o usuário mandar rodar naquela execução.
- Loga cada publicação em `07_LOGS/social-<cliente>.md` com id, canal, timestamp e status.
- Falha de token/permissão → parar e reportar, nunca tentar em loop.
