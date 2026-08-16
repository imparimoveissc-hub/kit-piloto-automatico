---
name: follow-up
description: Gera mensagens de follow-up adaptadas ao contexto
---

# /follow-up — Mensagens de Follow-up

## Processo

### 1. Identificar contexto
Pergunte: "Qual o tipo de follow-up?"

Opcoes:
1. Pos-reuniao
2. Pos-proposta
3. Pos-entrega
4. Cobranca (pagamento)
5. Reativacao (cliente sumiu)
6. Pedido de depoimento

### 2. Gerar mensagens (3 variacoes cada)

**Pos-reuniao:**
```
Variacao 1 (mesmo dia):
Oi [nome], obrigado pela reuniao. Conforme combinamos, vou [proximo passo]. Te mando [entregavel] ate [data]. Qualquer coisa, estou aqui.

Variacao 2 (dia seguinte):
[nome], passando pra reforcar os pontos da nossa conversa. Os proximos passos sao: 1) [passo 1] 2) [passo 2]. Alguma duvida?

Variacao 3 (3 dias depois, sem resposta):
Oi [nome], tudo certo? So passando pra ver se ficou alguma duvida sobre o que conversamos. Estou a disposicao.
```

**Pos-proposta:**
```
Variacao 1 (2 dias):
[nome], enviei a proposta [dia]. Conseguiu dar uma olhada? Se tiver alguma duvida sobre os planos ou condições, me fala que explico.

Variacao 2 (5 dias):
Oi [nome], passando pra saber se teve chance de avaliar a proposta. Tem algum ponto que gostaria de ajustar?

Variacao 3 (7 dias, break-up):
[nome], como nao tive retorno, imagino que o timing nao foi o ideal. Sem problema. Fico a disposicao caso queira retomar no futuro. Abraco!
```

**Pos-entrega:**
```
Variacao 1 (1 dia):
[nome], enviei a entrega ontem. Conseguiu ver? Algum ajuste necessario?

Variacao 2 (3 dias):
Oi [nome], passando pra saber o que achou da entrega. Feedback e importante pra gente manter a qualidade.

Variacao 3 (7 dias):
[nome], tudo bem? Nao recebi retorno sobre a ultima entrega. Esta tudo certo ou precisa de algum ajuste?
```

**Cobranca:**
```
Variacao 1 (lembrete gentil):
Oi [nome], tudo bem? Passando pra lembrar que o pagamento referente a [servico/periodo] vence em [data]. Segue os dados: [pix/boleto].

Variacao 2 (vencido):
[nome], o pagamento de [valor] referente a [periodo] esta em aberto desde [data]. Pode verificar? Qualquer dificuldade, me fala que a gente resolve.

Variacao 3 (10+ dias):
Oi [nome], o pagamento de [periodo] continua pendente. Preciso resolver essa questao pra dar continuidade ao projeto. Podemos conversar?
```

**Reativacao:**
```
Variacao 1 (sumiu ha 30 dias):
[nome], tudo bem? Faz um tempo que a gente nao se fala. Como estao as coisas por ai? Se precisar de algo, estou aqui.

Variacao 2 (sumiu ha 60 dias):
Oi [nome], passando pra dar um oi. Tenho novidades que podem te interessar: [novidade relevante]. Quer bater um papo rapido?

Variacao 3 (sumiu ha 90+ dias):
[nome], quanto tempo! Espero que esteja tudo bem. Estou com [novidade/promocao] e lembrei de voce. Se fizer sentido, me fala que te explico.
```

**Pedido de depoimento:**
```
Variacao 1:
[nome], estou organizando alguns cases de resultado. O trabalho que fizemos juntos teve resultado muito bom. Voce toparia me mandar um depoimento curto (pode ser por audio) contando como foi a experiencia?

Variacao 2:
Oi [nome], posso te pedir um favor rapido? Estou montando prova social pro meu trabalho. Um depoimento seu de 30 segundos (audio ou texto) faria muita diferenca. Pode ser bem simples: o que mudou, qual resultado voce viu.
```

### 3. Sugerir timing

| Tipo | Quando enviar |
|------|--------------|
| Pos-reuniao | Mesmo dia + dia seguinte + 3 dias |
| Pos-proposta | 2 dias + 5 dias + 7 dias (break-up) |
| Pos-entrega | 1 dia + 3 dias + 7 dias |
| Cobranca | Dia do vencimento + 3 dias + 10 dias |
| Reativacao | 30 dias + 60 dias + 90 dias |
| Depoimento | Apos resultado concreto |
