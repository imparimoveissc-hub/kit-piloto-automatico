# Quality Gates V30

Gates existem para impedir retrabalho caro. Cada gate deve devolver problemas especificos e correcoes concretas.

Use `00_OS/gate-matrix.md` para severidade, score, verdict e escalada.

## Contrato de resposta

```yaml
verdict: pass | concerns | fail
score: 0-10
specific_issues:
concrete_fixes:
blocked_next_step: true | false
severity: S0 | S1 | S2 | S3 | S4
```

## GATE-INTAKE

Passa quando:

- objetivo esta claro;
- output esperado esta nomeado;
- premissas estao registradas;
- proxima etapa tem owner.

## GATE-RESEARCH

Passa quando:

- ha VOC literal suficiente para o tamanho da task;
- quotes tem origem;
- dores, desejos, objecoes e linguagem estao separados;
- ha pelo menos 3 "quotes ouro" para copy.

## GATE-STRATEGY

Passa quando:

- publico e awareness estao definidos;
- DRE dominante esta claro;
- MUP e MUS estao separados;
- promessa tem mecanismo;
- prova disponivel sustenta a promessa;
- a Big Idea passa no teste: especifica, emocional, defensavel, memoravel.

## GATE-COPY

Passa quando:

- copy usa linguagem do publico, nao linguagem generica;
- promessa sem mecanismo foi eliminada;
- prova tem nome, numero ou detalhe concreto quando disponivel;
- headline passa por 4 U's: util, urgente, unica, ultra-especifica;
- troca o nicho/profissao e ainda funciona? Se sim, falha por genericidade;
- voz pt-BR esta natural e sem cara de IA;
- sem travessao longo em copy final;
- CTA tem acao clara e motivo para agir agora.

## GATE-PRODUCTION

Passa quando:

- asset segue copy aprovada;
- mobile e legibilidade foram considerados;
- hierarquia visual favorece a acao principal;
- arquivos finais tem nomes claros;
- specs de publicacao estao presentes.

## GATE-TRAFFIC

Passa quando:

- campanha tem objetivo mensuravel;
- evento de conversao esta definido;
- criativos tem hipotese de teste;
- publico e budget fazem sentido;
- plano de leitura de dados esta definido antes de subir.

## GATE-WHATSAPP

Passa quando:

- objetivo da conversa esta claro;
- oferta, publico e restricoes foram considerados;
- mensagens sao curtas e naturais no celular;
- existe regra de handoff humano;
- existem stop rules e opt-out quando aplicavel;
- bot nao finge ser humano;
- nao ha promessa, preco, prazo, desconto ou prova inventada;
- docs Cowork estao em modo `draft` ate ativacao real;
- disparo real ou automacao ativa exige confirmacao humana.

## GATE-AUTOMATION

Passa quando:

- objetivo e trigger do processo estao claros;
- entradas, saidas e responsaveis foram nomeados;
- etapas manuais, assistidas, automaticas e bloqueadas foram separadas;
- ferramentas, acessos e dados necessarios estao listados;
- existe handoff humano;
- existe plano de teste antes de ativar;
- existe rollback;
- tudo esta em modo `draft` ate confirmacao;
- nenhum envio, API write, CRM update, budget, publicacao ou acao irreversivel roda sem confirmacao humana.

## GATE-PRODUCT

Passa quando:

- claims da LP foram inventariados;
- cada promessa tem entrega correspondente ou gap marcado;
- usuario leigo consegue entender o proximo passo;
- automacoes prometidas tem fluxo, documento ou limite explicito;
- gaps de produto estao priorizados por severidade;
- claims fortes tem prova ou `[A PREENCHER]`.

## GATE-NICHE-KIT

Passa quando:

- dores, objeções, restricoes e provas sao especificas do nicho;
- nao substitui VOC real;
- WhatsApp, SDR e CS estao adaptados ao ciclo de venda do nicho;
- comandos do squad reduzem friccao de usuario leigo;
- riscos regulatorios do nicho estao mapeados;
- existe demo ou fluxo piloto antes de marcar como estavel.

## GATE-DELIVERY

Passa quando:

- entregaveis prometidos existem;
- handoff final tem proximos passos;
- gaps estao marcados como `[A PREENCHER]` ou bloqueios;
- ledger esta atualizado.
