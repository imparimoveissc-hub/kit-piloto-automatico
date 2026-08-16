---
name: lume-visual-style-brief
description: "Briefing de estilo \"Lume visual\" (minimalista, sensível, cinematográfico) para reuso com a skill video-use em futuros vídeos."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 924a9880-d9db-4221-a69b-240449323bd8
---

Quando o usuário pedir o estilo "Lume visual" (ou similar: minimalista, sensível, cinematográfico, contemplativo) em qualquer vídeo via skill [[video-use]], aplicar o briefing abaixo.

## Briefing original do cliente

Edite o vídeo em um estilo visual minimalista, sensível e cinematográfico, inspirado em uma estética "Lume visual".

**Objetivo:** vídeo autêntico, real e verdadeiro, aparência natural, elegante e emocional — sem parecer artificial, exagerado ou publicitário demais.

**Direção visual:**
- Cortes limpos, lentos e intencionais.
- Priorizar momentos reais: respiração, movimento natural, detalhes das mãos, textura da pele, tecidos, objetos, sombras e luz entrando no ambiente.
- Evitar transições chamativas. Cortes secos suaves, fades muito sutis ou dissolves quase imperceptíveis.
- Edição deve parecer humana, calma e contemplativa.
- Sem efeitos digitais óbvios, glitch, zooms agressivos, flashes ou excesso de motion graphics.

**Cor e tratamento:**
- Color grading suave, luz quente e natural.
- Preservar tons de pele reais.
- Contraste baixo a médio, pretos levemente levantados, highlights macios.
- Reduzir saturação excessiva (mas com moderação — ver nota de calibração abaixo).
- Grão de filme muito sutil, quase imperceptível.
- Resultado deve parecer analógico, orgânico e elegante.

**Ritmo:**
- Calmo, com pausas visuais.
- Cortes no beat emocional da música, não necessariamente em cada batida.
- Cenas respirando por 1 a 3 segundos.
- Valorizar silêncio visual, espaço negativo, composição limpa.

**Música:**
- Minimalista, atmosférica, emocional. Piano suave, ambient, textura orgânica, vocal etéreo ou instrumental cinematográfico discreto.
- Música não deve dominar — sustenta a emoção, fica por baixo da voz.
- Evitar música épica, pop exagerado, batidas agressivas.

**Texto na tela:**
- Pouco texto, tipografia limpa e discreta, bastante espaço ao redor.
- Cor off-white / cinza quente / preto suave.
- Nada de legendas chamativas, caixas grandes ou animações exageradas (ver nota de calibração — cliente pediu legendas completas em sessão posterior, ver abaixo).

**Composição:** enquadramentos simples, luz natural, sombras suaves, detalhes íntimos, movimento orgânico. Sensação de presença, memória e verdade — "lembrança bem editada, não um anúncio".

**Exportação:** aspect ratio vertical 9:16 (mas pode ser adaptado pro formato pedido).

## Paleta de cores

```
Warm Ivory     #F4EFE7
Soft Sand      #D8C7B3
Muted Taupe    #A8917D
Natural Clay   #B66F55
Olive Shadow   #6F735C
Deep Charcoal  #242322
Soft Black     #11100F
```
Evitar neon, saturação alta, contraste duro.

## Calibração aprendida (do uso real, importante para próximos vídeos)

**Por:** o cliente ajustou o resultado em rodadas sucessivas — essas correções valem como ponto de partida, não o briefing "puro", para a próxima vez.

- **Grade de cor:** o filtro inicial (saturação 0.72, colorbalance forte) ficou "filtro forte demais, nada natural" — calibração final aprovada: `eq=contrast=1.01:saturation=0.92:gamma=1.01` + colorbalance bem sutil (rs/gs/bs ~0.02-0.04) + curves leve (`0/0.015 0.5/0.5 1/0.97`) + grain `noise=alls=4`. Comece sutil, não agressivo.
- **Áudio:** cliente pediu voz acima da música (não o contrário) — balanço final: voz `volume=1.15` (limpa, com `highpass=f=90,afftdn=nf=-30` pra remover ruído ambiente, SEM lowpass que abafa) e música `volume=0.35` com fade in/out.
- **Áudio único:** se o vídeo usa múltiplos "planos" (recortes/crops de um único take, simulando cortes de câmera), **não** use crossfade/acrossfade no áudio — gera eco/sobreposição de voz audível. Extraia o áudio uma vez, contínuo, direto da fonte original (mesmo range de tempo), e use cortes de vídeo **hard-cut** (concat `-c copy`, sem dissolve) para que vídeo e áudio fiquem com a mesma duração e perfeitamente sincronizados.
- **Legenda:** o cliente pediu progressivamente: (1) legendas completas cobrindo 100% do vídeo (não só 2-3 textos esparsos) — gerar via transcript word-level, chunks de 2 palavras, MAIÚSCULO; (2) estilo "chamativo" inicial era caixa colorida + fonte grande, depois o cliente preferiu **sem caixa de fundo**, fonte **menor e em negrito**, com leve contorno escuro pra legibilidade. Ou seja: comece SEM caixa, fonte moderada (~FontSize 18-20 com libass `subtitles` filter), negrito, outline simples — é mais provável agradar de primeira do que a versão "chamativa com caixa".
- **Centralização do sujeito:** ao criar múltiplos "planos virtuais" via crop de um único take 4K, meça a posição real do sujeito no frame original (ex: via frame de referência) antes de definir os crops — não estime visualmente, calcule o x/y center real e derive os crops a partir disso.

## Pegadinhas técnicas do ffmpeg/libass (video-use)

- **FontSize do filtro `subtitles` (libass) é escalado por PlayResY=288 por padrão** quando não se define PlayResX/Y explicitamente em vídeos 1080x1920 — um FontSize=58 renderiza giant (~387px), cobrindo o rosto. Para texto "normal" tipo legenda 2 palavras em vídeo 1080x1920, usar FontSize entre 18-25.
- **Para caixa de fundo (BorderStyle=3), a cor vem de `OutlineColour`, não de `BackColour`** — e `Outline` funciona como o padding/tamanho da caixa (se `Outline=0`, a caixa fica invisível mesmo com cor definida).
- Música royalty-free sem direitos autorais e de uso comercial liberado (sem atribuição): **Mixkit** (mixkit.co) é uma fonte confiável — links diretos em `https://assets.mixkit.co/music/<id>/<id>.mp3`, "Mixkit Stock Music Free License".

## Cliente/projeto

Vídeo de origem usado nessa calibração: galpão logístico industrial, cliente "Impar Imóveis" — ver [[master_followup_prompt]] se relevante a outros projetos desse cliente.
