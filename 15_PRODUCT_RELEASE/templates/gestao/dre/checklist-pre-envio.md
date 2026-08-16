# Checklist Pre-Envio - DRE Mensal

> Aplicar ANTES de apertar "Enviar". Nenhum item marcado em "vermelho" -> NAO envia.
> Quem responde: contador responsavel + revisor (2 olhos).

---

## 1. Conferencia dos numeros

- [ ] Receita Bruta bate com soma das notas fiscais emitidas no periodo
- [ ] Deducoes batem com tributos sobre vendas + devolucoes documentadas
- [ ] CMV/CPV bate com baixa de estoque + custo de servico do periodo
- [ ] Despesas operacionais batem com extratos + comprovantes
- [ ] Resultado financeiro bate com extratos bancarios (juros, tarifas, rendimentos)
- [ ] IRPJ/CSLL calculados conforme regime tributario do cliente
- [ ] Lucro Liquido fecha com somatoria vertical da DRE
- [ ] Saldo de caixa no fim do mes bate com extrato consolidado

**Bloqueador**: divergencia acima de R$ 100 sem justificativa -> NAO envia.

---

## 2. Indicadores e analise

- [ ] 4 margens calculadas (Bruta, Operacional, EBITDA, Liquida)
- [ ] Comparativo MoM (mes vs mes anterior) presente
- [ ] Comparativo YoY (mes vs mesmo mes ano passado) presente
- [ ] Top 3 variacoes positivas identificadas com causa
- [ ] Top 3 variacoes negativas identificadas com causa
- [ ] Pelo menos 2 insights escritos em linguagem do cliente
- [ ] Pelo menos 2 acoes praticas sugeridas com prazo

**Bloqueador**: variacao MoM acima de 30% em alguma linha sem explicacao -> NAO envia.

---

## 3. Alertas e atencao

- [ ] Tributos do mes estao pagos OU prazo de pagamento informado no email
- [ ] Folha de pagamento esta paga ou com data confirmada
- [ ] Sem lancamentos sem documento fiscal acima de R$ 500
- [ ] Cliente NAO esta proximo do teto do Simples Nacional sem aviso
- [ ] Caso esteja, alerta escrito explicitamente no insight
- [ ] Nenhum dado de outro cliente vazou pro relatorio (revisar 2x)

**Bloqueador critico**: vazamento de dado de outro cliente -> NAO envia, retrabalha.

---

## 4. Documento (PDF)

- [ ] Cabecalho com logo {{NOME_ESCRITORIO}} + nome do cliente + CNPJ
- [ ] Periodo de referencia visivel no topo (AAAA-MM)
- [ ] Data de emissao + nome do contador + CRC no rodape
- [ ] Tabela DRE legivel (nao corta colunas em A4 retrato)
- [ ] Indicadores em destaque visual (caixas ou tabela separada)
- [ ] Comparativos MoM e YoY em tabela ou grafico simples
- [ ] Insights em prosa, NAO em bullet point cru
- [ ] PDF pesa menos que 5 MB
- [ ] Nome do arquivo: `DRE_[NomeCliente]_[AAAA-MM].pdf`

**Bloqueador**: PDF cortado, ilegivel ou com erro de layout -> NAO envia.

---

## 5. Email

- [ ] Destinatario correto (conferir 2x, cliente certo)
- [ ] Nenhum destinatario errado em CC ou BCC
- [ ] BCC `{{EMAIL_ARQUIVO_BCC}}` adicionado (registro interno)
- [ ] Assunto preenchido conforme template
- [ ] Preview text (preheader) preenchido
- [ ] Saudacao com primeiro nome correto do cliente
- [ ] Mes de referencia correto no corpo do email
- [ ] 4 numeros chave preenchidos (Receita, Lucro, 2 margens)
- [ ] Sinal das variacoes correto (verde pra positivo, vermelho pra negativo)
- [ ] Insight principal preenchido (nao deixar `{{INSIGHT_PRINCIPAL}}`)
- [ ] 3 acoes sugeridas preenchidas
- [ ] Link de agendamento funciona (clicar pra testar)
- [ ] WhatsApp display correto
- [ ] Nome do contador + CRC corretos na assinatura
- [ ] PDF anexado (conferir o anexo abre antes de enviar)
- [ ] Nome do anexo bate com template

**Bloqueador**: variavel `{{X}}` aparecendo no email final -> NAO envia.

---

## 6. Tom e clareza (revisor)

- [ ] Zero jargao contabil no email (nada de "regime de competencia", "ativo circulante", etc.)
- [ ] Insight comeca pelo numero, nao por contexto
- [ ] Acao sugerida e concreta (verbo + objeto + prazo), nao generica
- [ ] Frases curtas, paragrafos de 3-4 linhas no maximo
- [ ] Zero erro de ortografia
- [ ] Nome do cliente escrito corretamente (cuidado com acentos)
- [ ] Tom: profissional + humano, nem corporativo gelado nem casual demais

**Bloqueador**: erro de portugues ou nome errado do cliente -> NAO envia.

---

## 7. Aprovacao final

| Quem | O que aprova | Data | Status |
|---|---|---|---|
| Contador responsavel | Numeros e analise | | [ok / volta] |
| Revisor (2o analista) | Tudo (4 olhos) | | [ok / volta] |
| Socio {{NOME_ESCRITORIO}} | So se variacao MoM > 50% ou alerta tributario serio | | [ok / N/A] |

---

## 8. Pos-envio

Apos clicar "Enviar":

- [ ] Status do cliente atualizado pra "DRE_ENVIADO" no controle interno
- [ ] Data e hora de envio registradas
- [ ] PDF arquivado em `arquivo/clientes/[NomeCliente]/dre/[AAAA-MM]/`
- [ ] Email arquivado (BCC ja garante, conferir que chegou)
- [ ] Lembrete de follow-up criado pra 3 dias depois (se cliente nao responder)
- [ ] Proximo ciclo (mes seguinte) ja agendado na agenda da equipe

---

## 9. Em caso de erro detectado APOS envio

1. **Imediato (menos de 1h)**: enviar email "Pedimos a desconsideracao do anterior, segue versao corrigida"
2. **Mais de 1h**: enviar nova versao com selo "RETIFICADO" no PDF + email explicando o que mudou
3. Registrar incidente em `07_LOGS/decisions.md` do cliente
4. Ajustar SOP/checklist pra evitar repeticao
5. Comunicar cliente por WhatsApp + email (nao so email)

---

## 10. Versoes

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Checklist inicial - 9 secoes, 50+ pontos |
