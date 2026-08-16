# Familia — Ecommerce

## Contexto

Operacao com produto, pedidos, duvidas, abandono, troca, suporte e pos-venda.

## Primeira tarefa util

Criar fluxo de atendimento para duvidas antes da compra.

```text
/whatsapp-system
Objetivo: atendimento ecommerce para duvidas de produto e carrinho.
```

## Automacao sugerida

Nome: recuperacao de carrinho e duvida de produto.

Trigger: cliente pergunta no WhatsApp ou abandona carrinho.

Fluxo:

1. identificar produto;
2. responder duvida com base em catalogo;
3. confirmar disponibilidade/prazo se houver fonte;
4. oferecer link de compra;
5. acionar humano para desconto, reclamacao, troca ou caso sem resposta.

## WhatsApp sugerido

```text
Oi, [NOME]. Me manda o nome ou print do produto que voce quer ver e eu te ajudo com:

1. duvidas principais;
2. prazo/entrega, se estiver disponivel;
3. link certo para comprar.
```

## Squad inicial

- CoS;
- WhatsApp Orchestrator;
- Customer Success Bot;
- Automation Architect;
- QA Editor.

## Riscos

- informar estoque/prazo sem fonte;
- prometer desconto;
- tratar troca/devolucao sem politica;
- expor dados do pedido.

## Comandos recomendados

- `/setup-nicho`
- `/whatsapp-system`
- `/automatizar-processo`
- `/relatorio`

