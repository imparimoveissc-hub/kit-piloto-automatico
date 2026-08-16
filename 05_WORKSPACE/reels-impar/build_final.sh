#!/bin/zsh
# Master cinematografico: xfade + voz editada + titulos/labels/CTA. Ordem casada com a narracao.
W="/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/reels-impar"
N="$W/norm"
OUT="/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/06_OUTPUTS/reels-impar"
FONT="/System/Library/Fonts/Avenir Next.ttc"
mkdir -p "$OUT"

# ---------- PASS A: xfade concat (ordem casada com a fala) ----------
ffmpeg \
 -i "$N/01_facade.mp4" -i "$N/08_janela.mp4" -i "$N/09_piscina.mp4" -i "$N/05_cozinha.mp4" \
 -i "$N/03_jantar.mp4" -i "$N/02_sala.mp4" -i "$N/07_quarto2.mp4" -i "$N/06_quarto1.mp4" \
 -i "$N/04_vista.mp4" -i "$N/10_cta.mp4" \
 -filter_complex "\
 [0][1]xfade=transition=fade:duration=0.5:offset=4.47[a]; \
 [a][2]xfade=transition=fade:duration=0.5:offset=8.97[b]; \
 [b][3]xfade=transition=fade:duration=0.5:offset=13.47[c]; \
 [c][4]xfade=transition=fade:duration=0.5:offset=17.97[d]; \
 [d][5]xfade=transition=fade:duration=0.5:offset=22.44[e]; \
 [e][6]xfade=transition=fade:duration=0.5:offset=26.94[f]; \
 [f][7]xfade=transition=fade:duration=0.5:offset=31.44[g]; \
 [g][8]xfade=transition=fade:duration=0.5:offset=34.91[h]; \
 [h][9]xfade=transition=fade:duration=0.5:offset=39.41[v]" \
 -map "[v]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p "$W/v_concat.mp4" -y -loglevel error
echo "PASS A OK -> v_concat.mp4"

# ---------- PASS B: titulos + labels + CTA + voz ----------
FF="fontfile=${FONT}"
SH="shadowcolor=black@0.5:shadowx=2:shadowy=2"
# label elegante: aparece de $2 a $3 com fade 0.4s, na base
lt() { echo "drawtext=${FF}:text='$1':fontcolor=white:fontsize=48:${SH}:x=(w-text_w)/2:y=h-260:alpha='if(lt(t,$2),0,if(lt(t,$2+0.4),(t-$2)/0.4,if(lt(t,$3-0.4),1,if(lt(t,$3),($3-t)/0.4,0))))'"; }

WM="drawtext=${FF}:text='I M P A R   I M Ó V E I S':fontcolor=white:fontsize=50:${SH}:x=(w-text_w)/2:y=150:alpha='if(lt(t,0.6),0,if(lt(t,1.3),(t-0.6)/0.7,if(lt(t,3.9),1,if(lt(t,4.4),(4.4-t)/0.5,0))))'"
SUB="drawtext=${FF}:text='Morada Visconde':fontcolor=white:fontsize=40:${SH}:x=(w-text_w)/2:y=222:alpha='if(lt(t,1.0),0,if(lt(t,1.7),(t-1.0)/0.7,if(lt(t,3.9),1,if(lt(t,4.4),(4.4-t)/0.5,0))))'"

# CTA card (scrim escuro + textos)
SCRIM="drawbox=x=0:y=0:w=iw:h=ih:color=black@0.4:t=fill:enable='gte(t,39.7)'"
C1="drawtext=${FF}:text='Disponível para locação':fontcolor=white:fontsize=54:${SH}:x=(w-text_w)/2:y=h/2-160:alpha='if(lt(t,40.0),0,if(lt(t,40.7),(t-40.0)/0.7,1))'"
C2="drawtext=${FF}:text='I M P A R   I M Ó V E I S':fontcolor=white:fontsize=64:${SH}:x=(w-text_w)/2:y=h/2-60:alpha='if(lt(t,40.4),0,if(lt(t,41.1),(t-40.4)/0.7,1))'"
C3="drawtext=${FF}:text='Agende sua visita':fontcolor=white:fontsize=42:${SH}:x=(w-text_w)/2:y=h/2+40:alpha='if(lt(t,40.8),0,if(lt(t,41.5),(t-40.8)/0.7,1))'"
C4="drawtext=${FF}:text='@imparimoveis':fontcolor=white:fontsize=38:${SH}:x=(w-text_w)/2:y=h/2+120:alpha='if(lt(t,41.2),0,if(lt(t,41.9),(t-41.2)/0.7,1))'"

DRAW="${WM},${SUB},\
$(lt 'Vista magnífica' 4.7 8.5),\
$(lt 'Área de festas' 9.2 13.0),\
$(lt 'Churrasqueira integrada' 13.7 17.5),\
$(lt 'Cozinha equipada' 18.2 22.0),\
$(lt 'Living amplo' 22.6 26.5),\
$(lt 'Suíte mobiliada' 27.1 31.0),\
$(lt 'Home office' 31.6 34.5),\
$(lt 'Climatizado e semi-mobiliado' 35.1 39.0),\
${SCRIM},${C1},${C2},${C3},${C4}"

ffmpeg -i "$W/v_concat.mp4" -i "$W/voice_edit.wav" \
 -filter_complex "[0:v]${DRAW},vignette=PI/5:mode=backward[v]; \
 [1:a]afade=t=out:st=44.8:d=0.7[a]" \
 -map "[v]" -map "[a]" -shortest \
 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
 "$OUT/reels-impar-final.mp4" -y -loglevel error
echo "PASS B OK -> $OUT/reels-impar-final.mp4"
ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of default=noprint_wrappers=1 "$OUT/reels-impar-final.mp4"