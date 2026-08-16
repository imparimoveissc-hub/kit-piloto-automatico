#!/usr/bin/env python3
"""
inject-kos-header.py — injeta cabeçalho KOS no topo do prompt de cada task/skill
Roda uma vez; idempotente (não duplica o header se já existir).

Uso: python3 00_OS/kos/inject-kos-header.py
"""

from pathlib import Path
import sys

KIT_DIR = Path(__file__).parent.parent.parent.resolve()
TASKS_DIR = Path.home() / ".claude/scheduled-tasks"
SKILLS_DIR = Path.home() / ".claude/skills"

# Mapeamento task/skill → Brain module
MODULE_MAP = {
    # tasks
    "impar-gerente-digital":          "Sistema",
    "impar-manutencao-horaria":       "Sistema",
    "impar-reativador-marketplace":   "Marketplace",
    "impar-relatorio-marketplace-manha": "Marketplace",
    "impar-leads-chaves-na-mao":      "Leads",
    "leads-chaves-na-mao-whatsapp":   "Leads",
    "impar-messenger-inbox":          "Leads",
    "impar-atende-leads-dia":         "Leads",
    "impar-followup-manha":           "Leads",
    "impar-followup-checagem-0845":   "Leads",
    "impar-notificar-leads-planilha": "Leads",
    "emissao-nfs-dia-20":             "NFS-e",
    "emissao-nfs-dia-25":             "NFS-e",
    "emissao-nfs-dia-29":             "NFS-e",
    "emissao-nfs-dia-30":             "NFS-e",
    "emissao-notas-fiscais":          "NFS-e",
    "vigia-reajustes-semanal":        "Contratos",
    # skills
    "emitir-notas-fiscais":           "NFS-e",
    "emitir-nota-avulsa":             "NFS-e",
    "retirar-notas-fiscais":          "NFS-e",
    "backup-claude":                  "Sistema",
    "social-content-operator":        "geral",
    "video-use":                      "geral",
}

SKIP_DISABLED = {"impar-manutencao-horaria", "impar-notificar-leads-planilha", "status-tudo-certo-whatsapp"}

HEADER_MARKER = "⚡ [KOS]"

def make_header(module: str, task_id: str) -> str:
    brain_path = f"00_OS/kos/brain/{module}.md"
    return (
        f"{HEADER_MARKER} LEIA PRIMEIRO — antes de abrir qualquer arquivo:\n"
        f"Brain: {brain_path}\n"
        f"Regra: se o Brain responder → pare no Brain. Só acesse arquivos se estritamente necessário.\n"
        f"Index: 00_OS/kos/index.json (jq '.functions[\"nome\"]' para localizar qualquer função)\n"
        f"──────────────────────────────────────────────────────────\n\n"
    )

def inject(skill_file: Path, task_id: str, module: str, dry_run: bool = False) -> str:
    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return f"ERRO ao ler: {e}"

    # Idempotência: não injeta se já tem o header
    if HEADER_MARKER in content:
        return "já tem header — pulado"

    # Localizar fim do frontmatter YAML (segundo ---)
    lines = content.split("\n")
    fm_end = -1
    dashes = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            dashes += 1
            if dashes == 2:
                fm_end = i
                break

    if fm_end == -1:
        # Sem frontmatter — injeta no topo
        new_content = make_header(module, task_id) + content
    else:
        # Injeta logo após o segundo ---
        before = "\n".join(lines[:fm_end + 1])
        after = "\n".join(lines[fm_end + 1:])
        # Garante linha em branco entre frontmatter e header
        after_stripped = after.lstrip("\n")
        new_content = before + "\n\n" + make_header(module, task_id) + after_stripped

    if not dry_run:
        skill_file.write_text(new_content, encoding="utf-8")

    return "injetado ✅"


def main(dry_run: bool = False):
    mode = "DRY RUN" if dry_run else "ESCREVENDO"
    print(f"=== inject-kos-header.py [{mode}] ===\n")

    results = []

    # 1. Scheduled tasks
    if TASKS_DIR.exists():
        for task_dir in sorted(TASKS_DIR.iterdir()):
            if not task_dir.is_dir():
                continue
            task_id = task_dir.name
            skill_file = task_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            if task_id in SKIP_DISABLED:
                results.append((task_id, "desativada — pulada"))
                continue
            module = MODULE_MAP.get(task_id, "geral")
            status = inject(skill_file, task_id, module, dry_run)
            results.append((task_id, f"[{module}] {status}"))

    # 2. Skills
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_id = skill_dir.name
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            module = MODULE_MAP.get(skill_id, "geral")
            status = inject(skill_file, skill_id, module, dry_run)
            results.append((f"skill:{skill_id}", f"[{module}] {status}"))

    # Relatório
    injected = sum(1 for _, s in results if "injetado" in s)
    skipped  = sum(1 for _, s in results if "pulado" in s or "desativ" in s)

    for name, status in results:
        icon = "✅" if "injetado" in status else "⏭ "
        print(f"  {icon} {name:45s} {status}")

    print(f"\nTotal: {injected} injetados | {skipped} pulados | {len(results)} analisados")

    if injected > 0 and not dry_run:
        print("\n🔄 Regenerando index.json ...")
        import subprocess
        subprocess.run(
            ["python3", str(KIT_DIR / "00_OS/kos/build-index.py")],
            check=False
        )


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    main(dry_run=dry)
