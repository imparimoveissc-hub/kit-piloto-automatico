"""
Gerador de Vídeo de Imóvel — Fotos → Vídeo Cinematográfico
Replica funcionalidade de ferramentas como vinceres.ai

Movimentos suportados:
  tilt_up   — câmera sobe (bottom → top)
  tilt_down — câmera desce (top → bottom)
  dolly_in  — câmera avança (zoom in suave, perspectiva constante)
  dolly_out — câmera recua (zoom out suave)
  pan_right — câmera pan para a direita
  pan_left  — câmera pan para a esquerda
  static    — foto estática com leve respiração

Formatos de saída:
  landscape — 1920×1080 (feed, WhatsApp, YouTube)
  portrait  — 1080×1920 (Reels, Stories, TikTok)
  square    — 1080×1080 (feed Instagram)

Uso:
    python3 gerar_video_imovel.py \
        --fotos ./fotos/ \
        --movimentos "tilt_up,dolly_in,pan_right,dolly_out" \
        --formato landscape \
        --resolucao hd \
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
from PIL import Image, ImageDraw, ImageFont


# ── Resoluções ───────────────────────────────────────────────────────────────
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

FPS = 30
DURACAO_FOTO  = 4.0   # segundos por foto
DURACAO_FINAL = 3.5   # slide de encerramento


# ── Preparação de imagem ─────────────────────────────────────────────────────

def preparar_foto(img_path: str, saida: str, w: int, h: int, escala: float = 1.3) -> None:
    """
    Recorta e escala a foto para cobrir w×h com margem de zoom/pan.
    escala > 1 garante que há espaço para mover sem revelar bordas pretas.
    """
    img = Image.open(img_path).convert("RGB")
    ow, oh = img.size
    ratio_out = w / h
    ratio_in  = ow / oh

    # Recorte central mantendo aspect ratio
    if ratio_in > ratio_out:
        ch, cw = oh, int(oh * ratio_out)
    else:
        cw, ch = ow, int(ow / ratio_out)
    left = (ow - cw) // 2
    top  = (oh - ch) // 2
    img = img.crop((left, top, left + cw, top + ch))

    # Escalar para w×h com margem
    tw = int(w * escala / 2) * 2
    th = int(h * escala / 2) * 2
    img = img.resize((tw, th), Image.LANCZOS)
    img.save(saida, "JPEG", quality=95)


# ── Movimentos cinematográficos ──────────────────────────────────────────────

def _zoompan_expr(movimento: str, duracao: float, w: int, h: int) -> str:
    """Retorna filtro zoompan para o movimento solicitado."""
    n   = int(duracao * FPS)
    iw  = "iw"  # largura da imagem preparada (w * escala)
    ih  = "ih"

    # zoom base: 1.0 = tamanho exato da saída (a imagem preparada é 1.3× maior)
    # A imagem foi escalada para w*1.3, mas zoompan recebe essa imagem e faz output w×h.
    # Então zoom=1.0 exibe a imagem centralizada sem bordas pretas.

    if movimento == "tilt_up":
        # Câmera sobe: y começa no fundo, termina no topo
        z   = "'1.0'"
        x   = f"'({iw}/2)-(ow/2)'"
        y   = f"'({ih}-oh)-({ih}-oh)*on/{n}'"

    elif movimento == "tilt_down":
        z   = "'1.0'"
        x   = f"'({iw}/2)-(ow/2)'"
        y   = f"'({ih}-oh)*on/{n}'"

    elif movimento == "dolly_in":
        # Zoom suave de 1.0 → 1.18 centrado
        z   = f"'1.0+0.18*on/{n}'"
        x   = f"'({iw}/2)-(ow/zoom/2)'"
        y   = f"'({ih}/2)-(oh/zoom/2)'"

    elif movimento == "dolly_out":
        z   = f"'1.18-0.18*on/{n}'"
        x   = f"'({iw}/2)-(ow/zoom/2)'"
        y   = f"'({ih}/2)-(oh/zoom/2)'"

    elif movimento == "pan_right":
        z   = "'1.0'"
        x   = f"'({iw}/2-ow/2)+({iw}-ow)*0.12*on/{n}'"
        y   = f"'({ih}/2)-(oh/2)'"

    elif movimento == "pan_left":
        z   = "'1.0'"
        x   = f"'({iw}/2-ow/2)-({iw}-ow)*0.12*on/{n}+({iw}-ow)*0.12'"
        y   = f"'({ih}/2)-(oh/2)'"

    else:  # static — leve respiração
        z   = f"'1.0+0.03*sin(on*3.14/{n})'"
        x   = f"'({iw}/2)-(ow/zoom/2)'"
        y   = f"'({ih}/2)-(oh/zoom/2)'"

    return f"zoompan=z={z}:x={x}:y={y}:d={n}:s={w}x{h}:fps={FPS},setsar=1"


def segmento_video(foto_prep: str, duracao: float, movimento: str, w: int, h: int, saida: str) -> None:
    n = int(duracao * FPS)
    vf = _zoompan_expr(movimento, duracao, w, h)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duracao),
        "-i", foto_prep,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-t", str(duracao),
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou ({movimento}): {r.stderr[-400:]}")


# ── Slide de encerramento ────────────────────────────────────────────────────

def slide_final(titulo: str, subtitulo: str, cta: str, w: int, h: int, saida: str) -> None:
    try:
        f_tit = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(32, h // 22))
        f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",      max(22, h // 34))
        f_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(26, h // 28))
    except Exception:
        f_tit = f_sub = f_cta = ImageFont.load_default()

    img  = Image.new("RGB", (w, h), (16, 16, 16))
    draw = ImageDraw.Draw(img)

    cx = w // 2
    cy = h // 2 - h // 8

    # Linha dourada
    draw.rectangle([w // 8, cy - 20, w - w // 8, cy - 14], fill=(200, 160, 60))

    itens = [
        (titulo,    f_tit, cy + 10,  (255, 255, 255)),
        (subtitulo, f_sub, cy + 10 + h // 16, (170, 170, 170)),
        (cta,       f_cta, cy + 10 + h // 16 + h // 12, (200, 160, 60)),
    ]
    for txt, font, y, cor in itens:
        if not txt:
            continue
        bbox = draw.textbbox((0, 0), txt, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((w - tw) // 2, y), txt, font=font, fill=cor)

    tmp_frame = saida.replace(".mp4", "_frame.jpg")
    img.save(tmp_frame, "JPEG", quality=95)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(DURACAO_FINAL),
        "-i", tmp_frame,
        "-vf", f"scale={w}:{h},setsar=1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        saida,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(tmp_frame)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg slide final: {r.stderr[-400:]}")


# ── Concatenar segmentos ─────────────────────────────────────────────────────

def concat_segmentos(segmentos: list[str], saida: str) -> None:
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
    fade_start = max(0, duracao_total - 2.0)
    cmd = [
        "ffmpeg", "-y",
        "-i", video,
        "-i", trilha,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-af", f"volume=0.65,afade=t=out:st={fade_start:.1f}:d=2",
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
    movimentos: str = "",          # "tilt_up,dolly_in,pan_right,dolly_out"
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

    # Resolução base × ratio do formato
    base_w, base_h = RESOLUCOES.get(resolucao, RESOLUCOES["fhd"])
    rx, ry = FORMATOS.get(formato, FORMATOS["landscape"])
    if rx > ry:  # landscape
        w, h = base_w, base_h
    elif rx < ry:  # portrait
        w, h = base_h, base_w
    else:          # square
        s = min(base_w, base_h)
        w = h = s

    print(f"📸 {len(fotos)} foto(s) | {w}×{h} | {resolucao.upper()} | {formato}")

    # Movimentos por foto
    mov_lista = [m.strip() for m in movimentos.split(",") if m.strip()] if movimentos else []
    MOVIMENTOS_AUTO = ["tilt_up", "dolly_in", "pan_right", "dolly_out", "tilt_down", "pan_left"]

    tmp_dir   = tempfile.mkdtemp(prefix="imovel_")
    segmentos = []

    try:
        for i, foto in enumerate(fotos):
            mov = mov_lista[i] if i < len(mov_lista) else MOVIMENTOS_AUTO[i % len(MOVIMENTOS_AUTO)]
            print(f"  🎬 [{i+1}/{len(fotos)}] {Path(foto).name} — {mov}")

            foto_prep = os.path.join(tmp_dir, f"prep_{i:02d}.jpg")
            seg_path  = os.path.join(tmp_dir, f"seg_{i:02d}.mp4")

            preparar_foto(foto, foto_prep, w, h, escala=1.25)
            segmento_video(foto_prep, DURACAO_FOTO, mov, w, h, seg_path)
            segmentos.append(seg_path)

        if titulo or subtitulo or cta:
            print("  🎬 Slide de encerramento...")
            slide_path = os.path.join(tmp_dir, "slide_final.mp4")
            slide_final(titulo or "", subtitulo or "", cta or "", w, h, slide_path)
            segmentos.append(slide_path)

        print(f"  🔧 Concatenando {len(segmentos)} segmentos...")
        video_concat = os.path.join(tmp_dir, "concat.mp4")
        concat_segmentos(segmentos, video_concat)

        duracao_total = len(fotos) * DURACAO_FOTO + (DURACAO_FINAL if titulo else 0)

        if trilha and os.path.exists(trilha):
            print("  🎵 Adicionando trilha...")
            adicionar_trilha(video_concat, trilha, saida, duracao_total)
        else:
            shutil.copy(video_concat, saida)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    mb = os.path.getsize(saida) / 1024 / 1024
    print(f"\n✅ {saida} — {mb:.1f} MB — {duracao_total:.0f}s — {w}×{h} {FPS}fps")


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Fotos de imóvel → Vídeo cinematográfico")
    p.add_argument("--fotos",      required=True,       help="Pasta com as fotos")
    p.add_argument("--titulo",     default="",          help="Título para slide final")
    p.add_argument("--subtitulo",  default="",          help="Subtítulo (ex: 120m² • R$ 850.000)")
    p.add_argument("--cta",        default="",          help="Chamada para ação")
    p.add_argument("--movimentos", default="",          help="Ex: tilt_up,dolly_in,pan_right,dolly_out")
    p.add_argument("--formato",    default="landscape", choices=["landscape","portrait","square"])
    p.add_argument("--resolucao",  default="fhd",       choices=["hd","fhd","4k"])
    p.add_argument("--trilha",     default=None,        help="Trilha .mp3/.aac")
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
