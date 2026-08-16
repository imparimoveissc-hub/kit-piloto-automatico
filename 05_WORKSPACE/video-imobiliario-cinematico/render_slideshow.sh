#!/usr/bin/env bash
set -euo pipefail

FFMPEG="/Users/user/bin/ffmpeg"
ROOT="/Users/user/Downloads/Kit-Piloto-Automatico-V30-DISTRIB"
OUT="$ROOT/06_OUTPUTS/2026-07-07_video-imobiliario-cinematico"
FR="$OUT/frames"
SEG="$OUT/slideshow_segments"
mkdir -p "$SEG"

images=(
  "9_05.jpg" "1_01.jpg" "2_01.jpg" "2_05.jpg"
  "3_05.jpg" "4_05.jpg" "5_05.jpg" "6_05.jpg"
  "7_05.jpg" "8_05.jpg" "9_05.jpg" "3_01.jpg"
  "4_01.jpg" "5_01.jpg" "6_01.jpg" "7_01.jpg"
  "8_01.jpg" "9_01.jpg" "3_05.jpg" "4_05.jpg"
  "5_05.jpg" "6_05.jpg" "7_05.jpg" "8_05.jpg"
  "9_05.jpg" "1_05.jpg" "3_01.jpg" "4_01.jpg"
  "5_01.jpg" "6_01.jpg" "7_01.jpg" "8_01.jpg"
  "9_01.jpg" "1_01.jpg"
)

i=1
for img in "${images[@]}"; do
  out=$(printf "%s/%02d.mp4" "$SEG" "$i")
  "$FFMPEG" -hide_banner -y -nostdin -loop 1 -t 4 -i "$FR/$img" \
    -f lavfi -t 4 -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -filter_complex "[0:v]scale=1120:1992:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.00055,1.055)':d=120:s=1080x1920:fps=30,eq=contrast=1.07:saturation=1.10:brightness=0.01:gamma=1.05,unsharp=3:3:0.10,format=yuv420p[v]" \
    -map "[v]" -map 1:a:0 -c:v libx264 -preset veryfast -crf 21 -c:a aac -b:a 128k -shortest "$out"
  i=$((i + 1))
done

{
  for n in $(seq -w 1 34); do
    echo "file '$SEG/$n.mp4'"
  done
} > "$OUT/slideshow_concat.txt"

"$FFMPEG" -hide_banner -y -nostdin -f concat -safe 0 -i "$OUT/slideshow_concat.txt" -c copy "$OUT/base-cenas-cinematicas.mp4"

"$FFMPEG" -hide_banner -y -nostdin -i /Users/user/Downloads/2.mov -i /Users/user/Downloads/3.MOV \
  -filter_complex "[0:a]atrim=0:25.70,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=12000,acompressor=threshold=-18dB:ratio=2.2:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=11[a2];[1:a]atrim=1.28:17.42,asetpts=PTS-STARTPTS[a31];[1:a]atrim=17.97:40.61,asetpts=PTS-STARTPTS[a32];[1:a]atrim=41.88:48.61,asetpts=PTS-STARTPTS[a33];[1:a]atrim=52.07:59.39,asetpts=PTS-STARTPTS[a34];[1:a]atrim=62.26:70.26,asetpts=PTS-STARTPTS[a35];[1:a]atrim=72.81:83.17,asetpts=PTS-STARTPTS[a36];[1:a]atrim=86.61:105.42,asetpts=PTS-STARTPTS[a37];[a31][a32][a33][a34][a35][a36][a37]concat=n=7:v=0:a=1,highpass=f=90,lowpass=f=12000,acompressor=threshold=-18dB:ratio=2.2:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=11[a3];anullsrc=channel_layout=stereo:sample_rate=48000,atrim=0:8[sil];[sil][a2][a3]concat=n=3:v=0:a=1[voice]" \
  -map "[voice]" -c:a aac -b:a 192k "$OUT/voz-cortada-tratada.m4a"

"$FFMPEG" -hide_banner -y -nostdin -f lavfi -i "sine=frequency=110:duration=140:sample_rate=48000" \
  -f lavfi -i "sine=frequency=220:duration=140:sample_rate=48000" \
  -f lavfi -i "sine=frequency=330:duration=140:sample_rate=48000" \
  -filter_complex "[0:a]volume=0.018[a0];[1:a]volume=0.012[a1];[2:a]volume=0.007[a2];[a0][a1][a2]amix=inputs=3,afade=t=in:st=0:d=3,afade=t=out:st=132:d=6,alimiter=limit=0.35[m]" \
  -map "[m]" -c:a aac -b:a 128k "$OUT/trilha-cinematica-leve.m4a"

"$FFMPEG" -hide_banner -y -nostdin -i "$OUT/base-cenas-cinematicas.mp4" -i "$OUT/voz-cortada-tratada.m4a" -i "$OUT/trilha-cinematica-leve.m4a" \
  -filter_complex "[2:a]volume=0.28[music];[1:a][music]amix=inputs=2:duration=shortest:dropout_transition=2,loudnorm=I=-15:TP=-1.2:LRA=11[aout]" \
  -map 0:v:0 -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart \
  "$OUT/video-imobiliario-cinematico-PRONTO.mp4"
