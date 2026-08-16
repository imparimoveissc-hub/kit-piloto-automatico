# SOP - Entrega Mensal de DRE

Status: template
Owner: {{NOME_ESCRITORIO}}
Ultima revisao: [AAAA-MM-DD]

## Objetivo

Entregar, todo mes, ate o **dia util 10**, um relatorio de DRE (Demonstracao do Resultado do Exercicio) com analise financeira clara e acionavel para o cliente final, via email institucional + anexo PDF.

A entrega NAO e a planilha contabil crua. E um documento explicativo que traduz numeros em decisao.

## Quando usar

Todo dia 1 de cada mes a equipe inicia o ciclo de fechamento contabil do mes anterior. Trigger fixo: virada de mes + entrada de extratos bancarios.

## Entradas necessarias

- Extratos bancarios do mes (todas as contas PJ)
- Notas fiscais emitidas (saida) e recebidas (entrada)
- Folha de pagamento + DARFs/GFIP do mes
- Comprovantes de despesas operacionais
- Movimentacoes de estoque (se aplicavel)
- Acesso ao sistema contabil do cliente (Omie / Conta Azul / Sage / proprio)
- DRE do mes anterior (para comparativo MoM)
- DRE do mesmo mes do ano passado (para comparativo YoY)

## Passo a passo

### Etapa 1 - Captura (dia util 1-3)

1. Solicitar ao cliente, via email padronizado, os documentos do mes que ainda nao chegaram.
2. Conferir se todos os extratos bancarios estao baixados e legiveis.
3. Importar movimentacao bancaria pro sistema contabil.
4. Marcar status "Em apuracao" no controle interno.

### Etapa 2 - Conciliacao bancaria (dia util 3-5)

1. Conciliar cada lancamento bancario com nota fiscal ou comprovante.
2. Identificar e classificar transferencias entre contas (nao sao receita nem despesa).
3. Marcar pendencias (lancamentos sem documento fiscal) e pedir ao cliente.
4. Bloqueador: nao avancar com mais de 5% de lancamentos sem classificacao.

### Etapa 3 - Classificacao (dia util 5-7)

1. Classificar receitas por linha (produto/servico/canal).
2. Classificar despesas em CMV/CPV, Operacionais (Vendas, Administrativas, Financeiras), Nao operacionais.
3. Conferir provisoes (IRPJ, CSLL, INSS patronal, FGTS).
4. Aplicar depreciacao/amortizacao do mes (se houver imobilizado).

### Etapa 4 - Geracao do DRE (dia util 7-8)

1. Rodar relatorio DRE no sistema contabil.
2. Exportar pra planilha modelo (`template-dre.md` em formato XLSX).
3. Conferir totalizacao linha por linha.
4. Calcular indicadores: Margem Bruta, Margem Operacional, EBITDA, Margem Liquida.

### Etapa 5 - Analise e insights (dia util 8-9)

1. Comparar com mes anterior (MoM) e mesmo mes ano passado (YoY).
2. Identificar 3 maiores variacoes (positivas e negativas).
3. Escrever 2-4 insights em linguagem do cliente (sem jargao contabil).
4. Sugerir 1-3 acoes praticas baseadas nos numeros.

### Etapa 6 - Revisao interna (dia util 9)

1. Segundo analista revisa: numeros, classificacoes, insights, ortografia.
2. Aplicar `checklist-pre-envio.md`.
3. Se gate falhar, retornar pra etapa que falhou.

### Etapa 7 - Formatacao do entregavel (dia util 9-10)

1. Gerar PDF do DRE formatado (cabecalho {{NOME_ESCRITORIO}} + dados do cliente + tabela + indicadores + insights).
2. Nomear arquivo: `DRE_[NomeCliente]_[AAAA-MM].pdf`.
3. Salvar copia em `arquivo/clientes/[NomeCliente]/dre/`.

### Etapa 8 - Envio por email (dia util 10)

1. Abrir template `email-template.html`.
2. Preencher variaveis: nome do cliente, mes/ano, numeros chave, 1 insight principal.
3. Anexar PDF.
4. Rodar `checklist-pre-envio.md` linha por linha.
5. **Aprovacao humana obrigatoria** antes de apertar Enviar.
6. Disparar pelo email institucional `{{EMAIL_INSTITUCIONAL}}`.
7. Adicionar BCC `{{EMAIL_ARQUIVO_BCC}}` para registro.

## Saidas (entregaveis)

- PDF `DRE_[NomeCliente]_[AAAA-MM].pdf` (relatorio formatado)
- Email institucional disparado com anexo
- Registro interno: status "Entregue" + data + nome do revisor
- Pendencias do mes seguinte ja registradas

## Gates de qualidade

| Gate | Quando | Bloqueador |
|---|---|---|
| Conciliacao OK | Fim da Etapa 2 | >5% lancamentos sem classificacao |
| Revisao 4 olhos | Fim da Etapa 6 | Falha em qualquer item do checklist |
| Aprovacao final | Antes do Envio | Email teste nao confere com layout esperado |

## Anti-padroes (NAO fazer)

- Enviar DRE puro do sistema contabil sem analise
- Repetir mes anterior sem rever variacoes
- Usar jargao contabil no email (regime de competencia, ativo circulante, etc)
- Mandar para mais de 1 destinatario externo sem confirmar sigilo
- Pular o checklist por pressa de prazo
- Inventar insight sem base nos numeros

## Variantes

- **Cliente Simples Nacional**: usar template simplificado, sem provisao de IRPJ/CSLL detalhada
- **Cliente Lucro Real**: incluir apuracao trimestral + LALUR
- **Cliente em primeiro mes**: comparativo YoY fica `N/A`, dobrar atencao no comparativo MoM
- **Cliente sazonal**: incluir grafico de receita YoY pra contextualizar variacao

## Owners

- Contador responsavel pelo cliente: executa Etapas 3-5
- Analista contabil: executa Etapas 1-2 e 6 (revisao)
- Socio {{NOME_ESCRITORIO}}: aprova em casos de variacao MoM > 50% ou alerta tributario serio

## Quando este SOP precisa ser atualizado

- Mudanca na legislacao tributaria (revisar Etapa 3 e 5)
- Mudanca no sistema contabil padrao (revisar Etapa 1 e 4)
- Reclamacao de cliente sobre clareza do relatorio (revisar Etapa 5 e template)
- Erro tecnico detectado na entrega (revisar checklist Etapa 6)
