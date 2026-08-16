---
name: meta-cli-install
description: Instala o Meta Ads CLI oficial no computador do mentorado. Cobre Windows (via WSL Ubuntu) e macOS/Linux nativo. Inclui Python 3.12+, uv, login OAuth, validação e setup do .env. Tudo em pt-BR. Trigger quando o usuário pedir pra instalar/configurar/setupar o Meta Ads CLI, ads-cli, "meta ads", ou disser que quer rodar a Traffic Stack mas a CLI ainda não está instalada.
---

# Skill: meta-cli-install

Esta skill é o **plano de execução** do slash command `/meta-cli-install` (definido em `.claude/commands/meta-cli-install.md`).

Quando ativado, siga **exatamente** o fluxo do command. Nunca pule:

1. Ler docs oficiais primeiro (WebFetch nas duas URLs do command)
2. Detectar plataforma
3. Em Windows: confirmar antes de instalar WSL
4. Python 3.12+ via método nativo do OS
5. `uv` da Astral
6. `uv tool install meta-ads-cli` (com fallbacks)
7. Wrapper `meta.cmd` (só Windows)
8. `meta auth login` (OAuth no browser)
9. `meta accounts list` (validação)
10. `cp .env.example .env` na raiz do kit
11. Smoke test
12. Resumo final pro mentorado

## Anti-padrões

- ❌ Pedir token manualmente pro mentorado
- ❌ Escrever token em arquivo dentro do kit
- ❌ Logar token em `06_OUTPUTS/` ou `07_LOGS/`
- ❌ Modificar `~/.profile` sem confirmar
- ❌ Instalar WSL sem confirmar
- ❌ Inventar comando se docs oficiais não cobrirem (sempre re-ler docs)

## Quando esta skill é ativada

Triggers diretos:
- "/meta-cli-install"
- "instala o meta cli"
- "preciso configurar o meta ads cli"
- "setup do ads cli"
- "como rodar a traffic stack" (se CLI ainda não estiver instalada)

Triggers indiretos (avaliar):
- Usuário roda `meta --version` e dá `command not found`
- Usuário tenta abrir o `PLAYBOOK.html` mas pergunta como começa
- Usuário fala "WSL", "Ubuntu", "Python 3.12" no contexto de tráfego

## Referência

- Command file: `.claude/commands/meta-cli-install.md`
- Docs oficiais: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started
- Playbook que usa essa CLI: `11_TRAFFIC_STACK/PLAYBOOK.html`
