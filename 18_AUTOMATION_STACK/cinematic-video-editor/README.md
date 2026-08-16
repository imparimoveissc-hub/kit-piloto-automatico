# Automação — Editor Cinematográfico de Vídeos

Status: `draft funcional`

Objetivo: receber um vídeo bruto e gerar uma versão mais pronta para Reels/Stories/TikTok, com estética cinematográfica, enquadramento vertical, áudio tratado, cortes opcionais de silêncio e legenda quando um arquivo `.srt`/`.vtt` for fornecido.

## O que faz agora

- Converte para formato vertical `9:16` por padrão.
- Centraliza/corta a imagem para 1080x1920.
- Aplica tratamento visual cinematográfico:
  - contraste;
  - saturação controlada;
  - nitidez leve;
  - vinheta sutil;
  - leve grão de filme.
- Trata áudio:
  - normalização;
  - compressão leve;
  - volume final mais consistente.
- Pode remover pausas/silêncios automaticamente.
- Pode queimar legenda no vídeo se você enviar `.srt` ou `.vtt`.
- Gera relatório com duração, arquivo de entrada, arquivo final e parâmetros usados.

## Uso simples

```bash
python3 18_AUTOMATION_STACK/cinematic-video-editor/cinematic_editor.py \
  "/caminho/do/video.mp4"
```

Saída padrão:

```text
06_OUTPUTS/cinematic-video-editor/<nome-do-video>/
```

## Uso com cortes de silêncio

```bash
python3 18_AUTOMATION_STACK/cinematic-video-editor/cinematic_editor.py \
  "/caminho/do/video.mp4" \
  --auto-cut
```

## Uso com legenda

```bash
python3 18_AUTOMATION_STACK/cinematic-video-editor/cinematic_editor.py \
  "/caminho/do/video.mp4" \
  --subtitles "/caminho/legenda.srt"
```

## Uso completo

```bash
python3 18_AUTOMATION_STACK/cinematic-video-editor/cinematic_editor.py \
  "/caminho/do/video.mp4" \
  --auto-cut \
  --subtitles "/caminho/legenda.srt" \
  --title "Apartamento na planta em Joinville" \
  --preset cinematic-reels
```

## Presets

- `cinematic-reels`: vertical 9:16, contraste elegante, legenda grande.
- `clean-reels`: vertical 9:16, visual limpo, menos grão.
- `preview-fast`: vertical 9:16 em 540x960 para teste rápido.
- `wide-cinematic`: horizontal 16:9, look cinematográfico sem cortar para Reels.

## Limites atuais

- Legenda automática por IA ainda não está embutida, porque `whisper` não está instalado neste ambiente.
- Se você já tiver legenda `.srt`/`.vtt`, o sistema aplica no vídeo.
- Para transcrição 100% automática, a próxima etapa é adicionar Whisper/local ou API de transcrição.
- Melhorias visuais generativas, como trocar fundo ou reconstruir imagem, devem usar Runway como etapa complementar.

## Próxima evolução

```text
vídeo bruto
  -> transcrição automática
  -> escolha dos melhores trechos
  -> cortes por frase
  -> legendas dinâmicas palavra-a-palavra
  -> trilha sonora baixa
  -> export final + cortes curtos
```
