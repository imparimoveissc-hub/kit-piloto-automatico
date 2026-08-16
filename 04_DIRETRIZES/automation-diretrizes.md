# Diretrizes de Automacao

## Regra principal

Automacao so melhora processo que ja tem objetivo claro. Se o processo estiver confuso, primeiro padronize.

## Classificacao de etapas

Cada etapa deve ser marcada como:

- `manual`: precisa de humano;
- `ai_assisted`: IA prepara, humano aprova;
- `automated`: pode rodar sozinha apos teste;
- `blocked`: falta dado/acesso ou risco alto.

## Ordem de desenho

1. Trigger.
2. Entradas.
3. Transformacoes.
4. Decisoes.
5. Saidas.
6. Handoff humano.
7. Ferramentas.
8. Teste.
9. Rollback.

## Riscos comuns

- enviar mensagem errada;
- atualizar CRM errado;
- expor dados pessoais;
- gerar promessa indevida;
- duplicar tarefa;
- entrar em loop;
- apagar ou sobrescrever arquivo;
- alterar campanha/anuncio;
- depender de credencial vencida.

## Padrao de entrega

Sempre entregar em modo `draft` ate o usuario confirmar ativacao.

Nunca pedir senha no chat.

## Para qualquer nicho

Use familia operacional antes de nicho especifico:

- servico local;
- profissional liberal;
- B2B consultivo;
- ecommerce;
- infoproduto;
- agencia/servico digital;
- clinica/saude;
- juridico/regulado.

