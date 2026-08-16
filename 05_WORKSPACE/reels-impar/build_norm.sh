#!/bin/zsh
# Normaliza cada clip: 1080x1920, grade Clean&Bright, upscale lanczos, Ken Burns (zoompan corrigido).
DL="/Users/user/Downloads"
W="/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/reels-impar"
N="$W/norm"
mkdir -p "$N"
FPS=30

GRADE="eq=contrast=1.06:brightness=0.0:saturation=1.10:gamma=0.97,curves=r='0/0 0.5/0.5 0.8/0.75 1/0.92':g='0/0 0.5/0.5 0.8/0.75 1/0.92':b='0/0 0.5/0.5 0.8/0.76 1/0.93',colorbalance=rm=0.015:gm=0.0:bm=-0.015"

# out, arquivo, ss, dur, low(1=denoise), kb(in/out/panL/panR)
norm() {
  local out="$1" file="$2" ss="$3" dur="$4" low="$5" kb="$6"
  local tf=$(( dur * FPS ))
  local dn=""; [ "$low" = "1" ] && dn="hqdn3d=3:2:5:4,"
  local pre="${dn}scale=1296:2304:force_original_aspect_ratio=increase:flags=lanczos,crop=1296:2304"
  local z
  case "$kb" in
    in)   z="zoompan=z='min(1.0+0.0012*on,1.15)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=${FPS}:s=1080x1920";;
    out)  z="zoompan=z='max(1.15-0.0012*on,1.0)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=${FPS}:s=1080x1920";;
    panR) z="zoompan=z='1.12':d=1:x='(iw-iw/zoom)*on/${tf}':y='ih/2-(ih/zoom/2)':fps=${FPS}:s=1080x1920";;
    panL) z="zoompan=z='1.12':d=1:x='(iw-iw/zoom)*(1-on/${tf})':y='ih/2-(ih/zoom/2)':fps=${FPS}:s=1080x1920";;
  esac
  ffmpeg -ss "$ss" -t "$dur" -i "$file" -an \
    -vf "${pre},${z},unsharp=5:5:0.6:5:5:0.0,${GRADE},format=yuv420p" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p "$N/$out.mp4" -y -loglevel error \
    && echo "OK $out (${dur}s $kb) -> $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$N/$out.mp4")s"
}

norm 01_facade  "$DL/WhatsApp Video 2026-07-02 at 12.32.21.mp4"    0.3 5 0 in
norm 02_sala    "$DL/WhatsApp Video 2026-07-02 at 12.31.15.mp4"    2.5 5 1 panR
norm 03_jantar  "$DL/WhatsApp Video 2026-07-02 at 12.31.20.mp4"    1.0 5 1 in
norm 04_vista   "$DL/WhatsApp Video 2026-07-02 at 12.31.29.mp4"    2.0 5 0 out
norm 05_cozinha "$DL/WhatsApp Video 2026-07-02 at 12.31.37.mp4"    1.0 5 0 panL
norm 06_quarto1 "$DL/WhatsApp Video 2026-07-02 at 12.31.40.mp4"    0.5 4 1 in
norm 07_quarto2 "$DL/WhatsApp Video 2026-07-02 at 12.31.45.mp4"    2.0 5 1 out
norm 08_janela  "$DL/WhatsApp Video 2026-07-02 at 12.32.14.mp4"    6.0 5 0 in
norm 09_piscina "$DL/WhatsApp Video 2026-07-02 at 12.31.58.mp4"    3.0 5 0 panR
norm 10_cta     "$DL/WhatsApp Video 2026-07-02 at 12.32.21 (1).mp4" 1.0 6.5 0 out
echo "=== NORMALIZACAO COMPLETA ==="