# Automação de Emissão de NFS-e (Portal Nacional Exclusivo)

Emite automaticamente notas fiscais de serviço (NFS-e) via:
- **Portal Nacional** (`https://www.nfse.gov.br/EmissorNacional`) — **exclusivo desde 20/07/2026**

---

## Migração 20/07/2026

A partir de 20 de julho de 2026, a Prefeitura de Joinville desativou seu portal local. **Toda emissão é feita exclusivamente pelo Portal Nacional da NFS-e.**

- Portal de Joinville (`https://nfem.joinville.sc.gov.br`) descontinuado
- Suporte legado a Joinville removido de todas as automações
- Configuração `PORTAL_TIPO` removida (era `nacional` ou `joinville`)

---

## Como funciona

```
Asaas paga boleto
      │
      ▼
Webhook POST /webhook/asaas
      │
      ├─ valida assinatura
      ├─ verifica idempotência (não duplica nota)
      ├─ busca dados completos no Asaas
      ├─ busca config do cliente em clientes.json
      ├─ abre Chromium via Playwright
      ├─ faz login no Portal Nacional (https://www.nfse.gov.br/EmissorNacional)
      ├─ preenche formulário
      ├─ emite a nota (ou aborta em dry_run)
      ├─ baixa o PDF
      ├─ salva em /notas fiscais/MM-AAAA/MM-AAAA-NOME.pdf
      └─ registra log
```

---

## Pré-requisitos

- Python 3.9+
- pip

```bash
cd 18_AUTOMATION_STACK/nfem-joinville
pip install -r requirements.txt
python -m playwright install chromium
```

---

## Configuração

### 1. Arquivo `.env`

Copie o exemplo e preencha:

```bash
cp .env.example .env
```

Campos obrigatórios:

| Variável | Descrição |
|---|---|
| `ASAAS_API_KEY` | Chave de API do Asaas (começa com `$aact_...`) |
| `ASAAS_WEBHOOK_TOKEN` | Token secreto do webhook (configure no Asaas) |
| `NFSE_NACIONAL_USER` | Login no Portal Nacional: CNPJ/CPF (ex: `50886299000100`) |
| `NFSE_NACIONAL_PASSWORD` | Senha do Portal Nacional |

Campos opcionais (têm padrão):

| Variável | Padrão | Descrição |
|---|---|---|
| `ASAAS_ENV` | `production` | `production` ou `sandbox` |
| `NOTAS_BASE_DIR` | `/Users/user/Desktop/backup Jonata/contabilidade Impar imóveis/notas fiscais` | Pasta raiz dos PDFs |
| `DRY_RUN` | `true` | `true` = não finaliza emissão (modo teste) |
| `BROWSER_HEADLESS` | `true` | `false` = abre janela do browser (debug) |
| `WEBHOOK_PORT` | `8765` | Porta do servidor webhook |

### 2. Configuração de clientes — `config/clientes.json`

Cada entrada mapeia um cliente Asaas a seus dados fixos de NF:

```json
{
  "clientes": [
    {
      "asaas_customer_id": "cus_XXXXX",
      "nome_tomador": "FULANO DE TAL",
      "cpf_cnpj": "000.000.000-00",
      "endereco": "Rua Exemplo, 100",
      "bairro": "Centro",
      "municipio": "Joinville",
      "uf": "SC",
      "cep": "89200-000",
      "descricao_servico": "Referente a locação de sala comercial..."
    }
  ]
}
```

**Como achar o `asaas_customer_id`:** no painel Asaas → Clientes → clique no cliente → o ID aparece na URL (`/customers/cus_XXXXX`).

A descrição suporta dois placeholders que são substituídos automaticamente:
- `[VALOR]` → valor pago formatado em R$
- `[TOTAL]` → mesmo que `[VALOR]`

---

## Rodando

### Modo teste (dry run)

Verifica o preenchimento sem emitir a nota:

```bash
# Garanta que DRY_RUN=true no .env
python -m src.cli simular
```

### Emitir nota manualmente para um pagamento

```bash
python -m src.cli emitir pay_XXXXXXXXXXXXX
```

### Rodar o mês inteiro manualmente (sem webhook)

Esse é o jeito mais simples de usar a automação todo mês: busca no Asaas tudo que foi pago no mês atual, mostra a lista com valores, pede confirmação, e só então emite.

```bash
# Só ver o que está pendente, sem emitir nada
python -m src.cli pendentes

# Ver a lista, confirmar e emitir tudo de uma vez (um único login para o lote inteiro)
python -m src.cli emitir-mes
```

O `emitir-mes` ativa `DRY_RUN=false` automaticamente só durante a execução e devolve para `true` no final, mesmo se der erro no meio do caminho — não precisa mexer no `.env` manualmente.

### Emitir nota avulsa (manual)

```bash
python -m src.cli emitir-manual \
  --tipo venda \
  --cpf-cnpj "00000000000191" \
  --descricao "Descrição do serviço" \
  --valor "15.00"
```

O navegador abre; **avise o usuário para digitar o captcha/autenticar e clicar em Login** (até 5 min de espera).

### Iniciar o servidor webhook

```bash
python -m src.cli servidor
```

O servidor sobe em `http://0.0.0.0:8765`.

### Configurar webhook no Asaas

1. No painel Asaas → Configurações → Integrações → Webhooks
2. URL: `https://SEU_DOMINIO:8765/webhook/asaas`
3. Eventos: `PAYMENT_CONFIRMED` e `PAYMENT_RECEIVED`
4. Token secreto: o mesmo que você colocou em `ASAAS_WEBHOOK_TOKEN`

> Para testes locais sem domínio público, use [ngrok](https://ngrok.com):
> ```bash
> ngrok http 8765
> # Use a URL gerada como endpoint no Asaas
> ```

---

## Pasta de destino dos PDFs

```
/Users/user/Desktop/backup Jonata/contabilidade Impar imóveis/notas fiscais/
├── 05-2026/
│   ├── 05-2026-SIDNEI CIRILO DA SILVA.pdf
│   └── 05-2026-ERIC RUBSON DA SILVA ROCHA.pdf
└── 06-2026/
    └── 06-2026-FULANO DE TAL.pdf
```

---

## Endpoints do servidor

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Status do servidor |
| `POST` | `/webhook/asaas` | Recebe eventos do Asaas |
| `GET` | `/erros` | Lista pagamentos com erro |
| `POST` | `/reprocessar/{payment_id}` | Reprocessa um pagamento com erro |

---

## Testes automatizados

```bash
pip install pytest
python -m pytest tests/ -v
```

Cobre:
- Status de pagamento autorizados e não autorizados
- Montagem dos dados da NF
- Idempotência (duplicata bloqueada)
- Salvamento de PDF com sufixo incremental
- Sanitização de nome de arquivo

---

## Controle de notas emitidas

O arquivo `data/emissoes.json` registra todas as emissões:

```json
{
  "pay_XXXXX": {
    "cliente": "FULANO DE TAL",
    "valor": 3610.46,
    "data_pagamento": "2026-06-25",
    "numero_nota": "000123",
    "caminho_pdf": "/Users/.../06-2026-FULANO DE TAL.pdf",
    "status": "sucesso",
    "emitido_em": "2026-06-25T14:30:00"
  }
}
```

**Para reprocessar um erro manualmente:**

```bash
python -m src.cli reprocessar pay_XXXXX
```

---

## Logs

Os logs ficam em `logs/nfem.log` (rotativo, máx 5 MB × 5 arquivos).  
Screenshots de debug ficam em `logs/` com timestamp.

---

## Segurança

- Nenhuma credencial fica no código — tudo via `.env`
- O `.env` não deve ser commitado (adicione ao `.gitignore`)
- O token do webhook valida autenticidade via HMAC-SHA256
- Credenciais do Asaas e do Portal ficam apenas nas variáveis de ambiente

---

## Estrutura do projeto

```
nfem-joinville/
├── .env.example                   # Modelo de configuração
├── README.md
├── requirements.txt
├── config/
│   └── clientes.json              # Dados fixos por cliente
├── data/
│   ├── emissoes.json              # Controle de idempotência (gerado)
│   ├── nfem_session.json          # Sessão quente Joinville (gerado)
│   └── nfse_nacional_session.json # Sessão quente Portal Nacional (gerado)
├── logs/                          # Logs e screenshots (gerado)
├── src/
│   ├── config.py                  # Variáveis e constantes
│   ├── logger.py                  # Logger centralizado
│   ├── asaas_client.py            # API do Asaas
│   ├── nfem_automation.py         # Playwright — Joinville (legado)
│   ├── nfse_nacional_automation.py# Playwright — Portal Nacional (novo)
│   ├── pdf_manager.py             # Salvamento e nomeação dos PDFs
│   ├── idempotency.py             # Controle anti-duplicata
│   ├── pipeline.py                # Orquestrador principal
│   ├── webhook_server.py          # Servidor FastAPI
│   └── cli.py                     # Interface de linha de comando
└── tests/
    └── test_pipeline.py           # Testes unitários
```

---

## Notas importantes

### ⚠️ Login e automação

Os portais podem exigir autenticação via captcha ou Gov.br no login. Hoje existem 3 caminhos:

1. **Certificado digital A1** - caminho preferencial e 100% automático quando configurado.
2. **Sessão quente salva** - reaproveita os cookies do `login-manual` enquanto ainda valem.
3. **Usuário/senha com captcha** - modo assistido, quando não houver certificado nem sessão válida.

**Na prática:** com o certificado A1 configurado em `.env`, o webhook e o CLI podem emitir sem intervenção humana. Sem certificado, o fluxo continua funcionando em modo guiado para completar o login na janela do navegador.

### 🔄 Migração de Portal (Joinville → Nacional)

Para voltar ao portal legado por enquanto, configure:
```
PORTAL_TIPO=joinville
```

Os seletores CSS no `nfse_nacional_automation.py` foram copiados do módulo Joinville e precisam ser validados/ajustados contra a interface real do Portal Nacional. Use `BROWSER_HEADLESS=false` para debug visual.

### 📋 Certificado digital

O Portal Nacional já está configurado para usar certificado digital A1 via Playwright `client_certificates`. O arquivo padrão é:

```
config/certs/impar_50886299000100.pfx
```

Se o pfx tiver outra localização, ajuste `NFSE_CERT_PFX_PATH` no `.env`. Se o certificado tiver senha, preencha `NFSE_CERT_PASSWORD`.

---

## Troubleshooting

### "Tomador com CPF/CNPJ ... não está cadastrado"

O tomador (cliente que recebe o serviço) precisa estar cadastrado no portal com esse CPF/CNPJ antes. Cadastre manualmente:
- **Portal Nacional**: Serviços → Configurações → Clientes
- **Joinville**: Serviços → Configurações → Clientes (Emissão NF-em)

### Nota emitida mas PDF não foi baixado

A nota foi emitida no portal, mas a automação não conseguiu localizar o link de download do PDF. Isso pode acontecer se o HTML do portal mudou. Tente:
1. Rodar com `BROWSER_HEADLESS=false` e `DRY_RUN=false`
2. Verificar visualmente se o link do PDF está onde a automação espera
3. Ajustar os seletores CSS em `nfse_nacional_automation.py` ou `nfem_automation.py`

### Seletor CSS não funciona

Se os seletores mudarem no portal, a automação vai travar. Use:
```bash
BROWSER_HEADLESS=false python -m src.cli simular
```
A janela do browser fica aberta para você inspecionar os elementos com F12.

---

## Contato e Suporte

Dúvidas sobre a integração: verificar `logs/nfem.log` e `07_LOGS/decisions.md` do projeto.
