---
tipo: brain
modulo: NFS-e
status: ativo
criticidade: alta
atualizado: 2026-07-26
---

# 🧾 NFS-e — Notas Fiscais

> [!success] Status: Portal Nacional ativo
> Emissão exclusivamente pelo Portal Nacional desde 20/07/2026. Portal municipal não é mais usado.

## Quando emite

Automaticamente nos dias **20, 25, 29 e 30** de cada mês.
O Claude busca pagamentos confirmados no Asaas e emite as notas.

## Parâmetros fixos

| Campo | Valor |
|-------|-------|
| Portal | https://www.nfse.gov.br/EmissorNacional |
| Natureza | 107 (sempre) |
| Item — aluguel | 1712 |
| Item — venda/serviço | 1005 |

## Emissão em lote (automática)

Roda sozinha nos dias de corte. Após emitir, o Claude envia os PDFs no seu WhatsApp.

## Emissão avulsa (manual — uma nota só)

> [!tip] Use quando precisar emitir uma nota fora do dia de corte

Diga qualquer uma dessas frases:
- **"emitir nota avulsa"**
- **"emitir uma nota"**
- **"nota de aluguel avulsa"**

O Claude vai perguntar: CNPJ/CPF → venda ou aluguel → descrição → valor. Depois emite e manda o PDF no seu WhatsApp.

## Se der erro na emissão

> [!warning] Problemas comuns
> - **Captcha no portal** → o Claude precisa de sessão ativa no Chrome. Avise se pedir ajuda
> - **CPF sem formatação** → o Asaas precisa ter CPF correto no cadastro do cliente
> - **Portal em manutenção** → tentar novamente em 1-2h

## Como acionar

| O que você quer | O que dizer |
|-----------------|-------------|
| Emitir notas do lote | "emitir notas", "rodar emissão NFS-e" |
| Uma nota avulsa | "emitir nota avulsa" |
| Ver notas emitidas hoje | "notas emitidas hoje" |
| Retirar notas já emitidas | "retirar notas fiscais" |

## Credenciais

Ficam em: `18_AUTOMATION_STACK/nfem-joinville/.env`
Não compartilhe esse arquivo.

## Ver também

- [[emitir-notas-fiscais]] — skill completa
- [[emitir-nota-avulsa]] — skill de nota única
- [[00 - Índice Brain]] — voltar ao índice
