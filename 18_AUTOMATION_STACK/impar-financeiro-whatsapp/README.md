# Assistente Financeiro Impar via WhatsApp

Versao tecnica do contato financeiro:

- recebe texto, audio, imagem e PDF;
- extrai valor, data e contexto;
- pergunta o que o comprovante representa quando estiver ambiguo;
- grava apenas lancamentos confirmados no financeiro local;
- evita duplicidade com fingerprint do comprovante.

## Fluxo tecnico

```text
WhatsApp
  -> bridge local / webhook
  -> normalizacao de mensagem
  -> transcricao de audio
  -> OCR/visao do comprovante
  -> extracao de campos
  -> regra de confianca
  -> pergunta de confirmacao, se preciso
  -> POST /api/transactions
  -> resposta resumida no WhatsApp
```

## Pecas

- `automation-blueprint.yaml`: mapa de processo e riscos.
- `SOP.md`: operacao humana e assistida.
- `src/`: scaffold tecnico da ponte.
- `docs/`: contrato de entrada, saida e testes.

## Integracao alvo

O destino da escrita e a API local do app financeiro:

- `POST /api/transactions`
- `PATCH /api/transactions/:id`
- `GET /api/state`

## Status

`draft`. Nao ativado em producao.

## Uso recomendado

- Contato sugerido: `Assistente Financeiro Impar`
- Origem inicial: seu WhatsApp pessoal logado
- Entrada aceita: texto, audio, imagem e PDF
- Regra principal: perguntar quando o comprovante nao estiver claro
- Fluxo operacional pronto em `05_WORKSPACE/clientes/jonata-impar/whatsapp/assistente-financeiro.md`
- Captura diaria em `05_WORKSPACE/clientes/jonata-impar/whatsapp/captura-diaria-comprovantes.md`
