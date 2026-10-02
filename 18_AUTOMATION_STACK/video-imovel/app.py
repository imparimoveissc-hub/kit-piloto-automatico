"""
IMPAR STUDIO — Servidor Flask
Roda em: python3 app.py  →  http://localhost:5001
"""

import os, sys, uuid, json, time, threading, shutil, subprocess
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, Response
from werkzeug.utils import secure_filename

try:
    import requests as _requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

BASE_DIR    = Path(__file__).parent
UPLOAD_DIR  = BASE_DIR / "uploads"
OUTPUT_DIR  = BASE_DIR / "outputs"
SCRIPT_PATH = BASE_DIR / "gerar_video_imovel.py"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# jobs[job_id] = {status, progress, message, output_file}
jobs: dict = {}


# ── Rotas ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload():
    session_id = request.form.get("session_id") or str(uuid.uuid4())
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    uploaded = []
    for f in request.files.getlist("photos"):
        if not f or not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext not in ALLOWED_EXT:
            continue
        name = secure_filename(f.filename)
        dest = session_dir / name
        f.save(dest)
        uploaded.append({"name": name, "path": str(dest)})

    return jsonify({"ok": True, "session_id": session_id, "files": uploaded})


@app.route("/api/generate", methods=["POST"])
def generate():
    data       = request.get_json(force=True)
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"ok": False, "error": "session_id ausente"}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "queued", "progress": 0,
        "message": "Na fila...", "output": None
    }

    t = threading.Thread(target=_run_job, args=(job_id, session_id, data), daemon=True)
    t.start()
    return jsonify({"ok": True, "job_id": job_id})


@app.route("/api/progress/<job_id>")
def progress(job_id):
    def stream():
        while True:
            job  = jobs.get(job_id, {"status": "not_found"})
            yield f"data: {json.dumps(job)}\n\n"
            if job.get("status") in ("done", "error", "not_found"):
                break
            time.sleep(0.4)
    return Response(stream(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/download/<job_id>")
def download(job_id):
    f = OUTPUT_DIR / f"{job_id}.mp4"
    if not f.exists():
        return "Arquivo não encontrado", 404
    return send_file(str(f), as_attachment=True, download_name="impar_video.mp4")


@app.route("/api/cleanup/<session_id>", methods=["DELETE"])
def cleanup(session_id):
    d = UPLOAD_DIR / session_id
    if d.exists():
        shutil.rmtree(d)
    return jsonify({"ok": True})


# ── Image Studio ──────────────────────────────────────────────────────────────

@app.route("/api/image/status")
def image_status():
    token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    return jsonify({"ok": True, "ready": bool(token and _HAS_REQUESTS)})


@app.route("/api/image/generate", methods=["POST"])
def image_generate():
    data   = request.get_json(force=True)
    prompt = data.get("prompt", "").strip()
    qty    = max(1, min(4, int(data.get("qty", 1))))

    if not prompt:
        return jsonify({"ok": False, "error": "prompt ausente"}), 400

    token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not token:
        return jsonify({"ok": False, "error": "REPLICATE_API_TOKEN não configurado"}), 503
    if not _HAS_REQUESTS:
        return jsonify({"ok": False, "error": "pip install requests necessário"}), 503

    images = []
    for _ in range(qty):
        img_url = _replicate_generate(prompt, token)
        if img_url:
            images.append({"url": img_url})

    if not images:
        return jsonify({"ok": False, "error": "Nenhuma imagem gerada"}), 500

    return jsonify({"ok": True, "images": images})


def _replicate_generate(prompt: str, token: str) -> str | None:
    """Chama Replicate SDXL e retorna URL da imagem gerada."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "wait",
    }
    payload = {
        "version": "7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
        "input": {
            "prompt": prompt,
            "negative_prompt": "people, person, human, text, watermark, blurry, distorted, ugly",
            "width": 1344,
            "height": 768,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        }
    }
    try:
        r = _requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers, json=payload, timeout=120
        )
        r.raise_for_status()
        result = r.json()

        # Se still processing, poll
        poll_url = result.get("urls", {}).get("get")
        for _ in range(60):
            status = result.get("status")
            if status == "succeeded":
                output = result.get("output", [])
                return output[0] if output else None
            if status in ("failed", "canceled"):
                return None
            if not poll_url:
                break
            time.sleep(2)
            r2 = _requests.get(poll_url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
            r2.raise_for_status()
            result = r2.json()

        output = result.get("output", [])
        return output[0] if isinstance(output, list) and output else None
    except Exception:
        return None


# ── Worker ───────────────────────────────────────────────────────────────────

def _run_job(job_id: str, session_id: str, data: dict):
    def upd(progress: int, message: str, status: str = "running"):
        jobs[job_id].update({"status": status, "progress": progress, "message": message})

    try:
        session_dir  = UPLOAD_DIR / session_id
        output_file  = OUTPUT_DIR / f"{job_id}.mp4"

        upd(5, "Preparando fotos...")

        # Montar lista de movimentos na ordem escolhida pelo usuário
        fotos_ordem = data.get("fotos_ordem", [])  # lista de nomes de arquivo
        movimentos  = ",".join(data.get("movimentos_lista", []))

        # Se o usuário ordenou as fotos, reordená-las em subpasta temporária
        if fotos_ordem:
            ordered_dir = UPLOAD_DIR / f"{session_id}_ord"
            ordered_dir.mkdir(exist_ok=True)
            for i, nome in enumerate(fotos_ordem):
                src = session_dir / nome
                if src.exists():
                    ext = src.suffix
                    dst = ordered_dir / f"{i:03d}{ext}"
                    shutil.copy(src, dst)
            pasta = str(ordered_dir)
        else:
            pasta = str(session_dir)

        upd(15, "Iniciando geração...")

        cmd = [
            sys.executable, str(SCRIPT_PATH),
            "--fotos",     pasta,
            "--movimentos", movimentos,
            "--formato",   data.get("formato",   "landscape"),
            "--resolucao", data.get("resolucao", "fhd"),
            "--titulo",    data.get("titulo",    ""),
            "--subtitulo", data.get("subtitulo", ""),
            "--cta",       data.get("cta",       ""),
            "--saida",     str(output_file),
        ]

        trilha = data.get("trilha_path")
        if trilha and Path(trilha).exists():
            cmd += ["--trilha", trilha]

        upd(20, "Aplicando movimentos cinematográficos...")

        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )

        n_fotos   = len(fotos_ordem) or 1
        foto_atual = 0
        for line in proc.stdout:
            line = line.strip()
            if "🎬" in line or "[" in line:
                foto_atual += 1
                pct = 20 + int(60 * foto_atual / (n_fotos + 1))
                upd(min(pct, 80), line.replace("🎬", "").strip())
            elif "🔧" in line:
                upd(85, "Montando vídeo final...")
            elif "🎵" in line:
                upd(92, "Adicionando trilha sonora...")
            elif "✅" in line:
                upd(99, "Finalizando...")

        proc.wait()

        # Limpeza da pasta ordenada temporária
        if fotos_ordem:
            shutil.rmtree(ordered_dir, ignore_errors=True)

        if proc.returncode == 0 and output_file.exists():
            mb = output_file.stat().st_size / 1024 / 1024
            jobs[job_id].update({
                "status":   "done",
                "progress": 100,
                "message":  f"Vídeo pronto! ({mb:.1f} MB)",
                "output":   job_id,
            })
        else:
            upd(0, "Erro na geração do vídeo.", "error")

    except Exception as e:
        jobs[job_id].update({"status": "error", "progress": 0, "message": str(e)})


# ── Entrada ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"\n🏠  Impar Studio rodando em  http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
