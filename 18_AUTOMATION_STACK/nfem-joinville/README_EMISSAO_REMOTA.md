# Emissão remota de nota fiscal pelo WhatsApp (do celular)

**Status: draft — pronto, mas você precisa ativar (2 comandos no Mac).**

Permite emitir uma nota fiscal avulsa mandando uma mensagem de WhatsApp do celular.
Você manda o comando → o **Mac** emite a NFS-e no portal de Joinville → o PDF volta
no seu WhatsApp. O Claude do celular não participa: quem executa é um listener que
roda sozinho no Mac.

---

## Como funciona (arquitetura)

```
Celular (WhatsApp)  ──"nota venda; ..."──►  Ponte whatsapp-mcp (messages.db)
                                                      │
                                        src/whatsapp_listener.py (polling)
                                                      │
                                        src.cli emitir-manual --usar-sessao
                                                      │
                                        Playwright headless + sessão salva
                                                      │
                                          NFS-e emitida  → PDF
                                                      │
Celular (WhatsApp)  ◄──PDF + resumo──   bridge /api/send
```

Dois pré-requisitos que o projeto resolve:

1. **Execução no Mac** — o Mac precisa estar **ligado e com a ponte do WhatsApp rodando**
   (a mesma que você já usa). O listener faz polling do banco da ponte a cada 15s.
2. **Captcha do login** — o portal pode pedir captcha em alguns cenários. O caminho
   preferencial agora é o **certificado digital A1**; quando ele estiver configurado,
   o disparo remoto roda sem captcha. Se o certificado não estiver disponível, ainda
   existe a **sessão "quente"**: você faz login manual uma vez e os cookies ficam
   salvos. Quando a sessão expirar, o listener te avisa no WhatsApp para refazer o login.

---

## Ativar (uma vez)

No Mac, dentro de `18_AUTOMATION_STACK/nfem-joinville`:

```bash
# 1) Login manual — abre o navegador, você digita o captcha, a sessão é salva
python3 -m src.cli login-manual

# 2) Sobe o listener (deixa rodando)
./run_listener.sh
#   ou:  python3 -m src.whatsapp_listener
```

Para rodar em segundo plano e sobreviver ao terminal fechado:

```bash
nohup python3 -m src.whatsapp_listener > logs/listener.out 2>&1 &
```

(Opcional) Iniciar sozinho quando o Mac liga: veja `com.impar.nfem-listener.plist.exemplo`.

---

## Usar (do celular)

Mande uma mensagem de WhatsApp **para o número da Ímpar** (a conta logada na ponte),
no formato:

```
nota venda; <CNPJ/CPF>; <descrição do serviço>; <valor>
nota aluguel; <CNPJ/CPF>; <descrição do serviço>; <valor>
```

Exemplos:

```
nota venda; 12.345.678/0001-90; Consultoria de marketing; 1.500,00
nota aluguel; 059.527.501-04; Comissão de administração; 361,00
```

Regras fixas (iguais ao fluxo local): **natureza 107**; item **1005 (venda)** /
**1712 (aluguel)**; o **tomador precisa já estar cadastrado no NF-em** pelo CPF/CNPJ.

O listener responde:
- `⏳ Emitindo...` ao receber o comando;
- o **PDF** + um resumo (nº da nota, tomador, valor) quando emite;
- `⚠️ sessão expirou` (rode `login-manual` no Mac) ou `❌ <erro>` quando falha.

---

## Limitações honestas

- **Mac desligado = não emite.** Para independer do Mac, o listener teria que ir para
  a VM Oracle (mais trabalho; o captcha fica sem tela). Não está feito.
- **Sessão do portal expira** (minutos/horas, definido pela Prefeitura). Quando cair,
  você refaz o `login-manual` no Mac. É o "fallback humano" combinado.
- **Sem confirmação interativa:** o comando do WhatsApp emite direto (não tem o passo
  de "confirma?" do fluxo local). Confira os dados antes de enviar.
- O número de destino está fixado no listener como `554796876631@s.whatsapp.net`
  (Jonata). Para mudar, edite `JONATA_JID` em `src/whatsapp_listener.py`.

---

## Arquivos

- `src/whatsapp_listener.py` — o listener (polling + parse + resposta).
- `src/cli.py` → `emitir-manual --usar-sessao` e `login-manual`.
- `src/nfem_automation.py` — sessão quente (`storage_state`, `unattended`).
- `data/nfem_session.json` — cookies da sessão (gerado pelo `login-manual`).
- `data/listener_state.json` — controle de qual mensagem já foi processada.
- `run_listener.sh` — atalho para subir o listener.
