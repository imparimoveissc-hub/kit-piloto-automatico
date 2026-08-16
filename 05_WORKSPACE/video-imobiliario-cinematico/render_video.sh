#!/usr/bin/env bash
set -euo pipefail

FFMPEG="/Users/user/bin/ffmpeg"
ROOT="/Users/user/Downloads/Kit-Piloto-Automatico-V30-DISTRIB"
OUT="$ROOT/06_OUTPUTS/2026-07-07_video-imobiliario-cinematico"
SEG="$OUT/segments_v2"
mkdir -p "$SEG"

vf_base="[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=contrast=1.06:saturation=1.10:brightness=0.01:gamma=1.05,unsharp=3:3:0.12,format=yuv420p[v]"
vf_voice="[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=brightness=0.055:contrast=1.05:saturation=1.05:gamma=1.18,unsharp=3:3:0.15,format=yuv420p[v]"

render_silent() {
  local input="$1" ss="$2" dur="$3" out="$4"
  "$FFMPEG" -hide_banner -y -nostdin -ss "$ss" -t "$dur" -i "$input" \
    -f lavfi -t "$dur" -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -filter_complex "$vf_base" \
    -map "[v]" -map 1:a:0 -map_metadata -1 -c:v libx264 -preset veryfast -crf 22 \
    -c:a aac -b:a 128k -shortest -movflags +faststart "$out"
}

render_voice() {
  local input="$1" ss="$2" dur="$3" out="$4"
  "$FFMPEG" -hide_banner -y -nostdin -ss "$ss" -t "$dur" -i "$input" \
    -filter_complex "$vf_voice" \
    -map "[v]" -map 0:a:0 -map_metadata -1 -c:v libx264 -preset veryfast -crf 22 \
    -af "highpass=f=90,lowpass=f=12000,acompressor=threshold=-18dB:ratio=2.2:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=11" \
    -c:a aac -b:a 160k -movflags +faststart "$out"
}

render_silent "/Users/user/Downloads/9.mov" 0.50 4.00 "$SEG/01-area-condominio.mp4"
render_silent "/Users/user/Downloads/1.mov" 0.80 3.60 "$SEG/02-fachada.mp4"
render_voice  "/Users/user/Downloads/2.mov" 0.00 25.70 "$SEG/03-corretor-abertura.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 1.28 16.14 "$SEG/04-tour-fala-01.mp4"
render_silent "/Users/user/Downloads/4.mov" 1.00 3.80 "$SEG/05-sala-apoio.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 17.97 22.64 "$SEG/06-tour-fala-02.mp4"
render_silent "/Users/user/Downloads/5.mov" 1.00 3.80 "$SEG/07-integracao-apoio.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 41.88 6.72 "$SEG/08-tour-fala-03.mp4"
render_silent "/Users/user/Downloads/6.mov" 0.80 4.50 "$SEG/09-cozinha-apoio.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 52.07 7.32 "$SEG/10-tour-fala-04.mp4"
render_silent "/Users/user/Downloads/7.mov" 0.80 3.80 "$SEG/11-home-office-apoio.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 62.26 7.99 "$SEG/12-tour-fala-05.mp4"
render_silent "/Users/user/Downloads/8.mov" 0.80 4.80 "$SEG/13-quarto-apoio.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 72.81 10.36 "$SEG/14-tour-fala-06.mp4"
render_silent "/Users/user/Downloads/9.mov" 4.20 4.00 "$SEG/15-area-final.mp4"
render_voice  "/Users/user/Downloads/3.MOV" 86.61 18.80 "$SEG/16-tour-fechamento.mp4"

cat > "$OUT/concat.txt" <<LIST
file '$SEG/01-area-condominio.mp4'
file '$SEG/02-fachada.mp4'
file '$SEG/03-corretor-abertura.mp4'
file '$SEG/04-tour-fala-01.mp4'
file '$SEG/05-sala-apoio.mp4'
file '$SEG/06-tour-fala-02.mp4'
file '$SEG/07-integracao-apoio.mp4'
file '$SEG/08-tour-fala-03.mp4'
file '$SEG/09-cozinha-apoio.mp4'
file '$SEG/10-tour-fala-04.mp4'
file '$SEG/11-home-office-apoio.mp4'
file '$SEG/12-tour-fala-05.mp4'
file '$SEG/13-quarto-apoio.mp4'
file '$SEG/14-tour-fala-06.mp4'
file '$SEG/15-area-final.mp4'
file '$SEG/16-tour-fechamento.mp4'
LIST

"$FFMPEG" -hide_banner -y -nostdin -f concat -safe 0 -i "$OUT/concat.txt" -c copy "$OUT/video-imobiliario-sem-musica.mp4"

"$FFMPEG" -hide_banner -y -nostdin -f lavfi -i "sine=frequency=110:duration=150:sample_rate=48000" \
  -f lavfi -i "sine=frequency=220:duration=150:sample_rate=48000" \
  -f lavfi -i "sine=frequency=330:duration=150:sample_rate=48000" \
  -filter_complex "[0:a]volume=0.018[a0];[1:a]volume=0.012[a1];[2:a]volume=0.007[a2];[a0][a1][a2]amix=inputs=3,afade=t=in:st=0:d=3,afade=t=out:st=142:d=6,alimiter=limit=0.35[m]" \
  -map "[m]" -c:a aac -b:a 128k "$OUT/trilha-cinematica-leve.m4a"

"$FFMPEG" -hide_banner -y -nostdin -i "$OUT/video-imobiliario-sem-musica.mp4" -i "$OUT/trilha-cinematica-leve.m4a" \
  -filter_complex "[1:a]volume=0.30[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-15:TP=-1.2:LRA=11[aout]" \
  -map 0:v:0 -map "[aout]" -c:v copy -c:a aac -b:a 192k -movflags +faststart \
  "$OUT/video-imobiliario-cinematico-PRONTO.mp4"
