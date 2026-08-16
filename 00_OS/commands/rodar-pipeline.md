# Command - rodar-pipeline

## Objetivo

Executar o pipeline V30 quando a demanda exigir varias fases.

## Passos

1. Confirmar que a demanda e pipeline, nao peca avulsa.
2. Ler `01_PIPELINE/kpa-v30-pipeline.yaml`.
3. Criar tasks P0 a P7 no ledger, mas marcar como `blocked` as que dependem de gate anterior.
4. Executar P0 e P1.
5. Avancar fase por fase.
6. So liberar P5 paralelo quando `GATE-COPY` passar.

## Regra

Se uma fase falhar 3 vezes, parar e voltar a fase anterior. Nao insistir em output caro com base ruim.
