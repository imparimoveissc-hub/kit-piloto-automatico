from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import zipfile
from xml.etree import ElementTree as ET


class ReceiptOcr:
    """Adaptador de OCR/visao para imagens e PDFs de comprovantes."""

    def extract_text(self, file_path: str) -> str:
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self._extract_pdf(path)
        return self._extract_image(path)

    def _extract_image(self, path: Path) -> str:
        try:
            proc = subprocess.run(
                ["tesseract", str(path), "stdout", "-l", "por+eng", "--psm", "6"],
                capture_output=True,
                text=True,
                check=False,
                timeout=180,
            )
        except Exception:
            return ""
        return (proc.stdout or proc.stderr or "").strip()

    def _extract_pdf(self, path: Path) -> str:
        try:
            proc = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
            text = (proc.stdout or "").strip()
            if text:
                return text
        except Exception:
            pass

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                prefix = Path(tmpdir) / "page"
                subprocess.run(
                    ["pdftoppm", "-png", str(path), str(prefix)],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=180,
                )
                pages = sorted(Path(tmpdir).glob("page-*.png"))
                return "\n".join(filter(None, (self._extract_image(page) for page in pages))).strip()
        except Exception:
            return ""
