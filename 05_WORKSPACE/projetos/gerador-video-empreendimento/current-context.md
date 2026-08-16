# Gerador de video de empreendimento

## Objetivo

Criar uma ferramenta local para o usuario preencher dados de um empreendimento de casas/sobrados geminados, adicionar imagens reais/Maps/Earth/render e gerar automaticamente um video vertical.

## Entrega atual

- Output: `06_OUTPUTS/2026-07-05_gerador-video-empreendimento/`
- Tipo: app estatico local em HTML/CSS/JS.
- Funcao: gerar cenas, previa em canvas e exportar video WebM.

## Premissas

- Primeiro MVP sem login, API externa ou publicacao automatica.
- Exportacao em WebM pelo navegador; conversao para MP4 fica como etapa externa se necessaria.
- Padrao inicial: 6 sobrados, sendo 1 unidade de esquina e 5 unidades de meio.

## Proximos upgrades possiveis

- Gerar MP4 via Remotion/FFmpeg.
- Adicionar narracao por TTS.
- Criar implantacao 3D a partir de medidas do lote.
- Adicionar template de marca da imobiliaria.
