---
name: edicao-video-ffmpeg-cinema
description: "Como editar vídeo nesta máquina — usar pipeline FFmpeg, não render do Remotion"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69eda5b9-9ccc-4cdd-9ba5-d749bbfca9c2
---

Para edição de vídeo nesta máquina, o **pipeline FFmpeg é a rota confiável**; o **renderer do Remotion falha** aqui (macOS < 15 Sequoia — erro "target closed" / MEDIA_ELEMENT_ERROR ao decodificar H264 no chrome headless). O projeto Remotion existe em `meu-video/` mas não renderiza.

**Why:** o usuário pediu Remotion, mas o render quebra nesta versão de macOS — insistir nele gera retrabalho.

**How to apply:**
- Grade cinematográfica "Clean & Bright": `eq=contrast=1.05:brightness=0.035:saturation=1.12:gamma=1.03` + `curves` (lift de mids) + `colorbalance` leve quente.
- Upscale de fontes baixas: `hqdn3d` (denoise) → `scale=...:flags=lanczos` → `unsharp`.
- Ken Burns: usar `zoompan=z=...:d=1:fps=30:s=1080x1920` e **NÃO** colocar filtro `fps` depois (duplica frames ~20x). Em zsh, escrever `fps=${FPS}` com chaves — `$FPS:s=` é lido como modificador `:s` de substituição ("bad substitution").
- Montagem: `xfade` (fade/fadewhite) com offsets acumulados; títulos via `drawtext` (fonte `/System/Library/Fonts/Avenir Next.ttc`).
- Transcrição: `whisper-cli` (brew whisper-cpp) + modelo `ggml-base.bin`, `-l pt`.

Whisper.cpp e ffmpeg (em /Users/user/bin/ffmpeg) já instalados. Ver [[impar-imoveis-reels]].
