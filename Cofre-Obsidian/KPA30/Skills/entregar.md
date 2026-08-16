---
name: entregar
description: Formata e prepara pacote de entrega pro cliente
---

# /entregar — Pacote de Entrega

## Processo

### 1. Identificar cliente
Pergunte: "Pra qual cliente e essa entrega?"
Leia o briefing em `clientes/[nome]/briefing.md`.

### 2. Coletar materiais
Pergunte: "Cole os materiais finais ou indique os arquivos."

### 3. Organizar pacote

Crie a estrutura:
```bash
mkdir -p clientes/[nome-cliente]/entregas/[data-YYYY-MM-DD]
```

Organize os arquivos:
```
entregas/[data]/
├── README.md          ← Indice do pacote
├── [material-1].md
├── [material-2].md
└── [material-N].md
```

### 4. Gerar indice (README.md)

```markdown
# Entrega — [Nome do Cliente]
Data: [data]
Responsavel: [empresa do config.md]

## Conteudo do pacote

| # | Material | Descricao |
|---|----------|-----------|
| 1 | [nome] | [o que e] |
| 2 | [nome] | [o que e] |

## Observacoes
[qualquer nota relevante]

## Proximos passos
[o que acontece agora]
```

### 5. Gerar mensagem de entrega

**WhatsApp:**
```
Oi [nome], tudo bem?

Sua entrega de [periodo/projeto] esta pronta.

Segue o pacote com [X] materiais:
• [material 1]
• [material 2]
• [material 3]

Qualquer ajuste, me avisa.
Abraco!
```

**Email:**
```
Assunto: Entrega [periodo] — [projeto]

Oi [nome],

Segue a entrega referente a [periodo/projeto].

Neste pacote:
1. [material 1]
2. [material 2]
3. [material 3]

[Observacoes se houver]

Fico a disposicao pra qualquer ajuste.

Abraco,
[sua empresa]
```

### 6. Salvar
Salve tudo em `clientes/[nome]/entregas/[data]/`

### 7. Proximo passo
Pergunte: "Entrega formatada. No final do mes, quer montar o relatorio? (/relatorio)"
