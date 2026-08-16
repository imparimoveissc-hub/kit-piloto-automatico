# Troubleshooting | Kit Piloto Automático com IA

## Problemas na Instalação

### 1. "npm não é reconhecido como comando"
**Causa:** Node.js não está instalado.
**Solução:** Baixe e instale o Node.js em https://nodejs.org (versão LTS). Depois feche e abra o terminal.

### 2. "Permissão negada" ao instalar o Claude Code
**Causa:** Terminal sem permissão de administrador.
**Solução (Windows):** Clique com botão direito no terminal → "Executar como administrador". Tente novamente.
**Solução (Mac/Linux):** Use `sudo npm install -g @anthropic-ai/claude-code`

### 3. "claude: command not found" depois de instalar
**Causa:** O terminal não reconhece o comando ainda.
**Solução:** Feche o terminal e abra de novo. Se persistir, reinicie o computador.

### 4. Login não abre o navegador
**Causa:** Navegador padrão não configurado ou bloqueio de popup.
**Solução:** Copie o link que aparece no terminal e cole manualmente no navegador.

### 5. "API key inválida" ou "não autenticado"
**Causa:** Conta Anthropic sem créditos ou plano.
**Solução:** Acesse console.anthropic.com e verifique se tem plano ativo. O Claude Code precisa de plano pago ou créditos.

---

## Problemas com os Agentes

### 6. Agente não aparece quando digito o comando
**Causa:** Arquivos dos agentes não estão na pasta certa.
**Solução:** Verifique se a pasta `.claude/agents/` existe no seu projeto e contém os arquivos .md dos agentes.

### 7. Agente dá resposta genérica/ruim
**Causa:** Falta contexto. O agente precisa de informações pra trabalhar.
**Solução:** Forneça mais detalhes. Em vez de "cria um post", diga "cria um post pra Instagram sobre lançamento de produto, tom informal, público: donos de restaurante, objetivo: atrair pra sessão estratégica gratuita".

### 8. Agente para no meio da resposta
**Causa:** Resposta muito longa ou limite de tokens atingido.
**Solução:** Peça "continue de onde parou" ou divida a tarefa em partes menores.

### 9. Agente mistura idiomas (português/inglês)
**Causa:** O agente pode responder no idioma do input.
**Solução:** Sempre inclua "Responda em português brasileiro" no final do seu pedido.

### 10. Agente demora muito pra responder
**Causa:** Pedido muito complexo ou conexão lenta.
**Solução:** Divida em pedidos menores. Em vez de "monta o relatório completo do mês", peça primeiro "monta a seção de métricas" e depois "monta a análise".

---

## Problemas com Templates

### 11. Template não abre no meu editor
**Causa:** Arquivos .md precisam de editor compatível.
**Solução:** Abra com: VS Code (gratuito), Notion (importar), Google Docs (copiar texto), ou qualquer editor de texto (Bloco de Notas funciona).

### 12. Campos [PREENCHER] não ficam bonitos no documento final
**Causa:** Markdown precisa ser convertido pra PDF ou outro formato.
**Solução:** Use o VS Code com extensão "Markdown PDF" pra exportar. Ou cole no Google Docs e formate lá.

---

## Problemas com WhatsApp

### 13. WhatsApp não conecta
**Causa:** QR Code expirou ou número já conectado em outro lugar.
**Solução:** Desconecte o WhatsApp Web de outros dispositivos primeiro. Gere novo QR Code e escaneie em até 30 segundos.

### 14. Mensagens automáticas não estão sendo enviadas
**Causa:** Fluxo desativado ou conexão perdida.
**Solução:** Verifique se o fluxo está ativo no painel. Se a conexão caiu, reconecte escaneando o QR Code novamente.

### 15. Cliente recebeu mensagem duplicada
**Causa:** Fluxo disparou duas vezes.
**Solução:** Verifique os gatilhos do fluxo. Pode ter duas automações respondendo ao mesmo evento.

---

## Problemas com Prompts

### 16. Prompt não gera resultado esperado
**Causa:** Placeholders não foram substituídos.
**Solução:** Antes de colar o prompt, substitua TODOS os campos entre colchetes. [NOME DO CLIENTE] vira "João Silva", [NICHO] vira "clínica odontológica", etc.

### 17. Resultado do prompt é muito curto
**Causa:** O prompt precisa de mais contexto.
**Solução:** Adicione no final: "Seja detalhado e inclua exemplos específicos pro contexto de [seu nicho]."

### 18. Resultado do prompt é muito longo
**Causa:** O prompt não limita o tamanho.
**Solução:** Adicione no final: "Limite a resposta a [X] parágrafos" ou "Seja conciso, máximo 200 palavras."

---

## Problemas Gerais

### 19. "Meu computador é lento, o Claude Code trava"
**Requisitos mínimos:** 4GB RAM, conexão de internet estável. O Claude Code é leve, o processamento acontece nos servidores da Anthropic.
**Solução:** Feche outros programas pesados enquanto usa.

### 20. "Gastei todos os tokens do mês"
**Causa:** Uso intensivo dos agentes.
**Solução:** O plano Claude Pro tem limite mensal. Monitore o uso em console.anthropic.com. Dica: use os templates e prompts (que não gastam tokens do Claude Code) pra tarefas simples, e reserve os agentes pra tarefas complexas.

---

## Ainda com problema?

Se nenhuma solução acima resolver:
1. Descreva o problema em detalhes
2. Inclua a mensagem de erro exata (se houver)
3. Informe seu sistema operacional (Windows/Mac/Linux)
4. Envie pra nosso suporte
