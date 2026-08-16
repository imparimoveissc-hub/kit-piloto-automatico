# Product Hardening

## Principio

Produto robusto e aquele em que a promessa publica, o onboarding, o atendimento, a automacao e a entrega real contam a mesma historia.

## Inventario de promessa

Classifique cada promessa da LP:

- resultado prometido;
- mecanismo;
- facilidade;
- velocidade;
- nivel de automacao;
- suporte;
- templates/documentos;
- economia de tempo;
- prova;
- garantia ou reducao de risco.

## Mapa de cobertura

| Status | Significado |
|---|---|
| `entregue` | existe fluxo/documento/produto que sustenta |
| `parcial` | existe, mas depende demais do operador |
| `manual` | so funciona com especialista humano |
| `nao_entregue` | promessa nao tem entrega correspondente |
| `sem_evidencia` | pode existir, mas nao foi comprovado |

## Prioridade

1. Promessa vendida e nao entregue.
2. Risco juridico, reputacional ou financeiro.
3. Falha que impede ativacao do usuario leigo.
4. Falha que exige conhecimento tecnico demais.
5. Automacao prometida que ainda depende de operador.
6. Refinamento cosmetico.

## Teste de usuario leigo

O produto deve funcionar para alguem que:

- nao sabe usar Claude bem;
- nao entende terminal;
- nao entende permissao de pasta;
- nao sabe o que e API/token/WSL;
- precisa de checklist simples;
- quer que o sistema diga o proximo passo.

Se depender de conhecimento tecnico escondido, abrir task de onboarding ou automacao.

