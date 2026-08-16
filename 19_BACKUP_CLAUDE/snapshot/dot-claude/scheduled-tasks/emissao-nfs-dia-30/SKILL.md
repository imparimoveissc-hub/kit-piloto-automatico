---
name: emissao-nfs-dia-30
description: Emissão automática de NFS-e Joinville — dia 30 de cada mês
---

Você é o agente de emissão de notas fiscais da Impar Imóveis. Execute o pipeline de emissão automática de NFS-e no portal NF-em Joinville.

## Objetivo
Buscar todos os pagamentos pendentes de nota fiscal no Asaas e emitir as NFS-e correspondentes no portal nfem.joinville.sc.gov.br.

## Passos

1. Verifique se as dependências estão instaladas:
```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
python3 -c "import playwright, httpx, dotenv; print('OK')" 2>&1
```
Se falhar, instale: `pip3 install playwright httpx python-dotenv --break-system-packages -q && python3 -m playwright install chromium`

2. Liste os pendentes:
```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
python3 -m src.cli pendentes
```

3. Se houver pendentes, emita automaticamente:
```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
echo "SIM" | python3 -m src.cli emitir-mes 2>&1 | tee /tmp/nf-emissao-dia30.log
```

4. Verifique erros:
```bash
cd "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/nfem-joinville"
python3 -m src.cli listar-erros
```

5. Informe o resumo: quantas notas emitidas, valor total, se houve erros.

## Contexto
- Credenciais em: `18_AUTOMATION_STACK/nfem-joinville/.env`
- PDFs salvos em: `/Users/user/Desktop/backup Jonata/contabilidade Impar imóveis/notas fiscais`
- Registro em: `18_AUTOMATION_STACK/nfem-joinville/data/emissoes.json`
- Este é o corte do dia 30 — período: dia 29 até dia 29 deste mês. Também cobre o fechamento mensal.