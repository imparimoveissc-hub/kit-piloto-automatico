# Command - mktplace 19 grupos tarde

> Rodada da tarde do Marketplace em modo Codex-first. Reaproveita a mesma lógica segura de crosspost dos grupos e aponta para o script unico `crosspost_groups_v2.py`.

## Triggers

- `mktplace 19 grupos tarde`
- `marketplace 19 grupos tarde`
- `mktplace tarde`
- `grupos tarde`
- `rodar grupos da tarde`

## Objetivo

Executar a rodada da tarde dos grupos do Marketplace da Impar no Codex, sem depender de comando do Claude Code, mantendo:

1. anuncio do dia ja publicado no Marketplace;
2. fila de grupos gerada;
3. lista aprovada de grupos preenchida;
4. dedupe diario ativo;
5. falha segura em login/checkpoint/captcha/bloqueio temporario.

## Como o Codex deve rodar

- Operar em pt-BR.
- Ler primeiro `05_WORKSPACE/current-context.md` e `07_LOGS/decisions.md`.
- Confirmar que a rotina do Marketplace esta no estado ativo para hoje.
- Usar o navegador e o ambiente local do Codex, nao o Claude Code.
- Nao tentar publicar se faltar anuncio do dia, se a fila estiver vazia ou se houver placeholders em `grupos-aprovados.csv`.

## Passo a passo

1. Confirmar o cap ativo do dia no `05_WORKSPACE/current-context.md`.
2. Abrir `05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/fila-grupos-postagens.csv`.
3. Validar se existem itens pendentes para a janela da tarde.
4. Validar que o anuncio do dia ja saiu no Marketplace.
5. Rodar o crosspost com o script unico:

```bash
python3 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/crosspost_groups_v2.py
```

6. Se a rodada precisar ser limitada, usar `--limit` e manter a cadencia do dia.
7. Registrar o resultado em `07_LOGS/decisions.md` e no ledger se houver alteracao de estado.

## Regras de seguranca

- Se o script parar com `SEM_ANUNCIO_DO_DIA`, nao retentar.
- Se aparecer `SESSAO_INVALIDA` ou `BLOQUEIO_TEMPORARIO`, encerrar a rodada.
- Nao tentar contornar overlay, captcha, checkpoint ou bloqueio por heuristica manual fora do script.
- Nao publicar em massa fora da fila aprovada.
- Nao mudar preco, promessa ou dados do anuncio nesta rotina.

## Saida esperada

Ao terminar, registrar:

- hora da rodada;
- quantidade de grupos ok;
- quantidade de falhas;
- motivo da parada, se houver;
- proxima acao.

