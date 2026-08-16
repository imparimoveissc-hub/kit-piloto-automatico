#!/usr/bin/env python3
"""IMPAR OS — descoberta automática de automações e scripts."""

import os
import json
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = OS_DIR.parent
DB_PATH = OS_DIR / "database" / "impar.db"
REGISTRY_PATH = OS_DIR / "registry" / "registry.json"

AUTOMATION_BASE = PROJECT_ROOT / "18_AUTOMATION_STACK"
N8N_CORE = Path.home() / ".impar-n8n-core"

BLOCKED = {"start-bridge.sh", "install-launchd-macos.sh"}
APPROVAL_KEYWORDS = {"publish", "send", "post", "delete", "remove", "email", "whatsapp", "notif"}
WRITE_KEYWORDS = {"write", "update", "create", "insert", "push"}

def classify(path: Path) -> tuple[str, str]:
    name = path.name.lower()
    stem = path.stem.lower()
    if name in BLOCKED:
        return "BLOCKED", "high"
    if any(k in stem for k in APPROVAL_KEYWORDS):
        return "REQUIRES_APPROVAL", "medium"
    if any(k in stem for k in WRITE_KEYWORDS):
        return "REQUIRES_APPROVAL", "medium"
    return "READ_ONLY_AUTO", "low"

def make_id(path: Path) -> str:
    rel = path.relative_to(PROJECT_ROOT) if PROJECT_ROOT in path.parents else path
    parts = str(rel).replace("/", ".").replace(" ", "_").replace(".py", "").replace(".sh", "")
    return parts[:80]

def discover_scripts() -> list[dict]:
    items = []
    for dirpath in [AUTOMATION_BASE, N8N_CORE / "scripts"]:
        if not dirpath.exists():
            continue
        for ext in ["*.py", "*.sh"]:
            for p in dirpath.rglob(ext):
                if ".git" in p.parts or "__pycache__" in p.parts:
                    continue
                mode_cat, risk = classify(p)
                items.append({
                    "id": make_id(p),
                    "type": "script",
                    "ext": p.suffix,
                    "path": str(p),
                    "name": p.name,
                    "category": p.parent.name,
                    "mode": "blocked" if mode_cat == "BLOCKED" else ("read-only" if mode_cat == "READ_ONLY_AUTO" else "approval-required"),
                    "classification": mode_cat,
                    "risk": risk,
                    "ai_required": False,
                    "timeout": 60,
                    "enabled": mode_cat != "BLOCKED",
                    "discovered_at": datetime.now(timezone.utc).isoformat(),
                })
    return items

def discover_workflows() -> list[dict]:
    items = []
    wf_dir = N8N_CORE / "workflows"
    if wf_dir.exists():
        for p in wf_dir.glob("*.json"):
            try:
                data = json.loads(p.read_text())
                items.append({
                    "id": f"n8n.{p.stem}",
                    "type": "workflow",
                    "ext": ".json",
                    "path": str(p),
                    "name": data.get("name", p.stem),
                    "category": "n8n",
                    "mode": "orchestrated",
                    "classification": "READ_ONLY_AUTO",
                    "risk": "low",
                    "ai_required": False,
                    "timeout": 120,
                    "enabled": True,
                    "discovered_at": datetime.now(timezone.utc).isoformat(),
                })
            except Exception:
                pass
    # Also scan IMPAR_OS/workflows
    for p in (OS_DIR / "workflows").glob("*.json"):
        try:
            data = json.loads(p.read_text())
            items.append({
                "id": f"impar_os.{p.stem}",
                "type": "workflow",
                "ext": ".json",
                "path": str(p),
                "name": data.get("name", p.stem),
                "category": "impar_os",
                "mode": "orchestrated",
                "classification": "READ_ONLY_AUTO",
                "risk": "low",
                "ai_required": False,
                "timeout": 120,
                "enabled": True,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            })
        except Exception:
            pass
    return items

def discover_configs() -> list[dict]:
    items = []
    for p in AUTOMATION_BASE.rglob("*.json"):
        if ".git" in p.parts or "__pycache__" in p.parts:
            continue
        items.append({
            "id": make_id(p),
            "type": "config",
            "ext": ".json",
            "path": str(p),
            "name": p.name,
            "category": p.parent.name,
            "mode": "read-only",
            "classification": "READ_ONLY_AUTO",
            "risk": "low",
            "ai_required": False,
            "timeout": 5,
            "enabled": True,
            "discovered_at": datetime.now(timezone.utc).isoformat(),
        })
    return items

def main():
    all_items = []
    all_items.extend(discover_scripts())
    all_items.extend(discover_workflows())
    all_items.extend(discover_configs())

    registry = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(all_items),
        "blocked": sum(1 for i in all_items if i["classification"] == "BLOCKED"),
        "requires_approval": sum(1 for i in all_items if i["classification"] == "REQUIRES_APPROVAL"),
        "read_only_auto": sum(1 for i in all_items if i["classification"] == "READ_ONLY_AUTO"),
        "items": all_items,
    }

    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False))
    print(f"OK: {len(all_items)} itens descobertos → {REGISTRY_PATH}")
    print(f"  BLOCKED: {registry['blocked']}")
    print(f"  REQUIRES_APPROVAL: {registry['requires_approval']}")
    print(f"  READ_ONLY_AUTO: {registry['read_only_auto']}")

    # Sync to SQLite
    if DB_PATH.exists():
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        ts = datetime.now(timezone.utc).isoformat()
        for item in all_items:
            cur.execute("""INSERT OR REPLACE INTO automations
                (id, name, type, path, mode, risk, ai_required, enabled, last_checked, status)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (item["id"], item["name"], item["type"], item["path"],
                 item["mode"], item["risk"], 0 if not item["ai_required"] else 1,
                 1 if item["enabled"] else 0, ts, "discovered"))
        conn.commit()
        conn.close()
        print(f"OK: {len(all_items)} entradas gravadas no banco")

if __name__ == "__main__":
    main()
