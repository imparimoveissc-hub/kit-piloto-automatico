---
name: backup-migracao-claude
description: "Pacote de backup/migração do Claude Code para Mac novo — skill \"backup-claude\" + pasta 19_BACKUP_CLAUDE"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6d479272-b8a5-45ba-b898-5087fa121989
---

Backup completo do Claude Code para migrar de Mac vive em `19_BACKUP_CLAUDE/` no Kit (iCloud).

- **Mac atual:** dizer "Backup claude" (skill `backup-claude`) ou rodar `19_BACKUP_CLAUDE/backup-claude.sh` → gera `snapshot/` com ~/.claude (skills, settings, plugins, scheduled-tasks, memória), ngrok.yml, .env do Kit e do video-use, manifesto de versões.
- **Mac novo (comando único):** `bash .../19_BACKUP_CLAUDE/instalar-nova-maquina.sh` — instala brew/node/ngrok/git/gh/python/uv/Claude CLI/Playwright, restaura ~/.claude (reescreve /Users/user→$HOME), religa video-use (clona de github.com/browser-use/video-use), monta venv do NF-em, reconfigura authtoken ngrok.
- **3 passos manuais no Mac novo:** `/login` no Claude, reconectar MCPs/conectores pelo app, `/meta-cli-install`.

Contexto: usuário comprou MacBook novo (jul/2026). Kit inteiro já viaja pelo iCloud; scripts cuidam só do que fica fora dele. Passo a passo em `19_BACKUP_CLAUDE/LEIA-PRIMEIRO.md`.
