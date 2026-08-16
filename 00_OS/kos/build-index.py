#!/usr/bin/env python3
"""
build-index.py — KOS Fase 2: gera index.json a partir do codebase
Escaneia Python (AST), Markdown (headings) e scheduled tasks (SKILL.md)
Saída: 00_OS/kos/index.json

Uso: python3 00_OS/kos/build-index.py
"""
import ast
import json
import os
import re
from pathlib import Path
from datetime import datetime

# Kit root: sobe dois níveis a partir de 00_OS/kos/
KIT_DIR = Path(__file__).parent.parent.parent.resolve()


# ── Inferência de módulo ───────────────────────────────────────────────────────

def infer_module_from_path(path: str) -> str:
    p = path.lower()
    if any(k in p for k in ["marketplace", "facebook", "grupo"]):
        return "marketplace"
    if any(k in p for k in ["chaves-na-mao", "chaves_na_mao", "leads_watcher", "leads-planilha", "followup"]):
        return "leads"
    if any(k in p for k in ["gerente", "sistema", "manutencao"]):
        return "sistema"
    if any(k in p for k in ["nfse", "nfem", "nota_fiscal", "nota-fiscal"]):
        return "nfse"
    if any(k in p for k in ["contrato", "imobiliario", "juridico", "reajuste"]):
        return "contratos"
    return "geral"


def infer_module_from_task(task_id: str) -> str:
    t = task_id.lower()
    if "marketplace" in t:
        return "marketplace"
    if any(k in t for k in ["leads", "chaves", "planilha", "followup"]):
        return "leads"
    if any(k in t for k in ["gerente", "manutencao", "sistema"]):
        return "sistema"
    if any(k in t for k in ["nota", "nfs", "fiscal"]):
        return "nfse"
    if "contrato" in t or "reajuste" in t:
        return "contratos"
    return "geral"


# ── Scanner Python (AST) ───────────────────────────────────────────────────────

def scan_python_functions(base_dirs: list) -> dict:
    """
    Extrai definições de função de arquivos Python via AST.
    Retorna: { "nome_funcao": [ { file, line, module }, ... ] }
    """
    functions: dict = {}

    for base in base_dirs:
        base = Path(base).expanduser()
        if not base.exists():
            continue

        for py_file in base.rglob("*.py"):
            # Ignorar diretórios de cache e ambientes virtuais
            if any(p in str(py_file) for p in [".venv", "venv", "__pycache__", "site-packages"]):
                continue
            try:
                source = py_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(source, filename=str(py_file))
            except SyntaxError:
                continue
            except Exception:
                continue

            module_guess = infer_module_from_path(str(py_file))

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = node.name
                    entry = {
                        "file": str(py_file),
                        "line": node.lineno,
                        "module": module_guess
                    }
                    functions.setdefault(name, []).append(entry)

    return functions


# ── Scanner Markdown (headings + conceitos-chave) ─────────────────────────────

CONCEPT_PATTERNS = [
    r"`([a-zA-Z0-9_\-\.]+\.(?:json|csv|py|sh|plist|yaml|md))`",   # arquivos mencionados em backticks
    r"\*\*([a-zA-Z0-9_\-\.]+\.(?:json|csv|py|sh|plist|yaml))\*\*", # arquivos em negrito
]

def scan_markdown(md_files: list) -> dict:
    """
    Extrai headings e referências a arquivos/conceitos de arquivos Markdown.
    Retorna: { "conceito": [ { path, context, module }, ... ] }
    """
    concepts: dict = {}

    for md_file in md_files:
        md_file = Path(md_file).expanduser()
        if not md_file.exists():
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        module_guess = infer_module_from_path(str(md_file))

        # Headings H1–H3
        for match in re.finditer(r'^#{1,3}\s+(.+)$', text, re.MULTILINE):
            heading = match.group(1).strip()
            concepts.setdefault(heading, []).append({
                "path": str(md_file),
                "context": "heading",
                "module": module_guess
            })

        # Referências a arquivos específicos (ex: checkpoint.json, queue.json)
        for pattern in CONCEPT_PATTERNS:
            for match in re.finditer(pattern, text):
                concept = match.group(1)
                concepts.setdefault(concept, []).append({
                    "path": str(md_file),
                    "context": "file-reference",
                    "module": module_guess
                })

    return concepts


# ── Scanner de scheduled tasks ────────────────────────────────────────────────

CRON_RE = re.compile(r'cronExpression:\s*"?([^"\n]+)"?')
ENABLED_RE = re.compile(r'enabled:\s*(true|false)')
DESC_RE = re.compile(r'description:\s*(.+)')

def scan_scheduled_tasks() -> dict:
    """
    Lê ~/.claude/scheduled-tasks/*/SKILL.md e extrai metadados de cada task.
    Retorna: { "task-id": { cron, skill, module, enabled, description } }
    """
    tasks: dict = {}
    tasks_dir = Path.home() / ".claude/scheduled-tasks"

    if not tasks_dir.exists():
        return tasks

    for skill_file in sorted(tasks_dir.glob("*/SKILL.md")):
        task_id = skill_file.parent.name
        try:
            text = skill_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        cron_m = CRON_RE.search(text)
        enabled_m = ENABLED_RE.search(text)
        desc_m = DESC_RE.search(text)

        tasks[task_id] = {
            "cron": cron_m.group(1).strip() if cron_m else None,
            "skill": str(skill_file),
            "module": infer_module_from_task(task_id),
            "enabled": (enabled_m.group(1) == "true") if enabled_m else True,
            "description": desc_m.group(1).strip() if desc_m else None
        }

    return tasks


# ── Scanner de LaunchAgents ────────────────────────────────────────────────────

SCHEDULE_RE = re.compile(r'<key>(StartInterval|Hour|Minute)</key>\s*<(?:integer|string)>([^<]+)</(?:integer|string)>', re.DOTALL)
LABEL_RE = re.compile(r'<key>Label</key>\s*<string>([^<]+)</string>')

def scan_launchagents() -> dict:
    """
    Lê ~/Library/LaunchAgents/com.impar.*.plist e extrai metadados.
    Retorna: { "label": { plist, schedule_hint, module } }
    """
    agents: dict = {}
    la_dir = Path.home() / "Library/LaunchAgents"

    if not la_dir.exists():
        return agents

    for plist in sorted(la_dir.glob("com.impar.*.plist")):
        try:
            text = plist.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        label_m = LABEL_RE.search(text)
        label = label_m.group(1) if label_m else plist.stem

        schedule_parts = SCHEDULE_RE.findall(text)
        schedule_hint = ", ".join(f"{k}={v}" for k, v in schedule_parts) if schedule_parts else "ver plist"

        agents[label] = {
            "plist": str(plist),
            "schedule_hint": schedule_hint,
            "module": infer_module_from_path(label)
        }

    return agents


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("KOS build-index.py — Fase 2")
    print(f"Kit: {KIT_DIR}")
    print("=" * 55)

    # Diretórios Python a escanear
    py_dirs = [
        KIT_DIR / "18_AUTOMATION_STACK",
        Path.home() / ".local/impar-automation",
    ]

    # Arquivos Markdown chave
    brain_dir = KIT_DIR / "00_OS/kos/brain"
    md_files = list(brain_dir.glob("*.md")) + [
        KIT_DIR / "18_AUTOMATION_STACK/impar-facebook-marketplace-posting/MECANICO-IMPAR-PROCEDIMENTOS.md",
        KIT_DIR / "00_OS/kos/token-policy.md",
        KIT_DIR / "00_OS/kos/registry.yaml",
    ]

    print("\n[1/4] Escaneando Python (AST)...")
    functions = scan_python_functions(py_dirs)
    print(f"      {len(functions)} funções únicas encontradas")

    print("[2/4] Escaneando Markdown (headings + referências)...")
    concepts = scan_markdown(md_files)
    print(f"      {len(concepts)} conceitos/headings encontrados")

    print("[3/4] Escaneando scheduled tasks...")
    tasks = scan_scheduled_tasks()
    print(f"      {len(tasks)} tasks encontradas")

    print("[4/4] Escaneando LaunchAgents...")
    launchagents = scan_launchagents()
    print(f"      {len(launchagents)} LaunchAgents encontrados")

    index = {
        "generated_at": datetime.now().isoformat(),
        "kit_dir": str(KIT_DIR),
        "stats": {
            "functions": len(functions),
            "concepts": len(concepts),
            "tasks": len(tasks),
            "launchagents": len(launchagents)
        },
        "functions": functions,
        "concepts": concepts,
        "tasks": tasks,
        "launchagents": launchagents
    }

    out_path = KIT_DIR / "00_OS/kos/index.json"
    out_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    size_kb = out_path.stat().st_size / 1024
    print(f"\n✅ index.json gerado: {out_path}")
    print(f"   Tamanho: {size_kb:.1f} KB")
    print(f"   {len(functions)} funções | {len(concepts)} conceitos | {len(tasks)} tasks | {len(launchagents)} LaunchAgents")
    print("\nPróximos passos:")
    print("  - Consultar index.json antes de grep/find")
    print("  - Rodar novamente após qualquer mudança estrutural")
    print("  - Adicionado ao kos-install.sh como passo [5/5]")


if __name__ == "__main__":
    main()
