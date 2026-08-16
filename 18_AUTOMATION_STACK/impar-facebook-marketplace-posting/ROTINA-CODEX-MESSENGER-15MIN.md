⚠️ **CORREÇÃO 2026-07-11 16:14 BRT**: Primeira mensagem estava errada ('assistente virtual...'). Versão corrigida abaixo. OBRIGATÓRIO: ler EXATAMENTE conforme especificado (sem 'sou', sem emojis, sem 'assistente').

---

# Rotina Codex - Messenger Marketplace a cada 15 minutos

## Objetivo

Checar a inbox de Venda do Facebook Marketplace da Impar Imoveis e responder todos os clientes com status nao lido, mantendo a regra de um unico D0/link por lead.

## Caminho obrigatorio de navegador

1. Fazer preflight de ferramenta: confirmar que existe Browser plugin/navegador in-app controlavel nesta rodada.
2. Se a skill Browser estiver disponivel, ler a skill e selecionar explicitamente o Codex In-app Browser pelo fluxo oficial (`setupBrowserRuntime` + `agent.browsers.get("iab")`).
3. So registrar browser indisponivel depois desse preflight oficial falhar ou se a skill/controlador realmente nao estiver exposto na sessao.
4. Abrir `https://www.facebook.com/marketplace/inbox/` somente pelo Browser plugin/navegador in-app autenticado.
5. Confirmar que a pagina carregou a inbox do Marketplace com as abas/areas de Venda/Compra e sem login, 2FA, captcha ou checkpoint.
6. Ler o historico da conversa antes de qualquer resposta.
7. Varrer todos os itens nao lidos da inbox de Venda antes de encerrar a rodada.

Nao usar em nenhuma hipotese nesta rotina:

- Playwright standalone.
- Chromium/Chrome for Testing baixado por Playwright.
- Chrome headless.
- Chrome do sistema em `/Applications/Google Chrome.app`.
- Chrome do sistema sem extensao/sessao controlavel.
- Perfil persistente do Chrome em `~/Library/Application Support/Google/Chrome`.
- osascript/AppleScript para dirigir Chrome.
- Tentativa de contornar Crashpad, permissao do macOS ou `SIGABRT`.

Se a rotina nao conseguir usar o browser in-app/controlavel apos o preflight oficial da skill Browser, registrar `Messenger bloqueado: browser in-app/controlavel indisponivel nesta rodada apos preflight oficial; Chrome local proibido pela correcao 2026-07-11` e encerrar sem envio.

## Guardrails

- Nunca responder se houver duvida sobre o ultimo envio, anuncio, duplicidade ou historico.
- Nunca reenviar D0/link para o mesmo lead.
- Todo lead que aparecer como nao lido deve receber a resposta padrao pedindo telefone.
- Todo cliente com status nao lido deve receber a resposta padrao pedindo telefone.
- Quando iniciar a mensagem para um lead vindo do Facebook/Messenger, usar exatamente:

```text
Ola {{NOME}}

Imóvel disponivel, para mais informações me deixe seu contato.
```

- Limite de 1 follow-up ativo por lead por dia.
- Se o lead respondeu no mesmo dia, pode continuar o atendimento no Messenger.
- Se o lead mandar telefone, confirmar recebimento no Messenger e fazer handoff ao Jonata/SDR somente se o canal WhatsApp autorizado estiver disponivel.
- No handoff: usar SEMPRE o nome real exibido no cabeçalho da conversa do Messenger (ex: "João Silva") — NUNCA o número de telefone como nome. Se o nome não estiver visível, usar "Lead".
- No handoff: passar SEMPRE o link do anúncio do item em discussão (formato https://www.facebook.com/marketplace/item/XXXXXXXXXX) — NUNCA o link da inbox (https://www.facebook.com/marketplace/inbox/). Se o link do anúncio não estiver disponível, passar "sem link de anúncio".
- Nao prometer disponibilidade, preco fechado, valorizacao, endereco exato ou condicao comercial sem validacao humana.
- Nunca usar o WhatsApp pessoal do Jonata para leads da Impar.

## Falha segura

Encerrar sem envio quando aparecer:

- Login, 2FA, captcha, checkpoint ou confirmacao de seguranca do Facebook.
- Inbox nao carregada.
- Browser plugin/navegador in-app indisponivel.
- Historico inconsistente.
- Conversa com item que nao e imovel.
- Falta de certeza sobre destinatario.

## Resumo obrigatorio da rodada

- Messenger acessivel ou bloqueado.
- Quantas conversas foram verificadas.
- Quantas estavam nao lidas.
- Quantas respostas foram enviadas no Messenger.
- Quantos telefones foram capturados.
- Quantos alertas/handoffs foram enviados ao Jonata.
- Quantas conversas foram puladas e por qual motivo.
