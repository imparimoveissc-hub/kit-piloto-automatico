---
tipo: skill
origem: ambiente (não é arquivo do Kit)
status: ativa
---

# Skill — emitir-notas-fiscais

Emite NFS-e automaticamente via pipeline **NF-e Joinville** (Impar Imóveis).

## O que faz
1. Conecta no **Asaas** e busca pagamentos **recebidos**.
2. Cruza com a base de clientes.
3. Emite as NFS-e no portal **nfem.joinville.sc.gov.br**.

## Quando dispara
- Nos dias de corte: **20, 25, 29 e 30** de cada mês.
- Ou quando eu digo: "emitir notas", "notas pendentes", "rodar emissão", "NFS-e", "notas fiscais Joinville", "emitir do Asaas".

## Onde vivem as credenciais
`18_AUTOMATION_STACK/nfem-joinville/.env`

## Relacionadas
- [[retirar-notas-fiscais]]
- [[rodar-pipeline]]
