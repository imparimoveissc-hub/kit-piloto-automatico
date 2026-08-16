#!/usr/bin/env python3
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).with_name("config.json")


def run(cmd, capture=False, check=True, timeout=None):
    if capture:
        result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    else:
        result = subprocess.run(cmd, timeout=timeout)
    if check and result.returncode != 0:
        if capture:
            print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def require_tool(name):
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Ferramenta obrigatória não encontrada: {name}")
    return path


def load_config(preset_name):
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    preset = config["presets"].get(preset_name)
    if not preset:
        names = ", ".join(config["presets"].keys())
        raise SystemExit(f"Preset inválido: {preset_name}. Opções: {names}")
    return preset


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "video"


def ffprobe_duration(path):
    result = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], capture=True)
    return float(result.stdout.strip())


def ffprobe_streams(path):
    result = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_streams", "-show_format", str(path)
    ], capture=True)
    return json.loads(result.stdout)


def detect_silences(path, noise, min_silence):
    result = run([
        "ffmpeg", "-hide_banner", "-i", str(path),
        "-af", f"silencedetect=noise={noise}:d={min_silence}",
        "-f", "null", "-"
    ], capture=True, check=False)

    events = []
    for line in result.stderr.splitlines():
        start = re.search(r"silence_start:\s*([0-9.]+)", line)
        end = re.search(r"silence_end:\s*([0-9.]+)", line)
        if start:
            events.append(("start", float(start.group(1))))
        if end:
            events.append(("end", float(end.group(1))))
    return events


def silence_events_to_keep_segments(events, duration, handle):
    silences = []
    current = None
    for kind, time in events:
        if kind == "start":
            current = time
        elif kind == "end" and current is not None:
            silences.append((current, time))
            current = None
    if current is not None:
        silences.append((current, duration))

    keep = []
    cursor = 0.0
    for start, end in silences:
        keep_end = max(cursor, start + handle)
        if keep_end - cursor > 0.18:
            keep.append((cursor, keep_end))
        cursor = max(cursor, end - handle)
    if duration - cursor > 0.18:
        keep.append((cursor, duration))
    return [(max(0, a), min(duration, b)) for a, b in keep if b > a]


def create_cut_source(input_path, work_dir, args):
    duration = ffprobe_duration(input_path)
    if not args.auto_cut:
        return input_path, duration, []

    events = detect_silences(input_path, args.silence_noise, args.min_silence)
    segments = silence_events_to_keep_segments(events, duration, args.silence_handle)
    if not segments or len(segments) == 1 and math.isclose(segments[0][0], 0, abs_tol=0.2):
        return input_path, duration, []

    segment_dir = work_dir / "segments"
    segment_dir.mkdir(parents=True, exist_ok=True)
    concat_file = work_dir / "concat.txt"
    concat_lines = []

    for index, (start, end) in enumerate(segments, start=1):
        segment_path = segment_dir / f"segment-{index:03d}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner",
            "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
            "-i", str(input_path),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k",
            str(segment_path)
        ])
        concat_lines.append(f"file '{segment_path.as_posix()}'")

    concat_file.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    cut_source = work_dir / "source-cut.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", str(cut_source)
    ])
    return cut_source, ffprobe_duration(cut_source), segments


def escape_filter_path(path):
    return str(path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def build_video_filter(preset, subtitles=None):
    width = preset["width"]
    height = preset["height"]
    filters = [
        f"scale={width}:{height}:force_original_aspect_ratio=increase",
        f"crop={width}:{height}",
        f"fps={preset['fps']}",
        f"eq=contrast={preset['contrast']}:saturation={preset['saturation']}:brightness={preset['brightness']}:gamma={preset['gamma']}",
        "unsharp=5:5:0.55:3:3:0.25"
    ]
    if preset.get("vignette"):
        filters.append("vignette=PI/5")
    if preset.get("grain", 0) > 0:
        filters.append(f"noise=alls={preset['grain']}:allf=t+u")
    if subtitles:
        style = (
            "FontName=Arial,"
            f"FontSize={preset['subtitleFontSize']},"
            "PrimaryColour=&H00FFFFFF,"
            "OutlineColour=&H8A000000,"
            "BorderStyle=1,"
            "Outline=2,"
            "Shadow=0,"
            "Alignment=2,"
            f"MarginV={preset['subtitleMarginV']}"
        )
        filters.append(f"subtitles='{escape_filter_path(subtitles)}':force_style='{style}'")
    return ",".join(filters)


def render_final(source, output_path, preset, subtitles=None):
    video_filter = build_video_filter(preset, subtitles=subtitles)
    run([
        "ffmpeg", "-y", "-hide_banner",
        "-i", str(source),
        "-vf", video_filter,
        "-af", "aresample=48000:async=1:first_pts=0,loudnorm=I=-16:TP=-1.5:LRA=11,acompressor=threshold=-18dB:ratio=2.2:attack=12:release=180",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-b:v", preset["videoBitrate"],
        "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(output_path)
    ], timeout=1800)


def write_report(report_path, data):
    lines = [
        "# Relatório — Editor Cinematográfico",
        "",
        f"- Entrada: `{data['input']}`",
        f"- Saída: `{data['output']}`",
        f"- Preset: `{data['preset']}`",
        f"- Duração original: {data['duration_original']:.2f}s",
        f"- Duração final: {data['duration_final']:.2f}s",
        f"- Auto corte: {'sim' if data['auto_cut'] else 'não'}",
        f"- Legenda aplicada: {'sim' if data['subtitles'] else 'não'}",
    ]
    if data.get("title"):
        lines.append(f"- Título interno: {data['title']}")
    if data.get("segments"):
        lines.extend(["", "## Segmentos mantidos", ""])
        for start, end in data["segments"]:
            lines.append(f"- {start:.2f}s até {end:.2f}s")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Editor cinematográfico automático com FFmpeg.")
    parser.add_argument("input", help="Caminho do vídeo bruto.")
    parser.add_argument("--output-dir", help="Pasta de saída. Padrão: 06_OUTPUTS/cinematic-video-editor/<video>/")
    parser.add_argument("--preset", default="cinematic-reels", help="cinematic-reels, clean-reels, preview-fast ou wide-cinematic.")
    parser.add_argument("--subtitles", help="Arquivo .srt ou .vtt para queimar no vídeo.")
    parser.add_argument("--auto-cut", action="store_true", help="Remove silêncios longos antes de aplicar o look final.")
    parser.add_argument("--silence-noise", default="-35dB", help="Sensibilidade do silencedetect. Padrão: -35dB.")
    parser.add_argument("--min-silence", type=float, default=0.85, help="Silêncio mínimo para corte. Padrão: 0.85s.")
    parser.add_argument("--silence-handle", type=float, default=0.12, help="Respiro antes/depois do corte. Padrão: 0.12s.")
    parser.add_argument("--title", default="", help="Título interno para relatório.")
    return parser.parse_args()


def main():
    args = parse_args()
    require_tool("ffmpeg")
    require_tool("ffprobe")

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Vídeo não encontrado: {input_path}")

    subtitles = Path(args.subtitles).expanduser().resolve() if args.subtitles else None
    if subtitles and not subtitles.exists():
        raise SystemExit(f"Legenda não encontrada: {subtitles}")

    preset = load_config(args.preset)
    base_name = slugify(input_path.stem)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else ROOT / "06_OUTPUTS" / "cinematic-video-editor" / base_name
    work_dir = output_dir / "_work"
    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    duration_original = ffprobe_duration(input_path)
    source, duration_source, segments = create_cut_source(input_path, work_dir, args)

    output_path = output_dir / f"{base_name}-{args.preset}.mp4"
    render_final(source, output_path, preset, subtitles=subtitles)
    duration_final = ffprobe_duration(output_path)

    report_path = output_dir / "relatorio.md"
    write_report(report_path, {
        "input": str(input_path),
        "output": str(output_path),
        "preset": args.preset,
        "duration_original": duration_original,
        "duration_final": duration_final,
        "auto_cut": args.auto_cut,
        "subtitles": str(subtitles) if subtitles else "",
        "title": args.title,
        "segments": segments
    })

    print(json.dumps({
        "ok": True,
        "output": str(output_path),
        "report": str(report_path),
        "durationOriginal": duration_original,
        "durationFinal": duration_final
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
