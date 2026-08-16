# Checklist de Entrega de Arquivos

> **Como usar:** Use antes de enviar qualquer entrega ao cliente. Garante que todos os arquivos estao nos formatos corretos, organizados e nomeados de forma profissional. Marque cada item antes de enviar.

---

## Informacoes da Entrega

| Campo | Valor |
|-------|-------|
| **Cliente** | [NOME DO CLIENTE] |
| **Projeto** | [NOME DO PROJETO] |
| **Data da entrega** | [DD/MM/AAAA] |
| **Designer** | [SEU NOME] |
| **Versao** | [V1 / V2 / FINAL] |

---

## Estrutura de Pastas para Entrega

```
[NOME-CLIENTE]_[PROJETO]_[DATA]/
├── finais/
│   ├── png/                    ← Arquivos PNG (alta resolucao)
│   ├── jpg/                    ← Arquivos JPG (comprimidos para web)
│   ├── pdf/                    ← Arquivos PDF (impressao, se aplicavel)
│   └── video/                  ← Videos renderizados (MP4)
├── editaveis/
│   ├── psd/                    ← Photoshop
│   ├── ai/                     ← Illustrator
│   ├── figma/                  ← Link do Figma (se aplicavel)
│   └── canva/                  ← Link do Canva (se aplicavel)
├── assets/
│   ├── fotos/                  ← Fotos usadas no projeto
│   ├── icones/                 ← Icones e elementos graficos
│   └── fontes/                 ← Fontes utilizadas (se permitido)
└── README.txt                  ← Descricao dos arquivos e instrucoes
```

---

## Checklist de Arquivos

### Formatos e Resolucao

- [ ] PNG exportado em alta resolucao (300 DPI para impresso, 72 DPI para digital)
- [ ] JPG comprimido para web (qualidade 80-90%, tamanho < 500KB por arquivo)
- [ ] PDF vetorial para materiais de impressao (fontes convertidas em curvas)
- [ ] SVG para logos e icones (se solicitado)
- [ ] Video em MP4 (H.264, qualidade alta)

### Dimensoes

- [ ] Todas as pecas nas dimensoes corretas conforme briefing
- [ ] Versoes para diferentes plataformas exportadas separadamente
- [ ] Area segura respeitada (150px das bordas em stories)

| Peca | Dimensao esperada | Conferido |
|------|-------------------|-----------|
| [Feed Instagram] | 1080 x 1080px | [ ] |
| [Stories] | 1080 x 1920px | [ ] |
| [Banner Ads] | 1200 x 628px | [ ] |
| [OUTRO] | [DIMENSAO] | [ ] |

### Nomenclatura de Arquivos

**Padrao:** `[CLIENTE]_[TIPO]_[NUMERO]_[VERSAO].[EXTENSAO]`

Exemplo: `casaverde_feed_01_v1.png`

- [ ] Todos os arquivos seguem o padrao de nomenclatura
- [ ] Sem caracteres especiais, acentos ou espacos nos nomes
- [ ] Numeracao sequencial (01, 02, 03...)
- [ ] Versao indicada no nome (v1, v2, final)

### Qualidade Visual

- [ ] Textos sem erros de portugues (revisar duas vezes)
- [ ] Logo do cliente presente e correto (versao certa, posicao certa)
- [ ] Cores conforme identidade visual / paleta aprovada
- [ ] Fontes corretas (nao substituidas por fontes do sistema)
- [ ] Imagens em alta resolucao (sem pixelizacao)
- [ ] Contraste suficiente (texto legivel sobre o fundo)
- [ ] Alinhamento consistente entre as pecas

### Antes de Enviar

- [ ] Revisao final em tela cheia (zoom 100%)
- [ ] Verificar no celular (as pecas funcionam em tela pequena?)
- [ ] Todos os editaveis organizados e nomeados
- [ ] Link do Figma/Canva atualizado e com permissao de visualizacao
- [ ] Pasta organizada conforme estrutura acima
- [ ] README.txt com instrucoes basicas (o que e cada arquivo)

---

## Controle de Versoes

| Versao | Data | Alteracoes | Aprovado por |
|--------|------|------------|-------------|
| V1 | [DATA] | Primeira entrega | - |
| V2 | [DATA] | [AJUSTES FEITOS] | - |
| FINAL | [DATA] | [AJUSTES FINAIS] | [NOME] |

---

## Ajustes Solicitados

| # | Ajuste | Peca | Prioridade | Status |
|---|--------|------|------------|--------|
| 1 | [DESCRICAO DO AJUSTE] | [QUAL PECA] | Alta / Media / Baixa | Pendente / Feito |
| 2 | [DESCRICAO] | [PECA] | [PRIORIDADE] | [STATUS] |
| 3 | [DESCRICAO] | [PECA] | [PRIORIDADE] | [STATUS] |

---

<details>
<summary><strong>Exemplo de README.txt para a pasta de entrega</strong></summary>

```
ENTREGA — Casa Verde Eco Store
Projeto: Pack Social Media Abril/2026
Designer: Maria Silva
Data: 28/03/2026

CONTEUDO:
- /finais/png/ → 12 posts feed (1080x1080) + 8 stories (1080x1920)
- /finais/jpg/ → Versoes comprimidas para agendamento
- /editaveis/canva/ → Link: https://canva.com/design/xxxxx (viewer)
- /assets/fotos/ → Fotos de produto usadas

NOMENCLATURA:
casaverde_feed_01_final.png = Post 1 (carrossel slide 1)
casaverde_feed_02_final.png = Post 2
casaverde_stories_01_final.png = Story 1
...

FONTES USADAS:
- Playfair Display (Google Fonts)
- Inter (Google Fonts)

OBSERVACOES:
- Posts de carrossel estao numerados: _slide01, _slide02, etc.
- Stories com sticker de interacao: exportado sem o sticker (adicionar no app)
```

</details>
