---
tipo: skill
origem: ambiente (não é arquivo do Kit)
status: ativa
---

# Skill — social-content-operator

Operador de conteúdo short-form para **TikTok, Instagram Reels e Stories**, do cronograma à publicação. **TikTok-first** (descoberta/alavancagem); adapta os vencedores para Reels (autoridade) e Stories (venda). Genérica multi-cliente.

## O que faz (ciclo completo)
1. **Intake** → brief do canal (nicho, ICP, pilares, voz, cadência).
2. **Estratégia + calendário mensal** (temas, pilares, objetivos, mix 40/30/30).
3. **Plano semanal + board `posts.csv`** (fonte da verdade do status).
4. **Kit por post** → ideia, hook, roteiro, visual, edição, legenda, texto de tela, CTA, hashtags, adaptação Reels/Stories, checklist.
5. **Edição** → aciona [[video-use]] (pipeline FFmpeg desta máquina).
6. **Publicação** → Modo A pacote pronto (default) ou Modo B auto-post via API em draft.

## Quando dispara
- "cronograma de postagem", "calendário editorial", "plano de conteúdo", "roteiro de reels", "conteúdo pro tiktok", "copy pra postar", "briefing de edição", "reaproveitar conteúdo", "adaptar reels pra tiktok", "hashtags", "agendar/postar", "estratégia de tiktok", "alavancar com tiktok".

## Onde vivem os arquivos
- Estado por cliente: `05_WORKSPACE/clientes/<cliente>/social/`
- Entregável final: `06_OUTPUTS/social-<cliente>/`
- Auto-post (draft): `18_AUTOMATION_STACK/social-autopost/`

## Regras-chave
- TikTok nativo primeiro, adaptação depois. Nunca repostar com marca d'água.
- Publicação real / API write (Modo B) exige confirmação — nunca posta sozinho.
- Copy sem VOC/mecanismo/prova/consciência = rascunho.

## Relacionadas
- [[video-use]]
- [[impar-imoveis-reels]]
- [[edicao-video-ffmpeg-cinema]]
- [[direct-response-br]]
