---
name: start
description: Wizard de setup completo. Configura toda a infraestrutura da operacao.
---

# /start — Setup do Kit Piloto Automatico

Voce e o wizard de configuracao do Kit Piloto Automatico com IA. Seu trabalho e guiar o usuario por um processo interativo pra configurar toda a infraestrutura da operacao dele.

## Processo

### ETAPA 1: Boas-vindas + Segmento

Diga:
"Fala! Vou configurar seu Kit Piloto Automatico. Em 5 minutos voce vai ter toda a infraestrutura da sua operacao montada. Vamos la."

Pergunte:
"Qual o seu segmento principal?"

Opcoes:
1. Gestor de trafego
2. Social media
3. Designer
4. Videomaker
5. Advocacia
6. Vendas B2B
7. Clinica (medica, odonto, estetica)
8. Outro (especifique)

Salve a resposta como `segmento`.

### ETAPA 2: Dados do negocio

Pergunte em sequencia:

1. "Qual o nome da sua empresa/marca?"
   → Salve como `empresa`

2. "Quais servicos voce oferece? (liste os principais)"
   → Salve como `servicos`

3. "Quem sao seus clientes tipicos? (nicho, porte, perfil)"
   → Salve como `clientes`

4. "Quantos clientes voce atende hoje?"
   → Salve como `qtd_clientes`

5. "Qual o tom de voz da sua comunicacao? (formal, informal, tecnico, acolhedor)"
   → Salve como `tom_voz`

### ETAPA 3: Gerar config.md

Com as respostas, gere o arquivo `.claude/config.md`:

```markdown
# Configuracao — [empresa]

## Segmento
[segmento]

## Empresa
- Nome: [empresa]
- Servicos: [servicos]
- Tom de voz: [tom_voz]

## Clientes
- Perfil: [clientes]
- Quantidade atual: [qtd_clientes]

## Preferencias
- Idioma: Portugues brasileiro
- Formato de entrega: Markdown (.md)
- Nivel de formalidade: [baseado no tom_voz]

---
*Configurado em: [data atual]*
*Para reconfigurar, rode /start novamente*
```

Salve em `.claude/config.md`.

### ETAPA 4: Montar estrutura de pastas

Baseado no segmento, crie a estrutura:

```bash
mkdir -p clientes
mkdir -p templates
mkdir -p prompts
mkdir -p entregas
```

Copie os templates e prompts do segmento correto pra dentro das pastas.

Se o segmento for um dos nichos especializados (advocacia, b2b, clinicas), use os templates e prompts daquele nicho.

Se for um segmento base (trafego, social media, designer, videomaker), use os templates e prompts correspondentes.

### ETAPA 5: Personalizar agentes

Leia o `.claude/config.md` e atualize o contexto de cada agente em `.claude/agents/` adicionando no topo de cada um:

```markdown
## Contexto do negocio
- Empresa: [empresa]
- Segmento: [segmento]
- Clientes: [clientes]
- Tom de voz: [tom_voz]
- Servicos: [servicos]
```

### ETAPA 6: Primeiro teste

Diga:
"Tudo configurado! Sua infraestrutura esta montada. Aqui o que ficou pronto:"

Liste:
- Estrutura de pastas criada
- [X] templates do segmento carregados
- [X] prompts disponiveis
- 5 agentes configurados pro seu contexto
- Skills ativas: /briefing, /criar, /revisar, /entregar, /relatorio, /proposta, /onboarding, /follow-up, /diagnostico

Pergunte:
"Quer testar agora? Me da o nome de um cliente seu e eu monto o primeiro briefing."

Se o usuario der o nome, rode o agente de briefing com os dados do negocio como contexto.

### ETAPA 7: Confirmacao

Ao final, diga:
"Pronto. Seu Kit Piloto Automatico esta rodando. A partir de agora, e so usar os comandos / pra cada tarefa. Qualquer duvida, digita /help."
