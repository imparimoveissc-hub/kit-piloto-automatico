# Automacao - Facebook Marketplace Impar

Fluxo em 2 camadas:

1. `generate_queue.py` monta a fila diaria do Marketplace com cadencia **humanizada** (7-10 posts/dia conforme tipo de dia: 7-9 fins de semana, 8-10 dias uteis).
2. `generate_group_queue.py` expande os imoveis em 19 publicacoes por imovel para grupos aprovados, com cadencia de 3 minutos.

## Regras operacionais

- Marketplace é a primeira publicacao de cada imovel.
- Grupos usam lista aprovada em `05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/grupos-aprovados.csv`.
- Se a lista de grupos nao estiver preenchida, o sistema usa placeholders `[A PREENCHER]` e bloqueia publicacao real.
- Fila diaria futura parte do dia seguinte por padrao.
- Cadencia entre posts é aleatoria (7-20 minutos) para parecer humana.

## Scripts principales

- `generate_queue.py` — coleta imoveis e gera fila diaria (Marketplace)
- `generate_group_queue.py` — expande fila em 19 grupos por imovel (aceita datas futuras)
- `run_group_publisher.sh` — launcher unico que prepara as filas e abre o publicador de grupos
- `run_full_pipeline.sh` — orquestra ambos em sequencia
- `publish_marketplace_playwright.py` — automacao de browser para publicacao (beta)

## Status atual

- [x] Fila diaria: pronta para datas futuras (via CLI/env)
- [x] Grupos: estrutura pronta, aguardando lista aprovada
- [x] Cadencia humanizada: 7-10 posts/dia (aleatoria conforme semana)
