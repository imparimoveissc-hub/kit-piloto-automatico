# Configuração da Rotina - Messenger Marketplace (impar-messenger-inbox-hora)

## Status: ✅ ATIVO NO CODEX

No Codex, esta rotina roda como uma tarefa recorrente/manual com o browser in-app autenticado. A lógica continua a mesma, mas o ponto de entrada passa a ser a própria skill aberta na sessão do Codex.

## Rota Codex

- Abra a skill `impar-messenger-inbox-hora` no Codex.
- Confirme o browser in-app autenticado.
- Rode uma varredura completa da inbox de Venda.
- Registre o resumo em `07_LOGS/messenger-rodadas.md`.

## Legado local

O bloco abaixo fica como referência apenas para quem ainda roda o stack fora do Codex.

## Arquivos

- **Daemon plist:** `~/Library/LaunchAgents/com.impar.messenger-inbox-5min.plist`
- **Logs stdout:** `~/Library/Logs/impar-messenger-inbox-5min.log`
- **Logs stderr:** `~/Library/Logs/impar-messenger-inbox-5min-error.log`

## Comandos Úteis

### Verificar status
```bash
launchctl list | grep com.impar.messenger-inbox-5min
```

### Ver logs em tempo real
```bash
tail -f ~/Library/Logs/impar-messenger-inbox-5min.log
tail -f ~/Library/Logs/impar-messenger-inbox-5min-error.log
```

### Pausar daemon
```bash
launchctl unload ~/Library/LaunchAgents/com.impar.messenger-inbox-5min.plist
```

### Retomar daemon
```bash
launchctl load ~/Library/LaunchAgents/com.impar.messenger-inbox-5min.plist
```

### Forçar execução imediata
```bash
launchctl start com.impar.messenger-inbox-5min
```

## Intervalo

- **A cada 5 minutos** (300 segundos)
- **Inicia automaticamente** ao boot do Mac
- **Sem limite de horário** (24h/dia, 7 dias/semana)

## Executado por

Skill: `impar-messenger-inbox-hora` via Codex Browser / tarefa recorrente

## Data de Ativação

2026-07-20 10:55 -03 (Jonata)

## Próximas Melhorias

- [ ] Integrar logs com monitoramento remoto (Datadog/CloudWatch)
- [ ] Webhook de alerta para Slack/WhatsApp se erro > 3 rodadas consecutivas
- [ ] Dashboard de métricas (conversas/hora, leads/dia, taxa de resposta)
