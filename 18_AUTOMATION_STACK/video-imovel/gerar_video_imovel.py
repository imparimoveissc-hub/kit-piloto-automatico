"""
Gerador de Vídeo de Imóvel — Fotos → Vídeo Cinematográfico

Movimentos com easing cossenoidal + crossfade entre fotos.

Movimentos:
  tilt_up     — câmera sobe suave
  tilt_down   — câmera desce suave
  dolly_in    — zoom in centrado
  dolly_out   — zoom out centrado
  pan_right   — panorâmica direita
  pan_left    — panorâmica esquerda
  orbit_right — zoom in + pan direita (efeito orbital)
  orbit_left  — zoom in + pan esquerda
  push_in     — push dramático: zoom rápido + leve subida
  float_up    — deriva diagonal suave com respiro
  diagonal    — drift diagonal: zoom + pan diagonal
  static      — leve respiro (zoom senoidal)

Uso:
    python3 gerar_video_imovel.py \
        --fotos ./fotos/ \
        --movimentos "dolly_in,orbit_right,tilt_up,push_in" \
        --formato landscape \
        --resolucao fhd \
        --trilha musica.mp3 \
        --saida video_imovel.mp4
"""

import argparse
import os
import subprocess
import tempfile
import glob
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Configurações ────────────────────────────────────────────────────────────
RESOLUCOES = {
    "hd":  (1280,  720),
    "fhd": (1920, 1080),
    "4k":  (3840, 2160),
}

FORMATOS = {
    "landscape": (16, 9),
    "portrait":  (9, 16),
    "square":    (1, 1),
}

FPS           = 30
DURACAO_FOTO  = 5.0   # segundos por foto (mais tempo = movimento mais suave)
DURACAO_FINAL = 4.0   # slide de encerramento
TRANS_DUR     = 0.65  # crossfade entre fotos (segundos)
ESCALA        = 1.42  # margem de zoom/pan (maior = mais travel room)

# Sequência automática: diversidade de movimentos por foto
MOVIMENTOS_AUTO = [
    "dolly_in", "orbit_right", "tilt_up", "push_in",
    "pan_right", "float_up", "dolly_out", "orbit_left",
    "tilt_down", "diagonal", "pan_left", "static",
]


# ── Preparação de imagem ─────────────────────────────────────────────────────

def preparar_foto(img_path: str, saida: str, w: int, h: int, escala: float = ESCALA) -> None:
    """
    Recorta e escala a foto para cobrir w×h com margem para movimentos.
    A imagem final tem (w*escala) × (h*escala) pixels.
    """
    img = Image.open(img_path).convert("RGB")
    ow, oh = img.size
    ratio_out = w / h
    ratio_in  = ow / oh

    if ratio_in > ratio_out:
        ch, cw = oh, int(oh * ratio_out)
    else:
        cw, ch = ow, int(ow / ratio_out)
    left = (ow - cw) // 2
    top  = (oh - ch) // 2
    img = img.crop((left, top, left + cw, top + ch))

    tw = int(w * escala / 2) * 2
    th = int(h * escala / 2) * 2
    img = img.resize((tw, th), Image.LANCZOS)

    # Leve aumento de contraste para look mais cinematográfico
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(img).enhance(1.06)

    img.save(saida, "JPEG", quality=95)


# ── Expressões de easing ─────────────────────────────────────────────────────

def _ease(n: int) -> str:
    """Ease-in-out cossenoidal: 0 → 1 suavemente em N frames."""
    return f"(1-cos(3.14159265*on/{n}))/2"

def _ease_in(n: int) -> str:
    """Ease-in: começa lento, termina rápido."""
    return f"(1-cos(3.14159265/2*on/{n}))"

def _ease_out(n: int) -> str:
    """Ease-out: começa rápido, termina lento."""
    return f"sin(3.14159265/2*on/{n})"


# ── Movimentos cinematográficos ──────────────────────────────────────────────

def _zoompan_expr(movimento: str, duracao: float, w: int, h: int) -> str:
    """
    Retorna filtro zoompan FFmpeg com easing cossenoidal.

    Sistema de coordenadas:
      - Fonte: iw × ih  (= w*ESCALA × h*ESCALA)
      - Saída: ow × oh  (= w × h)
      - At z=1.0: crop = ow×oh, range de x=[0, iw-ow], y=[0, ih-oh]
      - Centro (z=1.0): x = iw/2-ow/2, y = ih/2-oh/2
      - Centro (z>1.0): x = iw/2-ow/zoom/2, y = ih/2-oh/zoom/2
    """
    n = int(duracao * FPS)
    e  = _ease(n)       # ease-in-out: 0→1
    ei = _ease_in(n)    # ease-in: 0→1 acelerando
    eo = _ease_out(n)   # ease-out: 0→1 desacelerando

    # Deslocamento lateral disponível (Z=1.0): (ESCALA-1)/2 × ow
    # Com ESCALA=1.42, isso é 0.21×ow de cada lado.
    # Usando 65% do disponível para deixar margem de segurança.
    dx = 0.14   # fração de ow para pan horizontal
    dy = 0.14   # fração de oh para pan vertical

    if movimento == "dolly_in":
        # Zoom suave 1.0 → 1.20, centrado, ease-in-out
        z = f"1.0+0.20*({e})"
        x = "iw/2-ow/zoom/2"
        y = "ih/2-oh/zoom/2"

    elif movimento == "dolly_out":
        # Zoom suave 1.20 → 1.0, centrado, ease-in-out
        z = f"1.20-0.20*({e})"
        x = "iw/2-ow/zoom/2"
        y = "ih/2-oh/zoom/2"

    elif movimento == "tilt_up":
        # Câmera sobe: y de centro-baixo → centro-alto, ease-in-out
        z = "1.0"
        x = "iw/2-ow/2"
        y = f"ih/2-oh/2+oh*{dy}-oh*{dy}*2*({e})"

    elif movimento == "tilt_down":
        # Câmera desce: y de centro-alto → centro-baixo
        z = "1.0"
        x = "iw/2-ow/2"
        y = f"ih/2-oh/2-oh*{dy}+oh*{dy}*2*({e})"

    elif movimento == "pan_right":
        # Pan da esquerda para direita, ease-in-out
        z = "1.0"
        x = f"iw/2-ow/2-ow*{dx}+ow*{dx}*2*({e})"
        y = "ih/2-oh/2"

    elif movimento == "pan_left":
        # Pan da direita para esquerda
        z = "1.0"
        x = f"iw/2-ow/2+ow*{dx}-ow*{dx}*2*({e})"
        y = "ih/2-oh/2"

    elif movimento == "orbit_right":
        # Zoom in + pan direita simultâneos → sensação orbital
        z = f"1.0+0.16*({e})"
        x = f"iw/2-ow/zoom/2+ow*0.09*({e})"
        y = "ih/2-oh/zoom/2"

    elif movimento == "orbit_left":
        # Zoom in + pan esquerda
        z = f"1.0+0.16*({e})"
        x = f"iw/2-ow/zoom/2-ow*0.09*({e})"
        y = "ih/2-oh/zoom/2"

    elif movimento == "push_in":
        # Push dramático: zoom rápido 1.0 → 1.28 com leve subida
        # Usa ease-in para energia crescente
        z = f"1.0+0.28*({ei})"
        x = "iw/2-ow/zoom/2"
        y = f"ih/2-oh/zoom/2-oh*0.04*({e})"

    elif movimento == "float_up":
        # Deriva muito suave para cima com respiro leve — sensação etérea
        z = f"1.04+0.025*sin(3.14159265*on/{n})"
        x = "iw/2-ow/zoom/2"
        y = f"ih/2-oh/zoom/2-oh*{dy}*({eo})"

    elif movimento == "diagonal":
        # Drift diagonal: zoom in + pan up-right
        z = f"1.0+0.14*({e})"
        x = f"iw/2-ow/zoom/2+ow*0.07*({e})"
        y = f"ih/2-oh/zoom/2-oh*0.06*({e})"

    else:  # static — leve respiro senoidal
        z = f"1.0+0.025*sin(3.14159265*on/{n})"
        x = "iw/2-ow/zoom/2"
        y = "ih/2-oh/zoom/2"

    # Color grade suave: leve aumento de contraste via filtro eq
    grade = ",eq=contrast=1.05:saturation=0.90:brightness=-0.005"

    return (
        f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={w}x{h}:fps={FPS}"
        f",setsar=1{grade}"
    )


def segmento_video(foto_prep: str, duracao: float, movimento: str, w: int, h: int, saida: str) -> None:
    vf = _zoompan_expr(movimento, duracao, w, h)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duracao + 0.1),  # +0.1s para evitar frame missing no xfade
        "-i", foto_prep,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-t", str(duracao),
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou ({movimento}): {r.stderr[-500:]}")


# ── Slide de encerramento ────────────────────────────────────────────────────

def slide_final(titulo: str, subtitulo: str, cta: str, w: int, h: int, saida: str) -> None:
    # Gradient escuro com toque quente
    img = Image.new("RGB", (w, h), (9, 9, 15))
    draw = ImageDraw.Draw(img)

    # Gradiente suave do centro para as bordas (simulado com retângulos)
    for i in range(60):
        alpha = int(30 * (1 - i / 60))
        r_val = 9 + i // 4
        draw.rectangle([i*w//120, i*h//120, w - i*w//120, h - i*h//120],
                       outline=(r_val, r_val, r_val + 6))

    # Linha dourada horizontal (topo da área de texto)
    cy = h // 2 - h // 10
    bar_x1, bar_x2 = w // 6, w - w // 6
    draw.rectangle([bar_x1, cy - 2, bar_x2, cy + 2], fill=(200, 164, 69))

    # Fontes
    font_paths = [
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font_regular_paths = [
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    def load_font(paths, size):
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
        return ImageFont.load_default()

    size_titulo = max(36, h // 18)
    size_sub    = max(24, h // 30)
    size_cta    = max(28, h // 24)

    f_tit = load_font(font_paths, size_titulo)
    f_sub = load_font(font_regular_paths, size_sub)
    f_cta = load_font(font_paths, size_cta)

    gap = h // 24
    y = cy + gap

    items = [
        (titulo,    f_tit, (255, 255, 255)),
        (subtitulo, f_sub, (160, 160, 165)),
        (cta,       f_cta, (200, 164, 69)),
    ]

    for txt, font, cor in items:
        if not txt:
            continue
        bbox = draw.textbbox((0, 0), txt, font=font)
        tw = bbox[2] - bbox[0]
        th_item = bbox[3] - bbox[1]
        draw.text(((w - tw) // 2, y), txt, font=font, fill=cor)
        y += th_item + gap

    # Blur suave nas bordas para vinheta
    mask = Image.new("L", (w, h), 255)
    mask_draw = ImageDraw.Draw(mask)
    vign = min(w, h) // 8
    for i in range(vign):
        v = int(255 * (i / vign) ** 0.5)
        mask_draw.rectangle([i, i, w - i, h - i], outline=v)
    vign_layer = Image.new("RGB", (w, h), (0, 0, 0))
    img = Image.composite(img, vign_layer, mask)

    tmp_frame = saida.replace(".mp4", "_frame.jpg")
    img.save(tmp_frame, "JPEG", quality=95)

    vf = (
        f"scale={w}:{h},setsar=1"
        f",zoompan=z='1.0+0.04*((1-cos(3.14159265*on/{int(DURACAO_FINAL*FPS)}))/2)'"
        f":x='iw/2-ow/zoom/2':y='ih/2-oh/zoom/2'"
        f":d={int(DURACAO_FINAL*FPS)}:s={w}x{h}:fps={FPS},setsar=1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(DURACAO_FINAL + 0.1),
        "-i", tmp_frame,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-t", str(DURACAO_FINAL),
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(tmp_frame)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg slide final: {r.stderr[-500:]}")


# ── Concatenar com crossfade ─────────────────────────────────────────────────

def concat_com_xfade(segmentos: list, duracoes: list, saida: str, trans_dur: float = TRANS_DUR) -> None:
    """Concatena segmentos com dissolve suave (xfade) entre eles."""
    n = len(segmentos)

    if n == 1:
        shutil.copy(segmentos[0], saida)
        return

    # Fallback para concat simples se só 2 segmentos e problemas com xfade
    inputs = []
    for s in segmentos:
        inputs += ["-i", s]

    # Construir cadeia de xfade
    # offset_i = sum(duracoes[0..i]) - (i+1)*trans_dur
    filters = []
    prev = "[0:v]"
    running = 0.0

    for i in range(n - 1):
        running += duracoes[i]
        offset = running - (i + 1) * trans_dur
        next_in = f"[{i+1}:v]"
        out_lbl = "[vout]" if i == n - 2 else f"[v{i+1}]"
        filters.append(
            f"{prev}{next_in}xfade=transition=fade:duration={trans_dur:.3f}:offset={offset:.3f}{out_lbl}"
        )
        prev = out_lbl

    filter_complex = ";".join(filters)

    cmd = [
        "ffmpeg", "-y",
    ] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # Fallback: concat sem xfade
        print("  ⚠ xfade falhou, usando concat simples...")
        _concat_simples(segmentos, saida)


def _concat_simples(segmentos: list, saida: str) -> None:
    lista = tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False)
    for s in segmentos:
        lista.write(f"file '{s}'\n")
    lista.close()
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", lista.name,
        "-c", "copy",
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(lista.name)
    if r.returncode != 0:
        raise RuntimeError(f"Concat falhou: {r.stderr[-400:]}")


# ── Adicionar trilha ─────────────────────────────────────────────────────────

def adicionar_trilha(video: str, trilha: str, saida: str, duracao_total: float) -> None:
    fade_start = max(0, duracao_total - 2.5)
    cmd = [
        "ffmpeg", "-y",
        "-i", video,
        "-i", trilha,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-af", f"volume=0.60,afade=t=in:st=0:d=1.0,afade=t=out:st={fade_start:.1f}:d=2.5",
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Trilha falhou: {r.stderr[-400:]}")


# ── Pipeline principal ───────────────────────────────────────────────────────

def gerar_video(
    pasta_fotos: str,
    titulo: str     = "",
    subtitulo: str  = "",
    cta: str        = "",
    movimentos: str = "",
    formato: str    = "landscape",
    resolucao: str  = "fhd",
    trilha: str     = None,
    saida: str      = "video_imovel.mp4",
) -> None:

    fotos = sorted(
        glob.glob(os.path.join(pasta_fotos, "*.jpg"))  +
        glob.glob(os.path.join(pasta_fotos, "*.jpeg")) +
        glob.glob(os.path.join(pasta_fotos, "*.png"))
    )
    if not fotos:
        raise ValueError(f"Nenhuma foto em: {pasta_fotos}")

    base_w, base_h = RESOLUCOES.get(resolucao, RESOLUCOES["fhd"])
    rx, ry = FORMATOS.get(formato, FORMATOS["landscape"])
    if rx > ry:
        w, h = base_w, base_h
    elif rx < ry:
        w, h = base_h, base_w
    else:
        s = min(base_w, base_h)
        w = h = s

    print(f"📸 {len(fotos)} foto(s) | {w}×{h} | {resolucao.upper()} | {formato}")

    mov_lista = [m.strip() for m in movimentos.split(",") if m.strip()] if movimentos else []

    tmp_dir   = tempfile.mkdtemp(prefix="imovel_")
    segmentos = []
    duracoes  = []

    try:
        for i, foto in enumerate(fotos):
            mov = mov_lista[i] if i < len(mov_lista) else MOVIMENTOS_AUTO[i % len(MOVIMENTOS_AUTO)]
            print(f"  🎬 [{i+1}/{len(fotos)}] {Path(foto).name} — {mov}")

            foto_prep = os.path.join(tmp_dir, f"prep_{i:02d}.jpg")
            seg_path  = os.path.join(tmp_dir, f"seg_{i:02d}.mp4")

            preparar_foto(foto, foto_prep, w, h)
            segmento_video(foto_prep, DURACAO_FOTO, mov, w, h, seg_path)
            segmentos.append(seg_path)
            duracoes.append(DURACAO_FOTO)

        if titulo or subtitulo or cta:
            print("  🎬 Slide de encerramento...")
            slide_path = os.path.join(tmp_dir, "slide_final.mp4")
            slide_final(titulo or "", subtitulo or "", cta or "", w, h, slide_path)
            segmentos.append(slide_path)
            duracoes.append(DURACAO_FINAL)

        print(f"  ✨ Crossfade entre {len(segmentos)} segmentos ({TRANS_DUR}s)...")
        video_concat = os.path.join(tmp_dir, "concat.mp4")
        concat_com_xfade(segmentos, duracoes, video_concat)

        duracao_total = sum(duracoes) - (len(duracoes) - 1) * TRANS_DUR

        if trilha and os.path.exists(trilha):
            print("  🎵 Adicionando trilha...")
            adicionar_trilha(video_concat, trilha, saida, duracao_total)
        else:
            shutil.copy(video_concat, saida)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    mb = os.path.getsize(saida) / 1024 / 1024
    print(f"\n✅ {saida} — {mb:.1f} MB — {duracao_total:.1f}s — {w}×{h} {FPS}fps")


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Fotos de imóvel → Vídeo cinematográfico")
    p.add_argument("--fotos",      required=True)
    p.add_argument("--titulo",     default="")
    p.add_argument("--subtitulo",  default="")
    p.add_argument("--cta",        default="")
    p.add_argument("--movimentos", default="")
    p.add_argument("--formato",    default="landscape", choices=["landscape","portrait","square"])
    p.add_argument("--resolucao",  default="fhd",       choices=["hd","fhd","4k"])
    p.add_argument("--trilha",     default=None)
    p.add_argument("--saida",      default="video_imovel.mp4")
    args = p.parse_args()

    gerar_video(
        pasta_fotos=args.fotos,
        titulo=args.titulo,
        subtitulo=args.subtitulo,
        cta=args.cta,
        movimentos=args.movimentos,
        formato=args.formato,
        resolucao=args.resolucao,
        trilha=args.trilha,
        saida=args.saida,
    )
