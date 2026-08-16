# Template: Automação via WhatsApp App Nativo do MacBook

**Arquivo:** whatsapp-app-nativo-macbook.md  
**Criado:** 2026-07-21  
**Baseado em:** Automação de Notificação de Leads (Impar Imóveis)  
**Reutilizável:** Sim — adapte texto, número destino e trigger

---

## Engenharia da Solução

### Princípio
Enviar mensagens automaticamente via WhatsApp Desktop (app nativo do macOS), **sem usar API, ponte ou conexão com o número destino**. O app já está logado em um número (ex: Jonata 5547996876631), que faz o envio.

### Componentes

| Componente | Função | Configurável |
|-----------|--------|--------------|
| Python script | Lógica, CLI, retry | ✅ Sim |
| URL scheme | `whatsapp://send?phone=...&text=...` | ✅ Sim |
| osascript + System Events | Automação keystroke (Enter) | ✅ Parcial |
| launchd (macOS daemon) | Disparo periódico (5 min, diário, etc) | ✅ Sim |
| Acessibilidade (macOS) | Permissão para osascript controlar teclado | ⚠️ Manual (setup inicial) |

### Fluxo Genérico

```
[GATILHO] 
  ↓
[LÓGICA PYTHON]
  ├─ Valida dados (telefone, mensagem)
  ├─ Formata URL scheme
  └─ Retry keystroke (3x)
  ↓
[URL SCHEME] open "whatsapp://send?phone=55...&text=..."
  ├─ Abre WhatsApp Desktop
  ├─ Preenche composer
  └─ Aguarda render (SEND_DELAY_S)
  ↓
[OSASCRIPT] keystroke return (3 tentativas)
  ├─ Valida frontmost (janela em foco)
  ├─ Tenta Enter (1s de delay entre tentativas)
  └─ Log status (success/failure)
  ↓
[LOG & RETRY]
  ├─ Success: registra em JSONL
  └─ Failure: grava no outbox (reprocessa depois)
```

---

## Padrão Python Genérico

```python
#!/usr/bin/env python3
"""Envia mensagens via WhatsApp Desktop nativo."""

import subprocess
import time
import urllib.parse
from pathlib import Path

WHATSAPP_PHONE_FROM = os.getenv("WHATSAPP_FROM", "5547996876631")  # quem envia (já logado)
WHATSAPP_PHONE_TO = os.getenv("WHATSAPP_TO", "5547920026017")      # quem recebe
SEND_DELAY_S = 5.0
WHATSAPP_PROCESS = "WhatsApp"

def send_whatsapp_native(message: str) -> tuple[bool, str]:
    """Envia via app nativo. Retorna (ok, status)."""
    
    # 1. Montar URL scheme
    url = f"whatsapp://send?phone={WHATSAPP_PHONE_TO}&text={urllib.parse.quote(message)}"
    
    # 2. Abrir WhatsApp
    try:
        subprocess.run(["open", url], check=True, timeout=15)
    except Exception as exc:
        return False, f"open_failed: {exc}"
    
    time.sleep(1)  # aguarda abertura
    
    # 3. Ativar janela
    subprocess.run(["osascript", "-e", f'tell application "{WHATSAPP_PROCESS}" to activate'])
    time.sleep(SEND_DELAY_S)
    
    # 4. Validar foco
    r = subprocess.run(
        ["osascript", "-e", 
         'tell application "System Events" to get name of first application process whose frontmost is true'],
        capture_output=True, text=True
    )
    if r.returncode != 0 or r.stdout.strip() != WHATSAPP_PROCESS:
        return False, f"focus_issue: {r.stdout.strip() or r.stderr.strip()}"
    
    # 5. Retry keystroke (3x)
    for tentativa in range(3):
        time.sleep(1)
        r = subprocess.run(
            ["osascript", "-e", 
             f'tell application "System Events" to tell process "{WHATSAPP_PROCESS}" to keystroke return'],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            return True, "sent_best_effort"
        if tentativa < 2:
            time.sleep(2)
    
    return False, f"keystroke_failed: {r.stderr.strip()}"
```

---

## Adaptações Comuns

### 1. **Mudar Número Destino**
```python
# De:
WHATSAPP_PHONE_TO = "5547920026017"  # Impar

# Para:
WHATSAPP_PHONE_TO = "5521987654321"  # Outro cliente
# Ou via env:
WHATSAPP_PHONE_TO = os.getenv("WHATSAPP_TO", "5521987654321")
```

### 2. **Mudar Texto da Mensagem**
```python
# De:
message = f"🔔 NOVO LEAD MARKETPLACE\n👤 Nome: {nome}\n..."

# Para:
message = f"📊 RELATÓRIO DIÁRIO\nVendas: {vendas}\n..."
# Ou:
message = f"⚠️ ALERTA\nCliente: {cliente}\n..."
```

### 3. **Mudar Trigger (Gatilho)**
```python
# De: a cada 5 min (launchd StartInterval 300)
# Para:

# Opção A: Diário (cron)
StartInterval = "0 9 * * *"  # 9h todo dia

# Opção B: Quando arquivo for criado (watch)
# Usar: watchdog, entr, ou verificação periódica em script

# Opção C: Via webhook (FastAPI, etc)
# Usar: API que recebe POST e dispara send_whatsapp()

# Opção D: Via MCP/Plugin
# Chamar send_whatsapp() de uma skill do Claude
```

### 4. **Mudar Fonte de Dados**
```python
# De: lê CSV local
rows = csv.DictReader(open("planilha.csv"))

# Para: API externa
response = requests.get("https://api.com/leads")
rows = response.json()["items"]

# Ou: Banco de dados
rows = db.query("SELECT * FROM leads WHERE notificado = false")

# Ou: Webhook que recebe dados
# (FastAPI recebe POST → enfileira para send_whatsapp)
```

### 5. **Mudar Cadência (launchd)**
```xml
<!-- De: a cada 5 minutos -->
<key>StartInterval</key>
<integer>300</integer>

<!-- Para: a cada 1 hora -->
<integer>3600</integer>

<!-- Ou: cron diário às 9h -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

---

## Pré-Requisitos (Sempre)

1. **Mac** (macOS 10.13+)
2. **Python 3** (padrão no macOS)
3. **WhatsApp Desktop** instalado e logado no número de ENVIO (ex: Jonata)
4. **Permissão de Acessibilidade** (passo manual: Ajustes > Privacidade > Acessibilidade > ativar Python/app)

---

## Instalação Rápida (Template)

```bash
# 1. Copiar script
cp seu-script.py ~/seu-projeto/

# 2. Copiar plist (adaptar Label)
cp seu-script.plist ~/.LaunchAgents/

# 3. Ativar
launchctl load -w ~/.LaunchAgents/seu-script.plist

# 4. Testar
~/seu-projeto/seu-script.py --test

# 5. Ver logs
tail -50f ~/Library/Logs/seu-script.log
```

---

## Limites & Proteções

| Limite | Padrão | Adaptável |
|--------|--------|-----------|
| Tentativas keystroke | 3 | ✅ Sim (for loop) |
| Delay entre tentativas | 2s | ✅ Sim (time.sleep) |
| Timeout launchd | 300s (5 min) | ✅ Sim (StartInterval) |
| Max mensagem | 4096 chars | ⚠️ WhatsApp nativo |
| Dedupe | por dia | ✅ Sim (JSON state) |
| Outbox retry | automático | ✅ Sim (loop flush) |

---

## Troubleshooting Universal

### Problema: "Mensagens escritas mas não enviadas"
**Causa:** Acessibilidade não concedida, ou macro do keystroke falhando.  
**Solução:** 
```bash
# Desabilitar/habilitar Acessibilidade
# (manual em Ajustes do Sistema)

# Ou testar osascript direto:
osascript -e 'tell app "System Events" to keystroke return'
# Se erro "não tem permissão", habilite Acessibilidade
```

### Problema: "launchd não está rodando"
**Causa:** plist com erro sintaxe, ou path inválido.  
**Solução:**
```bash
# Verificar sintaxe
plutil -lint ~/.LaunchAgents/seu-script.plist

# Recarregar
launchctl unload ~/.LaunchAgents/seu-script.plist
sleep 1
launchctl load -w ~/.LaunchAgents/seu-script.plist

# Ver status
launchctl list | grep seu-script
```

### Problema: "Erro de permissão no caminho"
**Causa:** Espaços no path não escapados no plist.  
**Solução:** Usar `/usr/bin/python3` direto no plist (sem intermediário shell).

---

## Exemplos de Reutilização

### Exemplo 1: Alertas de Venda (Diário)
```python
# Adapte:
message = f"🎉 VENDA FECHADA\nCliente: {cliente}\nValor: R$ {valor}\nCorretor: {corretor}"
WHATSAPP_PHONE_TO = "551199999999"  # supervisor
# Trigger: cron diário 18h (StartCalendarInterval Hour=18)
```

### Exemplo 2: Notificação de Feedback (Imediato)
```python
# Adapte:
message = f"⭐ FEEDBACK RECEBIDO\nCliente: {cliente}\nAvaliação: {estrelas}/5\nComentário: {texto}"
WHATSAPP_PHONE_TO = "554733333333"  # gerente qualidade
# Trigger: webhook (API que recebe POST do formulário)
```

### Exemplo 3: Status de Tarefas (Hora em hora)
```python
# Adapte:
message = f"📋 STATUS TAREFAS\n✓ Concluído: {done}\n⏳ Em andamento: {in_progress}\n⚠️ Bloqueado: {blocked}"
WHATSAPP_PHONE_TO = "5511988888888"  # líder squad
# Trigger: cron a cada hora (StartInterval 3600)
```

---

## Segurança & Boas Práticas

✅ **Fazer:**
- Usar env vars para telefones/configs sensíveis
- Logar tudo (timestamp, status, erro)
- Implementar dedupe (não enviar 2x)
- Retry automático (outbox)
- Testar com `--dry-run` antes de produção

❌ **Evitar:**
- Hardcoda telefone no código
- Enviar sem log
- Falhar silenciosamente (sempre registre erro)
- Ignorar Acessibilidade (vai falhar)
- Usar osascript sem proteção try/except

---

## Arquivos Gerados (Padrão)

```
seu-projeto/
├── seu-script.py                    # Script principal
├── seu-script.plist                 # Configuração launchd
├── logs/
│   ├── seu-script.jsonl             # Histórico de envios
│   ├── seu-script-outbox.jsonl      # Falhas pendentes (retry)
│   └── seu-script-state.json        # Estado (dedupe, etc)
└── README.md                        # Documentação
```

---

## Checklist para Reutilizar

- [ ] Copiar `notificar_lead_whatsapp.py` como base
- [ ] Adaptar `build_message()` com novo texto
- [ ] Mudar `WHATSAPP_PHONE_TO` para número destino
- [ ] Mudar `WHATSAPP_PHONE_FROM` se necessário (quem envia)
- [ ] Adaptar gatilho (launchd StartInterval / cron)
- [ ] Adaptar fonte de dados (CSV, API, DB, webhook)
- [ ] Testar com `--dry-run`
- [ ] Ativar Acessibilidade (setup manual)
- [ ] Testar com envio real (1 mensagem)
- [ ] Verificar logs
- [ ] Documentar adaptações em README local

---

**Pronto para clonar e adaptar!** 🚀
