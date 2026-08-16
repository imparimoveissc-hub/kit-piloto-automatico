---
name: gerar-contrato-locacao
description: >
  Gera um contrato de locação e o termo de vistoria preenchidos a partir dos dados das partes
  e do imóvel, salvando com a nomenclatura padrão da casa e sem alterar os modelos originais.
  Use quando o usuário disser "gerar contrato de locação", "montar o contrato", "fazer a minuta
  de aluguel", "preencher o contrato e a vistoria". Reaproveita o gerador que já existe no kit.
argument-hint: '[--residencial | --comercial]'
---

# /gerar-contrato-locacao

Preenche o contrato de locação e o termo de vistoria e devolve os arquivos finais. Antes de
entregar como final, roda o checklist de `/imobiliario-juridico:revisar-contrato-locacao`.

## Instruções

1. **Carregue o playbook** (`~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`).
   Se houver `[PREENCHER]`, pare e peça a cold-start-interview. Use os defaults da casa (índice,
   garantia, prazo, encargos) para pré-preencher campos e reduzir perguntas.

2. **Colete os campos obrigatórios** (peça só o que o playbook não resolve por default):
   locador(es), locatário(s), natureza (residencial/comercial), imóvel (endereço, matrícula,
   inscrição, áreas), prazo, início, 1º vencimento, dia de vencimento, valor do aluguel (número +
   extenso), garantia, seguro incêndio, IPTU, taxa de lixo, condomínio, valor total, data do
   contrato, condição específica, acessórios (ar-condicionado etc.), chaves entregues.

3. **Gere os documentos.** O kit já traz o gerador; chame-o em vez de reescrever a lógica:

   ```bash
   python3 "00_OS/commands/gerar-contrato-locacao.py"
   ```

   Se o usuário passou os dados no chat, colete os campos acima e chame as funções do script
   inline. Nunca edite os modelos originais — o script salva cópias preenchidas.

4. **Revise antes de entregar.** Rode o checklist da skill de revisão sobre a minuta gerada.
   Se algum item sair 🔴 ou cair na matriz de escalonamento, entregue como **rascunho** e sinalize.

5. **Registre o vencimento e o reajuste** chamando `/imobiliario-juridico:acompanhar-reajuste`
   com os dados do novo contrato (data de início, índice, valor) para já entrar no registro.

6. **Salve** com a nomenclatura definida no playbook e informe os caminhos finais.

## Saída

- Caminho do contrato preenchido.
- Caminho do termo de vistoria.
- Resumo do checklist (✅/⚠️/🔴) e nota "rascunho para revisão" se houver pendências.

## Exemplos

```
/imobiliario-juridico:gerar-contrato-locacao --residencial
```
