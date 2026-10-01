"""
Gerador de Vídeo de Imóvel — Fotos → Reel 9:16
Replica funcionalidade de ferramentas como vinceres.ai

Uso:
    python3 gerar_video_imovel.py \
        --fotos ./fotos_teste/ \
        --titulo "Apartamento 3 Quartos" \
        --subtitulo "Centro • 120m² • R$ 850.000" \
        --cta "Fale com um corretor" \
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


OUTPUT_W = 1080
OUTPUT_H = 1920
FPS = 30
DURACAO_FOTO = 3.5
DURACAO_TITULO_FINAL = 3.0


def preparar_foto(img_path: str, saida: str) -> None:
    """Redimensiona e recorta foto para cobrir 1080×1920 sem distorção."""
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    ratio_out = OUTPUT_W / OUTPUT_H
    ratio_in = w / h

    if ratio_in > ratio_out:
        new_h = h
        new_w = int(h * ratio_out)
    else:
        new_w = w
        new_h = int(w / ratio_out)

    left = (w - new_w) // 2
    top = (h - new_h) // 2
    img = img.crop((left, top, left + new_w, top + new_h))
    img = img.resize((OUTPUT_W * 2, OUTPUT_H * 2), Image.LANCZOS)  # 2x para o zoompan ter espaço
    img.save(saida, "JPEG", quality=95)


def segmento_ken_burns(foto_prep: str, duracao: float, direcao: str, saida: str) -> None:
    """Gera segmento de vídeo com efeito Ken Burns via ffmpeg zoompan."""
    n_frames = int(duracao * FPS)

    # Fórmulas zoompan para cada direção
    # z=zoom, x=posição horizontal, y=posição vertical
    # Valores relativos ao tamanho da imagem de entrada (2×saída)
    if direcao == "zoom_in":
        z_expr  = f"'1.0+0.15*on/{n_frames}'"
        x_expr  = f"'iw/2-(iw/zoom/2)'"
        y_expr  = f"'ih/2-(ih/zoom/2)+ih*0.03*on/{n_frames}'"
    elif direcao == "zoom_out":
        z_expr  = f"'1.15-0.15*on/{n_frames}'"
        x_expr  = f"'iw/2-(iw/zoom/2)'"
        y_expr  = f"'ih/2-(ih/zoom/2)-ih*0.03*on/{n_frames}'"
    elif direcao == "pan_right":
        z_expr  = "'1.08'"
        x_expr  = f"'(iw/2-(iw/zoom/2))+iw*0.06*on/{n_frames}'"
        y_expr  = f"'ih/2-(ih/zoom/2)'"
    else:  # pan_left
        z_expr  = "'1.08'"
        x_expr  = f"'(iw/2-(iw/zoom/2))-iw*0.06*on/{n_frames}'"
        y_expr  = f"'ih/2-(ih/zoom/2)'"

    vf = (
        f"zoompan=z={z_expr}:x={x_expr}:y={y_expr}"
        f":d={n_frames}:s={OUTPUT_W}x{OUTPUT_H}:fps={FPS},"
        f"setsar=1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duracao),
        "-i", foto_prep,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-t", str(duracao),
        saida,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou: {result.stderr[-500:]}")


def criar_slide_final(titulo: str, subtitulo: str, cta: str, saida: str) -> None:
    """Cria slide final estático com título, subtítulo e CTA."""
    try:
        font_tit = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 46)
        font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    except Exception:
        font_tit = font_sub = font_cta = ImageFont.load_default()

    img = Image.new("RGB", (OUTPUT_W, OUTPUT_H), (18, 18, 18))
    draw = ImageDraw.Draw(img)

    # Linha dourada decorativa
    draw.rectangle([80, 700, OUTPUT_W - 80, 707], fill=(200, 160, 60))

    # Textos
    itens = [
        (titulo,    font_tit, 740, (255, 255, 255)),
        (subtitulo, font_sub, 850, (180, 180, 180)),
        (cta,       font_cta, 980, (200, 160, 60)),
    ]
    for texto, font, y, cor in itens:
        bbox = draw.textbbox((0, 0), texto, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((OUTPUT_W - tw) // 2, y), texto, font=font, fill=cor)

    # Salvar frame e converter para vídeo estático
    tmp_frame = saida.replace(".mp4", "_frame.jpg")
    img.save(tmp_frame, "JPEG", quality=95)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(DURACAO_TITULO_FINAL),
        "-i", tmp_frame,
        "-vf", f"scale={OUTPUT_W}:{OUTPUT_H},setsar=1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),  # mesmo fps dos segmentos zoompan
        saida,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(tmp_frame)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou no slide final: {result.stderr[-500:]}")


def concat_segmentos(segmentos: list[str], saida: str) -> None:
    """Concatena segmentos de vídeo usando ffmpeg concat demuxer (por arquivo, não frame)."""
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
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(lista.name)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg concat falhou: {result.stderr[-500:]}")


def adicionar_musica(video: str, musica: str, saida: str) -> None:
    cmd = [
        "ffmpeg", "-y",
        "-i", video,
        "-i", musica,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-af", "volume=0.6",
        saida,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg áudio falhou: {result.stderr[-500:]}")


def gerar_video(pasta_fotos: str, titulo: str, subtitulo: str, cta: str,
                saida: str, musica: str | None = None) -> None:

    fotos = sorted(
        glob.glob(os.path.join(pasta_fotos, "*.jpg")) +
        glob.glob(os.path.join(pasta_fotos, "*.jpeg")) +
        glob.glob(os.path.join(pasta_fotos, "*.png"))
    )
    if not fotos:
        raise ValueError(f"Nenhuma foto encontrada em: {pasta_fotos}")

    print(f"📸 {len(fotos)} foto(s) encontrada(s)")

    tmp_dir = tempfile.mkdtemp(prefix="imovel_video_")
    segmentos = []
    direcoes = ["zoom_in", "zoom_out", "pan_right", "pan_left"]

    try:
        for i, foto in enumerate(fotos):
            print(f"  🎬 [{i+1}/{len(fotos)}] {Path(foto).name} — efeito: {direcoes[i % 4]}")
            foto_prep = os.path.join(tmp_dir, f"prep_{i:02d}.jpg")
            seg_path  = os.path.join(tmp_dir, f"seg_{i:02d}.mp4")

            preparar_foto(foto, foto_prep)
            segmento_ken_burns(foto_prep, DURACAO_FOTO, direcoes[i % 4], seg_path)
            segmentos.append(seg_path)

        print("  🎬 Criando slide final...")
        slide_path = os.path.join(tmp_dir, "slide_final.mp4")
        criar_slide_final(titulo, subtitulo, cta, slide_path)
        segmentos.append(slide_path)

        print(f"  🔧 Concatenando {len(segmentos)} segmentos...")
        video_concat = os.path.join(tmp_dir, "concat.mp4")
        concat_segmentos(segmentos, video_concat)

        if musica and os.path.exists(musica):
            print("  🎵 Adicionando música...")
            adicionar_musica(video_concat, musica, saida)
        else:
            shutil.copy(video_concat, saida)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    tamanho = os.path.getsize(saida) / 1024 / 1024
    duracao = len(fotos) * DURACAO_FOTO + DURACAO_TITULO_FINAL
    print(f"\n✅ Vídeo gerado: {saida}")
    print(f"   {OUTPUT_W}×{OUTPUT_H} | {FPS}fps | ~{duracao:.0f}s | {tamanho:.1f} MB | Reel 9:16")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fotos de imóvel → Vídeo Reel 9:16")
    parser.add_argument("--fotos",     required=True)
    parser.add_argument("--titulo",    required=True)
    parser.add_argument("--subtitulo", required=True)
    parser.add_argument("--cta",       default="Fale com um corretor")
    parser.add_argument("--saida",     default="video_imovel.mp4")
    parser.add_argument("--musica",    default=None)
    args = parser.parse_args()

    gerar_video(
        pasta_fotos=args.fotos,
        titulo=args.titulo,
        subtitulo=args.subtitulo,
        cta=args.cta,
        saida=args.saida,
        musica=args.musica,
    )
