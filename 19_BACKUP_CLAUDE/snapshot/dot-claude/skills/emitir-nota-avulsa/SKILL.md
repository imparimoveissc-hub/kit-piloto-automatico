---
name: emitir-nota-avulsa
description: >
  Emite UMA nota fiscal avulsa (manual, fora do fluxo do Asaas) no NF-em Joinville
  e envia o PDF no WhatsApp do Jonata. Use quando o usuário disser: "emitir nota de
  venda", "nova nota fiscal de venda", "criar nota de venda", "emitir nota avulsa",
  "nota fiscal manual", "emitir uma nota", "nota de aluguel avulsa", "gerar uma nota
  pra um cliente", ou qualquer variação de emissão de UMA nota informando os dados na
  hora. NÃO confundir com a skill `emitir-notas-fiscais` (essa busca pagamentos no
  Asaas e emite o lote do mês). Aqui os dados são digitados pelo usuário, uma nota por vez.
---

# Skill: Emitir Nota Avulsa (NF-em Joinville) + WhatsApp

Emite uma nota fiscal única com dados informados na hora e envia o PDF no WhatsApp do Jonata.

- **Portal:** https://nfem.joinville.sc.gov.br
- **Pipeline:** `18_AUTOMATION_STACK/nfem-joinville/`
- **WhatsApp do Jonata:** `554796876631@s.whatsapp.net` (número 5547996876631, sem o 9 extra no JID)
- **Regras fixas:** natureza da operação = **107**; item da lista de serviço = **1005 (VENDA)** / **1712 (ALUGUEL)**; alíquota ISS e demais campos seguem a config padrão.

---

## Passo 1 — Coletar os dados (pergunte, um de cada vez)

Pergunte ao usuário e só siga quando tiver todos:

1. **CNPJ/CPF do cliente (tomador)** — obrigatório. O tomador precisa já estar cadastrado no NF-em por esse documento; a automação só informa o CPF/CNPJ e o site preenche nome e endereço.
2. **Tipo da nota: VENDA ou ALUGUEL?** — define o item da lista de serviço (venda → 1005, aluguel → 1712). Se o usuário só falou "nota de venda", assuma **venda**.
3. **Descrição do serviço** — obrigatória (texto que vai no corpo da nota).
4. **Valor dos serviços** — obrigatório (ex.: `1.234,56` ou `1234.56`).

A natureza da operação é sempre **107** — não pergunte.

Antes de emitir, mostre um resumo e peça confirmação (emissão é ação real e irreversível):

```
Vou emitir esta nota:
• Tomador (CNPJ/CPF): <doc>
• Tipo: <VENDA/ALUGUEL>  → item de serviço <1005/1712>
• Natureza da operação: 107
• Descrição: <descrição>
• Valor: R$ <valor>

Confirma a emissão? (a janela do navegador vai abrir para você digitar o captcha do login)
```

---

## Passo 2 — Emitir

Só rode após a confirmação explícita do usuário.

```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
python3 -m src.cli emitir-manual \
  --tipo <venda|aluguel> \
  --cpf-cnpj "<CNPJ/CPF>" \
  --descricao "<descrição>" \
  --valor "<valor>"
```

- O navegador abre; **avise o usuário para digitar o captcha e clicar em Login** (até 5 min de espera).
- Ao final, o comando imprime um JSON com `status`, `numero_nota`, `tomador` e `pdf_path`.
- Se `status` for `erro`, mostre a mensagem ao usuário e **não** envie nada no WhatsApp. Erros comuns:
  - Tomador não cadastrado no NF-em → cadastrar em Serviços > Configurações > Clientes antes.
  - Falha de login/captcha → rodar de novo.

---

## Passo 3 — Enviar o PDF no WhatsApp do Jonata

Com `status: sucesso`, pegue o `pdf_path` do JSON e envie via WhatsApp para o Jonata.

> **Atenção ao número:** o WhatsApp guarda o número do Jonata sem o 9 extra. Use o JID
> `554796876631@s.whatsapp.net` como `recipient` (é o Jonata, 5547996876631). Se falhar,
> tente o número cru `5547996876631`.

- Use `mcp__whatsapp__send_file` com `recipient = "554796876631@s.whatsapp.net"` e `media_path = <pdf_path>`.
- Em seguida, mande uma mensagem de contexto com `mcp__whatsapp__send_message` para `554796876631@s.whatsapp.net`:

```
Nota fiscal emitida ✅
Nº <numero_nota> • <VENDA/ALUGUEL>
Tomador: <tomador>
Valor: R$ <valor>
```

---

## Passo 4 — Resumo para o usuário

```
Nota emitida — Nº <numero_nota>

• Tipo: <VENDA/ALUGUEL> (item <1005/1712>)
• Tomador: <tomador> (<CNPJ/CPF>)
• Valor: R$ <valor>
• PDF salvo em: <pdf_path>
• Enviado no WhatsApp do Jonata (5547996876631): ✅
```

---

## Regras

- **Uma nota por vez.** Para o lote mensal do Asaas, use a skill `emitir-notas-fiscais`.
- **Nunca emita sem confirmar** o resumo com o usuário.
- Natureza é sempre 107; item é 1005 (venda) ou 1712 (aluguel) — não invente outros códigos.
- Só envie no WhatsApp quando a emissão retornar `sucesso` com um PDF válido.
