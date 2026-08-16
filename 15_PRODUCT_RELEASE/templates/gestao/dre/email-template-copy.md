# Email DRE - Versao Copy (texto + variaveis)

> Use essa versao pra fallback texto puro, pra clientes que preferem email simples,
> ou como base do que vai dentro do HTML.
> Variaveis em `{{MAIUSCULAS}}` sao preenchidas no momento do disparo.

---

## Assunto

```
DRE {{MES_REFERENCIA}} - {{NOME_EMPRESA}} - Analise financeira {{NOME_ESCRITORIO}}
```

Alternativas (escolher por relacao com cliente):

- Formal: `DRE {{MES_REFERENCIA}} - {{NOME_EMPRESA}} | {{NOME_ESCRITORIO}}`
- Direto: `Seu DRE de {{MES_REFERENCIA}} chegou ({{NOME_EMPRESA}})`
- Insight no assunto (quando tem destaque): `{{NOME_EMPRESA}}: lucro liquido de {{MES_REFERENCIA}} cresceu {{VAR_LUCRO_MOM}}`

## Preview text (preheader)

```
Resumo do mes, indicadores e 3 acoes praticas pra {{MES_PROXIMO}}.
```

---

## Corpo (versao texto puro)

```
Ola, {{PRIMEIRO_NOME_CLIENTE}}.

Segue o fechamento financeiro de {{MES_REFERENCIA}} da {{NOME_EMPRESA}}.
O PDF anexo tem o relatorio completo. Abaixo o resumo do que mais importa
pra decisao nas proximas semanas.

RESUMO EXECUTIVO

Receita Bruta:   R$ {{RECEITA_BRUTA}}   ({{VAR_RECEITA_MOM}} vs mes anterior)
Lucro Liquido:   R$ {{LUCRO_LIQUIDO}}   ({{VAR_LUCRO_MOM}} vs mes anterior)
Margem EBITDA:   {{MARGEM_EBITDA}}%
Margem Liquida:  {{MARGEM_LIQUIDA}}%

INSIGHT DO MES

{{INSIGHT_PRINCIPAL}}

ACOES SUGERIDAS PRA {{MES_PROXIMO}}

1. {{ACAO_1}}
2. {{ACAO_2}}
3. {{ACAO_3}}

Pra revisar com voce, agenda 30 min comigo aqui: {{LINK_AGENDA}}
Prefere whatsapp? Responde esse email ou chama no {{WHATSAPP_DISPLAY}}.

ANEXO
DRE_{{NOME_EMPRESA_SLUG}}_{{ANO_MES}}.pdf - relatorio completo

Qualquer duvida, da o toque.

{{NOME_CONTADOR}}
{{CRC}} - {{NOME_ESCRITORIO}}
{{TELEFONE_ESCRITORIO}}
{{EMAIL_INSTITUCIONAL}}
```

---

## Variaveis (dicionario)

### Variaveis do cliente (mudam a cada disparo)

| Variavel | Tipo | Exemplo | Fonte |
|---|---|---|---|
| `{{PRIMEIRO_NOME_CLIENTE}}` | string | "Roberto" | Cadastro do cliente |
| `{{NOME_EMPRESA}}` | string | "Padaria Sao Joao Ltda" | Cadastro |
| `{{CNPJ}}` | string | "12.345.678/0001-90" | Cadastro |
| `{{MES_REFERENCIA}}` | string | "Abril/2026" | Periodo apurado |
| `{{MES_PROXIMO}}` | string | "Maio" | Calculado |
| `{{ANO_MES}}` | string | "2026-04" | Para nome de arquivo |
| `{{NOME_EMPRESA_SLUG}}` | string | "PadariaSaoJoao" | Para nome de arquivo |

### Variaveis do DRE (calculadas no mes)

| Variavel | Tipo | Exemplo | Fonte |
|---|---|---|---|
| `{{RECEITA_BRUTA}}` | currency | "187.450,00" | DRE linha 1 |
| `{{LUCRO_LIQUIDO}}` | currency | "23.870,00" | DRE linha 15 |
| `{{MARGEM_EBITDA}}` | numero | "18,4" | Calculado |
| `{{MARGEM_LIQUIDA}}` | numero | "12,7" | Calculado |
| `{{VAR_RECEITA_MOM}}` | string com sinal | "+12,3%" ou "-4,1%" | Calculado |
| `{{VAR_LUCRO_MOM}}` | string com sinal | "+8,7%" ou "-15,2%" | Calculado |
| `{{COR_RECEITA}}` | hex | "#1a7f3c" (verde) ou "#b3261e" (vermelho) | Derivado do sinal |
| `{{COR_LUCRO}}` | hex | idem | idem |
| `{{INSIGHT_PRINCIPAL}}` | string | 2-4 linhas | Analise contador |
| `{{ACAO_1}}` `{{ACAO_2}}` `{{ACAO_3}}` | string | 1 linha cada | Analise contador |

### Variaveis fixas do escritorio (definir 1 vez)

| Variavel | Tipo | Exemplo | Fonte |
|---|---|---|---|
| `{{NOME_ESCRITORIO}}` | string | "[Nome do seu escritorio]" | Setup |
| `{{NOME_CONTADOR}}` | string | "[Nome do contador responsavel]" | Setup por contador |
| `{{CRC}}` | string | "CRC-SP 1XXXXX/O-X" | Setup por contador |
| `{{TELEFONE_ESCRITORIO}}` | string | "(11) 4002-8922" | Setup |
| `{{WHATSAPP_ESCRITORIO}}` | string | "5511999998888" (sem +) | Setup |
| `{{WHATSAPP_DISPLAY}}` | string | "(11) 99999-8888" | Setup |
| `{{ENDERECO_ESCRITORIO}}` | string | "Av. Principal, 1234, sala 56 - Cidade/UF" | Setup |
| `{{LINK_AGENDA}}` | url | "https://cal.com/seuhandle/dre-revisao" | Setup |
| `{{EMAIL_INSTITUCIONAL}}` | string | "contato@seudominio.com.br" | Setup |
| `{{EMAIL_ARQUIVO_BCC}}` | string | "arquivo@seudominio.com.br" | Setup |
| `{{DOMINIO_SITE}}` | string | "seudominio.com.br" | Setup |
| `{{COR_PRIMARIA}}` | hex | "#0f2a45" | Identidade visual |

---

## Diretrizes de tom

- **Tom**: profissional mas humano. Nao corporativo congelado, nao casual demais.
- Tratamento: voce (nunca tu, nem "prezado").
- Frases curtas. Quebra de linha pra respirar.
- Sem jargao contabil no corpo do email. Jargao fica no PDF anexo se necessario.
- Numero antes da palavra: "Lucro caiu R$ 8 mil" e melhor que "Houve queda no lucro".
- Acao sempre concreta: "renegociar contrato com fornecedor X" e melhor que "revisar custos".
- Zero emoji no corpo. Emoji so em CTA visual no HTML (anexo, etc).

---

## Variantes do insight principal

### Quando lucro cresceu
> "Voce fechou {{MES_REFERENCIA}} com lucro liquido de R$ {{LUCRO_LIQUIDO}}, {{VAR_LUCRO_MOM}} acima de {{MES_ANTERIOR}}. O motivo principal foi [causa]. Vale manter o ritmo de [acao que funcionou] em {{MES_PROXIMO}}."

### Quando lucro caiu
> "Sua margem liquida foi de {{MARGEM_LIQUIDA_ANTERIOR}}% pra {{MARGEM_LIQUIDA}}% esse mes. Mesmo com receita {{COMPORTAMENTO_RECEITA}}, sobrou menos no final por causa de [causa]. Sugestao: olhar pra [acao] antes do fechamento de {{MES_PROXIMO}}."

### Quando receita explodiu
> "Receita bruta cresceu {{VAR_RECEITA_MOM}} esse mes, puxada por [linha/canal]. Atencao: gasto operacional acompanhou e a margem ficou em {{MARGEM_LIQUIDA}}%. Pra escalar sem perder rentabilidade, vale [acao]."

### Quando tem alerta tributario
> "Identifiquei {{ALERTA_TRIBUTARIO}} esse mes. Risco: [consequencia]. Acao imediata: [acao]. Posso resolver junto com voce em uma call de 30 min."

### Quando esta estavel
> "{{MES_REFERENCIA}} fechou em linha com {{MES_ANTERIOR}}: receita estavel, margem estavel, lucro estavel. Negocio rodando saudavel. Proxima fronteira pra voce e [oportunidade identificada]."

---

## Anti-padroes (NAO usar)

- "Prezado cliente" (frio)
- "Conforme solicitado, segue em anexo" (burocratico)
- "Estamos a disposicao" (vazio)
- "Aproveito a oportunidade pra" (rodeio)
- "Em caso de duvidas nao hesite em contatar-nos" (corporativo)
- "Atenciosamente," sozinho como fecho (impessoal)
- Numeros sem contexto: "Sua receita foi R$ X" sem dizer o que isso significa
- Lista de indicadores sem interpretacao: o que o cliente faz com 4 margens sem saber o que cada uma significa pra ele?

---

## Versionamento da copy

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Estrutura inicial - resumo executivo + insight + acoes + CTA |
