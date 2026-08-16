# Obsidian — Instalação em Nova Máquina

Guia de 4 etapas para configurar o Cofre KPA30 no Obsidian em qualquer Mac novo.
O passo 3 é executado automaticamente pelo `kos-install.sh`.

---

## Etapa 1 — Download

1. Acesse **obsidian.md** → clique em **Download for macOS**
2. Baixe o arquivo `.dmg` (ex.: `Obsidian-1.x.x-universal.dmg`)

> Versão mínima testada: 1.4.x. Usar sempre a versão mais recente.

---

## Etapa 2 — Instalação

1. Abra o `.dmg` baixado
2. Arraste o ícone do **Obsidian** para a pasta **Aplicativos**
3. Feche o instalador e ejete o `.dmg`
4. Abra o Obsidian uma primeira vez para aceitar os termos (se solicitado)
5. **Feche o Obsidian** antes de rodar o `kos-install.sh`

---

## Etapa 3 — Criar Cofre (automatizado)

O `kos-install.sh` faz isso automaticamente. Se precisar fazer manualmente:

```bash
VAULT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/Cofre-Obsidian"
KIT_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"

# 1. Criar pasta de configuração do vault
mkdir -p "$VAULT/.obsidian"

# 2. app.json — configurações básicas
cat > "$VAULT/.obsidian/app.json" << 'JSON'
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "current",
  "attachmentFolderPath": "Assets",
  "useMarkdownLinks": false,
  "newLinkFormat": "shortest",
  "readableLineLength": true,
  "strictLineBreaks": false,
  "foldHeading": true,
  "foldIndent": true
}
JSON

# 3. appearance.json — tema padrão
cat > "$VAULT/.obsidian/appearance.json" << 'JSON'
{
  "theme": "obsidian",
  "translucency": false
}
JSON

# 4. workspace.json — abre Brain Index direto
cat > "$VAULT/.obsidian/workspace.json" << 'JSON'
{
  "main": {
    "id": "brain-main",
    "type": "split",
    "children": [
      {
        "id": "brain-leaf",
        "type": "leaf",
        "state": {
          "type": "markdown",
          "state": {
            "file": "KPA30/Brain/00 - Índice Brain.md",
            "mode": "preview",
            "source": false
          }
        }
      }
    ],
    "direction": "vertical"
  },
  "left": {
    "id": "left-sidebar",
    "type": "split",
    "children": [
      {
        "id": "file-explorer",
        "type": "tabs",
        "children": [
          {
            "id": "file-explorer-leaf",
            "type": "leaf",
            "state": { "type": "file-explorer", "state": {} }
          }
        ]
      }
    ],
    "direction": "horizontal",
    "width": 260
  },
  "right": {
    "id": "right-sidebar",
    "type": "split",
    "children": [],
    "direction": "horizontal",
    "width": 0
  },
  "active": "brain-leaf",
  "lastOpenFiles": [
    "KPA30/Brain/00 - Índice Brain.md",
    "KPA30/Brain/Marketplace.md",
    "KPA30/Brain/Leads.md",
    "KPA30/Brain/Sistema.md",
    "KPA30/Brain/NFS-e.md",
    "KPA30/Brain/Contratos.md",
    "KPA30/00 - Índice KPA30.md"
  ]
}
JSON

# 5. Registrar vault no Obsidian
VAULT_ID=$(openssl rand -hex 8)
TS=$(python3 -c "import time; print(int(time.time() * 1000))")
mkdir -p "$HOME/Library/Application Support/obsidian"
cat > "$HOME/Library/Application Support/obsidian/obsidian.json" << JSON
{
  "vaults": {
    "${VAULT_ID}": {
      "path": "${VAULT}",
      "ts": ${TS},
      "open": true
    }
  },
  "updateDisabled": false,
  "hasOtherAppsRunning": false
}
JSON

echo "✅ Vault registrado. Abra o Obsidian."
```

---

## Etapa 4 — Teste de Funcionalidade

Após abrir o Obsidian, verifique:

| Verificação | Como checar | Esperado |
|-------------|-------------|----------|
| Vault reconhecido | Sidebar esquerda mostra `KPA30/` | ✅ |
| Brain Index aberto | Painel central mostra `00 - Índice Brain.md` | ✅ |
| Wikilinks funcionam | Clicar em `[[Marketplace]]` navega para a nota | ✅ |
| Callouts renderizados | `> [!success]` aparece em verde/colorido | ✅ |
| Interface em pt-BR | Menu "Arquivo", "Editar", etc. | ✅ |
| `core-plugins.json` criado | `ls Cofre-Obsidian/.obsidian/` mostra o arquivo | ✅ |

**Teste rápido via terminal:**
```bash
ls "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/Cofre-Obsidian/.obsidian/"
# Deve listar: app.json  appearance.json  core-plugins.json  workspace.json
```

Se `core-plugins.json` existir → Obsidian abriu e reconheceu o vault com sucesso.

---

## Solução de Problemas

| Problema | Causa provável | Solução |
|----------|----------------|---------|
| Obsidian abre vazio sem vault | `obsidian.json` não foi criado | Repetir passo 3 com Obsidian fechado |
| Wikilinks aparecem como texto | `.obsidian/` não existe | Criar a pasta e os JSONs do passo 3 |
| Vault aparece mas sem notas | Caminho errado no `obsidian.json` | Confirmar que o kit está sincronizado pelo iCloud |
| Interface em inglês | Obsidian não instalou o pacote de idioma | Configurações → Sobre → Idioma → Português (BR) |

---

## Referência

- Script de instalação completo: `kos-install.sh` (raiz do kit)
- Vault: `Cofre-Obsidian/KPA30/`
- Brain técnico (Claude): `00_OS/kos/brain/`
- Brain humano (Jonata): `Cofre-Obsidian/KPA30/Brain/`
