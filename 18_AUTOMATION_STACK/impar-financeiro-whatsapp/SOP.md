# SOP - Assistente Financeiro Impar via WhatsApp

## Objetivo

Receber mensagens, audios e comprovantes no WhatsApp e transformar em lancamentos financeiros sem perder contexto e sem duplicar registros.

## Regra de trabalho

1. Texto entra direto na extracao.
2. Audio passa por transcricao.
3. Imagem e PDF passam por OCR/visao.
4. Se houver ambiguidade, perguntar do que se trata o comprovante.
5. Se houver clareza suficiente, salvar no financeiro local e responder com resumo.
6. Se houver risco de duplicidade, travar e pedir confirmacao.

## Respostas base

### Lancamento claro

"Entendi. Vou registrar como gasto de R$ [valor] em [data]. Se quiser, me diga se foi PJ ou PF."

### Comprovante ambiguo

"Consigo ler o comprovante, mas ainda nao entendi do que se trata. Foi gasto com o que?"

### Possivel duplicidade

"Esse comprovante parece ja ter sido registrado. Quer que eu revise antes de salvar de novo?"

## Campos que o lancamento precisa ter

- Valor.
- Data.
- Descricao curta.
- Categoria.
- PF ou PJ.
- Fingerprint do comprovante.

## Pontos de controle

- Sempre verificar duplicidade antes da escrita.
- Nunca salvar sem valor.
- Nunca inferir categoria quando a evidência for fraca.
- Nunca enviar dados sensiveis em texto aberto no WhatsApp.

## Handoff humano

Passar para Jonata quando:

- a leitura do comprovante estiver ruim;
- houver duas categorias possiveis;
- PF e PJ ficarem confusos;
- o valor for alto e sem contexto.

## Teste manual

1. Enviar texto com gasto claro.
2. Enviar audio com gasto claro.
3. Enviar foto de comprovante legivel.
4. Enviar comprovante sem contexto e verificar a pergunta de clarificacao.
5. Reenviar o mesmo comprovante e verificar a barreira de duplicidade.

## Status

Draft. Pronto para implementacao tecnica.

