from __future__ import annotations

import subprocess
from pathlib import Path


class AudioTranscriber:
    """Adaptador de transcricao para mensagens de audio."""

    def transcribe(self, file_path: str) -> str:
        path = Path(file_path)
        try:
            import whisper  # type: ignore
        except Exception:
            return ""

        for model_name in ("base", "small", "medium"):
            try:
                model = whisper.load_model(model_name)
                result = model.transcribe(str(path), language="pt")
                return str(result.get("text", "")).strip()
            except Exception:
                continue

        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=False, timeout=10)
        except Exception:
            pass
        return ""
