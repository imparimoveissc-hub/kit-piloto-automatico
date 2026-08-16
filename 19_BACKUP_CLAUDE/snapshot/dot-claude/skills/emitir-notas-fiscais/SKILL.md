---
name: emitir-notas-fiscais
description: >
  Skill para emitir notas fiscais automaticamente via pipeline NF-em Joinville.
  Use esta skill sempre que o usuário mencionar: "emitir notas", "gerar NFs", "rodar emissão",
  "notas pendentes", "emissão automática", "emitir NFS-e", "rodar pipeline de notas",
  "emitir do Asaas", "notas de serviço Joinville", ou qualquer variação. Acione também
  nos dias de corte (20, 25, 29 e 30 de cada mês) quando o usuário pedir para rodar
  o processo do mês. Conecta com o Asaas para buscar pagamentos recebidos, cruza com
  a base de clientes e emite as NFS-e no portal nfem.joinville.sc.gov.br.
---

# Skill: Emitir Notas Fiscais (NF-em Joinville)

## Configuração

- **Portal:** https://nfem.joinville.sc.gov.br
- **Pipeline:** `18_AUTOMATION_STACK/nfem-joinville/`
- **Credenciais:** `.env` em `18_AUTOMATION_STACK/nfem-joinville/.env`
- **Dias de corte:** 20, 25, 29 e 30 de cada mês

---

## Passo 1 — Verificar dependências

```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
python3 -c "import playwright, httpx, dotenv; print('OK')" 2>&1
```

Se der erro de módulo, instale:
```bash
pip3 install playwright httpx python-dotenv --break-system-packages -q
python3 -m playwright install chromium
```

---

## Passo 2 — Listar pendentes

```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
python3 -m src.cli pendentes
```

- Se retornar **"Nenhum pagamento pendente"**: informe o usuário e encerre. Nada a emitir.
- Se retornar uma lista: apresente ao usuário com cliente, valor e data de pagamento.

---

## Passo 3 — Confirmar e emitir

Só prossiga com emissão real após apresentar a lista ao usuário e receber confirmação explícita.

```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
echo "SIM" | python3 -m src.cli emitir-mes
```

O pipeline:
1. Busca pagamentos RECEIVED/CONFIRMED no Asaas do mês atual
2. Cruza com `config/clientes.json` para dados de emissão
3. Acessa o portal nfem.joinville.sc.gov.br via Playwright
4. Emite cada NFS-e e salva o PDF em `NOTAS_BASE_DIR` (definido no `.env`)
5. Registra em `data/emissoes.json` com status e número da nota

---

## Passo 4 — Resumo

Após a emissão, mostre:

```
Emissão concluída — {data}

• Notas emitidas: X
• Valor total: R$ X.XXX,XX
• PDFs salvos em: /Users/user/Desktop/backup Jonata/contabilidade Impar imóveis/notas fiscais
• Próximo corte: {próxima data de corte}
```

Para verificar erros pós-emissão:
```bash
python3 -m src.cli listar-erros
```

---

## Reprocessar nota com erro

Se uma nota falhou, reprocesse pelo ID do pagamento Asaas:
```bash
python3 -m src.cli reprocessar <payment_id>
```

---

## Regras

- **Nunca emita sem confirmar** a lista de pendentes com o usuário primeiro.
- **DRY_RUN=true** no `.env` simula sem emitir — mude para `false` para emissão real.
- Em caso de erro de login no portal, verifique credenciais em `.env`: `NFEM_USER` e `NFEM_PASSWORD`.
