---
modulo: marketplace
atualizado: 2026-08-19
---
status: ativo
pid_publisher: daemons manha/tarde/noite ativos — com.impar.marketplace-noite PID 25212 — último ok 2026-08-09 20:24 (2 publicados via run_daily_publish.sh)
pid_crosspost: LaunchAgent com.impar.crosspost — OPERACIONAL — 220 grupos marcados em 07/08 17:33 — slot 21:30 adicionado
ultimo_ok: publisher 2026-08-09 20:24 (2 pub: 3173213, 4312616); reativador 2026-08-10 16:06 (0 pub, 109 cooldown 20d, sem pendentes)
proximo: reativador roda a cada 30min/2h; publisher daemon-noite dispara às 18:00
fix_aplicado_2026-08-07: adicionado slot 21:30 ao LaunchAgent; 3 cloud tasks antigas (crosspost_groups_v2.py) desabilitadas; MAX_ITENS 5→20; seguir_publicador desativado
nota: impar-marketplace-publish-error.log tem erros de 09/08 09:16 de LaunchAgent antigo (sem wrapper FDA) — substituído por run_daily_publish.sh; não impacta operação atual
acao_pendente: nenhuma
ultima_mudanca: "marketplace-daily-publish.plist recriado e carregado no launchd — plist havia desaparecido, health-check falhava toda rodada"
