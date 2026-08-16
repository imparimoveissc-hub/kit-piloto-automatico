from __future__ import annotations

from pathlib import Path


class DuplicateGuard:
    """Controle simples de fingerprints para evitar lancamento duplicado."""

    def __init__(self, store_path: str | Path = "data/fingerprints.jsonl") -> None:
        self.store_path = Path(store_path)

    def seen(self, fingerprint: str) -> bool:
        if not self.store_path.exists():
            return False
        try:
            return fingerprint in {
                line.strip()
                for line in self.store_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            }
        except OSError:
            return False

    def remember(self, fingerprint: str) -> None:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        with self.store_path.open("a", encoding="utf-8") as handle:
            handle.write(fingerprint + "\n")
