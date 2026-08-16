# Command — instalar backup codex

> Restaura um backup completo do Kit Piloto Automatico V30 em um Mac novo e prepara o ambiente para Codex/Chrome/Facebook Marketplace.

## Triggers

- "instalar backup codex"
- "restaurar backup codex"
- "instalar backup kpa30"
- "vou instalar o codex em outro computador"
- "restaurar kit no mac novo"

## Objetivo final

Ao terminar, o Mac novo deve ter:

1. Pasta `Kit-Piloto-Automatico-V30-DISTRIB` restaurada.
2. Arquivos ocultos e operacionais preservados (`.env`, `.claude`, `.codex`, logs, automacoes, outputs).
3. Dependencias basicas conferidas: Git, Python 3, Node/npm.
4. Instrucoes para instalar Codex app/CLI e Codex Chrome Extension.
5. Checklist de validacao pos-restauracao.

## Regra de seguranca

O backup contem `.env` e pode conter tokens. Nao subir em pasta publica, WhatsApp, email sem criptografia ou repositorio Git.

## Comando recomendado no Mac novo

1. Copiar a pasta do backup para `Downloads`.
2. Abrir Terminal.
3. Rodar:

```bash
cd ~/Downloads/KPA30-backup-20260708-164031
bash install_backup_codex.sh
```

Se o backup estiver em outro caminho:

```bash
bash /caminho/para/KPA30-backup-20260708-164031/install_backup_codex.sh
```

## O que o script faz

- Localiza o arquivo `.tar.gz` do backup.
- Pergunta onde restaurar.
- Extrai a pasta completa.
- Confere se arquivos-chave existem:
  - `00_INDEX.md`
  - `00_OS/cos.md`
  - `.env`
  - `.claude/`
  - `.codex/`
  - `18_AUTOMATION_STACK/`
  - `07_LOGS/task-ledger.md`
- Gera `RESTORE-REPORT.md`.
- Mostra proximas acoes manuais.

## Pos-restauracao

Instalar no Mac novo:

- Codex app/CLI conforme o canal usado.
- Google Chrome.
- Codex Chrome Extension:
  <https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg>

Depois abrir o Codex na pasta restaurada e pedir:

```text
verificar instalacao backup codex
```

## Validacao minima

No Terminal, dentro da pasta restaurada:

```bash
pwd
ls 00_INDEX.md 00_OS/cos.md 07_LOGS/task-ledger.md
python3 --version
node --version
npm --version
```

## Limites

O script nao instala tokens, nao faz login no Facebook, nao instala extensoes do Chrome sozinho e nao configura permissoes sensiveis sem acao humana.

