# Notas de Implementacao

## Decisao tecnica

O contato financeiro deve escrever apenas no endpoint local do app financeiro:

- `POST /api/transactions`

## Mecanismo de leitura

- Texto: usar diretamente.
- Audio: transcrever antes de extrair campos.
- Imagem/PDF: aplicar OCR antes de extrair campos.

## Dedupe

Fingerprint minimo por:

- sender;
- tipo da mensagem;
- texto normalizado;
- valor;
- data;
- descricao.

## Quando travar

- comprovante ilegivel;
- sem valor;
- sem contexto;
- PF/PJ incerto;
- fingerprint ja visto.

