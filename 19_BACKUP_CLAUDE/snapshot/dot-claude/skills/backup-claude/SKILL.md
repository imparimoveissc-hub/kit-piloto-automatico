---
name: backup-claude
description: Faz o backup completo do Claude Code (skills, config ~/.claude, tarefas agendadas, memoria, ngrok, video-use, ambientes Python) para migrar para outra maquina. Use quando o usuario disser "Backup claude", "backup do claude", "fazer backup", "backup pra maquina nova", "migrar o claude", "instalar o kit em outro mac", "backup completo", ou variacoes. Gera o snapshot em 19_BACKUP_CLAUDE/snapshot/ dentro do Kit (que sincroniza via iCloud) e explica o comando unico de instalacao no Mac novo.
---

# Backup claude — migração para outra máquina

Sempre em pt-BR.

## O que fazer

1. Rode o script de backup do Mac atual:

   ```bash
   bash "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/backup-claude.sh"
   ```

   Ele recolhe o que fica FORA do iCloud: `~/.claude` (skills, settings,
   plugins, scheduled-tasks, memória), o authtoken do ngrok, o `.env` do
   `video-use`, os `.env` do Kit e um manifesto de versões. Salva tudo em
   `19_BACKUP_CLAUDE/snapshot/`.

2. Confirme para o usuário o que foi salvo (liste as skills e tarefas do
   snapshot) e lembre que o Kit inteiro já viaja pelo iCloud.

3. Explique o **comando único** para o Mac novo (depois do iCloud baixar o Kit):

   ```bash
   bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/instalar-nova-maquina.sh
   ```

4. Avise os 3 passos manuais que sobram no Mac novo: `/login` no Claude,
   reconectar os MCPs/conectores pelo app, e `/meta-cli-install` se usar tráfego.

## Regras

- Antes de rodar, cheque se `19_BACKUP_CLAUDE/` existe. Se não existir, os
  scripts precisam ser recriados (ver `LEIA-PRIMEIRO.md`).
- Nunca imprima os valores dos `.env` nem o authtoken no chat. Só confirme que
  foram copiados.
- Se o `video-use` (symlink em `~/.claude/skills/video-use`) apontar para uma
  pasta ausente, avise que a skill de vídeo será re-clonada do GitHub no Mac novo.
- Detalhes completos em `19_BACKUP_CLAUDE/LEIA-PRIMEIRO.md`.
