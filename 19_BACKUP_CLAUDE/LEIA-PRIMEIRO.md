# 💾 Backup & Migração do Claude Code — Kit Piloto Automático V30

Este pacote copia o Claude Code inteiro (skills, config, tarefas agendadas,
ngrok, ambientes Python, video-use) do Mac atual para um Mac novo.

O Kit já vive no **iCloud Drive**, então ele sincroniza sozinho no Mac novo.
O que precisa de backup é o que fica **fora** do iCloud (a pasta `~/.claude`,
o token do ngrok e o repositório `video-use`). É isso que os scripts cuidam.

---

## 🟢 No Mac ATUAL (uma vez, antes de migrar)

No Claude Code, é só dizer:

> **Backup claude**

Ou, direto no Terminal:

```bash
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/backup-claude.sh
```

Isso gera a pasta `19_BACKUP_CLAUDE/snapshot/`. **Espere o iCloud terminar de
subir** (ícone de nuvem sem seta) antes de mexer no Mac novo.

---

## 🔵 No Mac NOVO (o comando único)

1. Faça login no **iCloud** (mesmo Apple ID) e espere o Kit baixar em
   `~/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB`.
2. Abra o **Terminal** e cole **este comando** — ele instala e restaura tudo:

```bash
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/instalar-nova-maquina.sh
```

O instalador coloca: Homebrew · Node · ngrok · git · gh · Python · uv ·
Claude Code CLI · navegadores do Playwright · restaura `~/.claude` (skills,
settings, plugins, tarefas agendadas, memória) · religa o `video-use` · monta
o ambiente do NF-em Joinville · reconfigura o token do ngrok.

### 3 passos manuais que sobram (precisam de login/interface)

1. **Logar:** rode `claude` dentro do Kit e digite `/login`.
2. **Reconectar MCPs/conectores** (WhatsApp, Filesystem, Meta, Composio,
   Google Drive…) pelo app Claude/Cowork → *Conectores*. Eles não migram por
   arquivo — é só reautorizar cada um.
3. **Meta Ads CLI** (se usar tráfego): rode a skill `/meta-cli-install`.

---

## ⚠️ Segurança

O snapshot e os `.env` do Kit contêm **credenciais** (Asaas, Meta, ngrok,
NF-em, API keys). Como ficam no iCloud, trate a conta Apple com 2FA e não
compartilhe a pasta. Se um dia quiser um backup **sem segredos**, apague
`19_BACKUP_CLAUDE/snapshot/envs/`, `snapshot/ngrok.yml` e os `.env` antes de
sincronizar.

## O que NÃO é copiado (de propósito)

- Histórico de sessões e cache do Claude (`~/.claude/sessions`, `cache`) — peso morto.
- `~/.claude.json` (contém `machineID`/login da máquina antiga) — recriado no `/login`.
- Conectores MCP — reautorizados pelo app (passo manual 2).
