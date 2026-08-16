# ✅ Marketplace Auto-Publish — Configuração Ativa

**Data:** 2026-07-24  
**Status:** 🟢 ATIVO (sem revisão humana)  
**Executado por:** LaunchAgent `com.impar.marketplace-daily-publish`

---

## O que mudou

Anteriormente, o script `publish_daily_from_fila.py` rodava **SEM** a flag `--publish`, deixando todos os imóveis em status "rascunho_revisao_humana".

**Agora:** Rodando com `--publish`, publica automaticamente no Facebook Marketplace assim que o horário sugerido vencer.

---

## Configuração

### LaunchAgent
- **Arquivo:** `~/Library/LaunchAgents/com.impar.marketplace-daily-publish.plist`
- **Intervalo:** A cada 1 hora (3600 segundos)
- **Inicia ao boot:** Sim
- **Flags utilizadas:**
  - `--due` → publica apenas itens com horário já vencido
  - `--publish` → ATIVA a publicação real (antes era "rascunho")
  - `--max 2` → máximo 2 imóveis por rodada (evita bloqueio do Facebook)

### Logs
- **Sucesso:** `/Users/usuario/Library/Logs/impar-marketplace-publish.log`
- **Erro:** `/Users/usuario/Library/Logs/impar-marketplace-publish-error.log`

---

## Como funciona

1. **A cada hora**, o LaunchAgent dispara `publish_daily_from_fila.py`
2. O script verifica `fila-postagens.csv` para imóveis de **hoje**
3. Filtra apenas itens com `horario_sugerido` já vencido (`--due`)
4. Publica até **2 itens** no Facebook Marketplace (`--max 2`)
5. Registra em `marketplace-publicados-log.csv` com status "ok"
6. Aguarda ~60-120 segundos entre imóveis (humanização)
7. Próxima rodada em 1 hora

---

## Status Atual (2026-07-24)

Os 8 imóveis de hoje estão prontos. **Esperado:**
- Amanhã de madrugada: publicação do primeiro lote
- Próximas horas: publicação dos demais conforme horários vençam
- Log completo em `/Users/usuario/Library/Logs/impar-marketplace-publish.log`

---

## Comandos Úteis

### Ver logs em tempo real
```bash
tail -f ~/Library/Logs/impar-marketplace-publish.log
tail -f ~/Library/Logs/impar-marketplace-publish-error.log
```

### Verificar se está ativo
```bash
launchctl list | grep com.impar.marketplace-daily-publish
```

### Forçar execução imediata
```bash
launchctl start com.impar.marketplace-daily-publish
```

### Pausar temporariamente
```bash
launchctl unload ~/Library/LaunchAgents/com.impar.marketplace-daily-publish.plist
```

### Retomar
```bash
launchctl load ~/Library/LaunchAgents/com.impar.marketplace-daily-publish.plist
```

### Ver histórico de publicações
```bash
grep "ok" "/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv" | tail -20
```

---

## Troubleshooting

### Imóvel não foi publicado?
1. Verificar se `horario_sugerido` já venceu (flag `--due`)
2. Verificar se o código não está em `marketplace-publicados-log.csv` (evita duplicação)
3. Verificar logs para erros de login/bloqueio

### Bloqueio do Facebook
Se receber "bloqueado temporariamente", o script automaticamente para e tenta novamente na próxima rodada (+1 hora).

### Fotos não baixaram
O script pula imóveis sem fotos válidas (>1KB cada). Verificar URLs em `fila-postagens.csv`.

---

## Próximas Melhorias

- [ ] Webhook para notificar Jonata em WhatsApp ao publicar
- [ ] Dashboard com taxa de sucesso/erro por hora
- [ ] Escalação automática: aumentar `--max` se 0 erros em 5 rodadas
- [ ] Integrar com `crosspost_groups.py` (publicar em grupos 30 min após Marketplace)

---

**Ativado por:** Claude (2026-07-24 21:15 UTC)
