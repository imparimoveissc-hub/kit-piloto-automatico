# DRE Mensal - Processo de entrega recorrente

> Pasta-mae do processo de entrega de DRE recorrente pros clientes finais.
> Tudo aqui e reutilizavel: muda cliente, muda mes, NAO muda o processo.
> Pra quem oferece servico contabil, controladoria terceirizada ou financeiro de cliente.

## Arquivos

| Arquivo | O que e | Quando usar |
|---|---|---|
| `SOP-entrega-dre.md` | Processo padrao em 8 etapas (captura -> envio) | Operacao mensal, treinamento de novo analista |
| `template-dre.md` | Estrutura do relatorio DRE + indicadores + insights | Base pra gerar o PDF de cada cliente todo mes |
| `email-template.html` | Email institucional bonitao em HTML | Disparo final pro cliente |
| `email-template-copy.md` | Versao texto + variaveis + diretrizes de tom | Fallback texto, copy reference, customizacao |
| `checklist-pre-envio.md` | QA gate antes de apertar "Enviar" | OBRIGATORIO antes de cada envio |

## Fluxo mensal resumido

```
Dia 1 a 3:    Captura de documentos
Dia 3 a 5:    Conciliacao bancaria
Dia 5 a 7:    Classificacao
Dia 7 a 8:    Geracao do DRE
Dia 8 a 9:    Analise e insights
Dia 9:        Revisao interna (checklist)
Dia 9 a 10:   PDF + email
Dia 10:       Envio
```

## Variaveis chave (preencher por cliente)

Mantidas como `{{MAIUSCULA}}` nos templates. Dicionario completo em `email-template-copy.md`.

Principais:
- `{{NOME_EMPRESA}}` `{{CNPJ}}` `{{PRIMEIRO_NOME_CLIENTE}}`
- `{{MES_REFERENCIA}}` `{{ANO_MES}}` `{{MES_PROXIMO}}`
- `{{NOME_ESCRITORIO}}` `{{EMAIL_INSTITUCIONAL}}` `{{DOMINIO_SITE}}`
- `{{RECEITA_BRUTA}}` `{{LUCRO_LIQUIDO}}` `{{MARGEM_EBITDA}}` `{{MARGEM_LIQUIDA}}`
- `{{VAR_RECEITA_MOM}}` `{{VAR_LUCRO_MOM}}`
- `{{INSIGHT_PRINCIPAL}}` `{{ACAO_1}}` `{{ACAO_2}}` `{{ACAO_3}}`

## Setup inicial (uma vez por escritorio)

Antes do primeiro disparo, fixar variaveis do SEU escritorio em um arquivo `meu-escritorio.yaml`:

```yaml
nome_escritorio: "[Nome do seu escritorio]"
contador_responsavel_padrao: "[Seu nome ou do socio]"
crc_padrao: "[CRC-UF XXXXXX/O-X]"
telefone_escritorio: "[(XX) XXXX-XXXX]"
whatsapp_escritorio: "[55XXXXXXXXXXX]"        # sem +
whatsapp_display: "[(XX) XXXXX-XXXX]"
endereco_escritorio: "[Rua, numero, sala - Cidade/UF]"
email_institucional: "[contato@seudominio.com.br]"
email_arquivo_bcc: "[arquivo@seudominio.com.br]"
link_agenda: "[https://cal.com/seuhandle]"
dominio_site: "[seudominio.com.br]"
identidade_visual:
  cor_primaria: "[hex da sua marca]"
  cor_secundaria: "[hex secundaria]"
```

Use esse arquivo pra preencher de uma vez as variaveis fixas nos templates (substitua no editor).

## Como customizar pra cada cliente

1. Copiar `template-dre.md` pra pasta do cliente em `05_WORKSPACE/clientes/[NomeCliente]/dre/[AAAA-MM]-dre.md`
2. Preencher campos `[A PREENCHER]` com os numeros do mes
3. Escrever 2-4 insights em linguagem do cliente (sem jargao contabil)
4. Gerar PDF (ver Etapa 7 do SOP)
5. Copiar `email-template.html` pra rascunho de email
6. Substituir `{{VARIAVEIS}}` (manual no Gmail/Outlook OU automatizado via Apps Script/Make/n8n)
7. Rodar `checklist-pre-envio.md` linha por linha
8. Enviar com aprovacao humana

## Automacao (proximo nivel)

A V30 sugere automatizar com:

- **Captura de extratos**: Gmail API + parsing PDF (draft, requer credencial)
- **Geracao do PDF**: Python + Jinja2 + WeasyPrint (draft, requer setup)
- **Disparo do email**: Gmail API com revisao manual antes do `Send` (manual, alto risco)
- **Arquivamento**: Google Drive API (draft, baixo risco)

Ver `18_AUTOMATION_STACK/agents/automation-orchestrator.md` pra desenhar a automacao quando estiver pronto.

## Status sugerido pro seu setup

- [ ] Variaveis do escritorio fixadas em `meu-escritorio.yaml`
- [ ] Primeiro cliente piloto definido
- [ ] PDF teste gerado com dados ficticios pra validar layout
- [ ] Email teste enviado pra contato interno (renderizacao em Gmail/Outlook/Apple Mail)
- [ ] Apos piloto OK, expandir pros demais clientes
- [ ] Integracao com sistema contabil (Omie / Conta Azul / Sage / outro)

## Proximos passos sugeridos

1. **Definir 1 cliente piloto** pra rodar o processo completo em [PROXIMO MES].
2. **Conferir variaveis fixas do seu escritorio** (endereco, CRC, whatsapp, link agenda) e fixar nos templates.
3. **Gerar PDF de teste** com dados ficticios pra validar layout.
4. **Enviar email teste pra contato interno** (nao cliente real) pra conferir renderizacao em Gmail/Outlook/Apple Mail.
5. **Apos piloto OK**, expandir pros demais clientes.
