#!/usr/bin/env python3
"""Valida o marketplace KPA30 contra o padrão claude-for-legal."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ok, warn, err = [], [], []

def rel(p): return os.path.relpath(p, ROOT)

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def frontmatter(path):
    """Extrai o bloco YAML entre --- e devolve dict simples (name/description/etc)."""
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        return None, txt
    block = m.group(1)
    data, key, buf = {}, None, []
    for line in block.split("\n"):
        if re.match(r"^[a-zA-Z_-]+:", line) and not line.startswith(" "):
            if key: data[key] = " ".join(buf).strip()
            key, _, rest = line.partition(":")
            key = key.strip(); buf = [rest.strip().lstrip("> |").strip()]
        else:
            buf.append(line.strip())
    if key: data[key] = " ".join(buf).strip()
    return data, txt

# 1. JSONs parseáveis
json_files = []
for dp, _, fn in os.walk(ROOT):
    if "/.git" in dp: continue
    for f in fn:
        if f.endswith(".json"):
            json_files.append(os.path.join(dp, f))
for jf in json_files:
    try:
        load_json(jf); ok.append(f"JSON válido: {rel(jf)}")
    except Exception as e:
        err.append(f"JSON inválido {rel(jf)}: {e}")

# 2. marketplace.json coerente
mkt = load_json(os.path.join(ROOT, ".claude-plugin/marketplace.json"))
for p in mkt["plugins"]:
    src = os.path.join(ROOT, p["source"])
    pj = os.path.join(src, ".claude-plugin/plugin.json")
    if not os.path.isdir(src):
        err.append(f"source do marketplace não existe: {p['source']}")
    elif not os.path.isfile(pj):
        err.append(f"plugin.json ausente em {p['source']}")
    else:
        meta = load_json(pj)
        if meta["name"] != p["name"]:
            err.append(f"nome diverge: marketplace={p['name']} plugin.json={meta['name']}")
        else:
            ok.append(f"plugin '{p['name']}' registrado e nomes batem")
        for req in ("version", "description", "author"):
            if req not in meta:
                err.append(f"plugin.json {p['name']} sem campo '{req}'")

# 3. Skills: frontmatter + name == diretório
plugin_dir = os.path.join(ROOT, "imobiliario-juridico")
skills_dir = os.path.join(plugin_dir, "skills")
for sk in sorted(os.listdir(skills_dir)):
    sp = os.path.join(skills_dir, sk, "SKILL.md")
    if not os.path.isfile(sp):
        err.append(f"skill '{sk}' sem SKILL.md"); continue
    fm, _ = frontmatter(sp)
    if fm is None:
        err.append(f"skill '{sk}' sem frontmatter YAML"); continue
    if fm.get("name") != sk:
        err.append(f"skill '{sk}': name do frontmatter = '{fm.get('name')}' (deveria ser '{sk}')")
    for req in ("name", "description", "argument-hint"):
        if not fm.get(req):
            err.append(f"skill '{sk}' sem campo '{req}'")
    if fm.get("name") == sk and fm.get("description") and fm.get("argument-hint"):
        ok.append(f"skill '{sk}': frontmatter completo")

# 4. Agentes: frontmatter com name/description/model/tools
agents_dir = os.path.join(plugin_dir, "agents")
for ag in sorted(os.listdir(agents_dir)):
    ap = os.path.join(agents_dir, ag)
    fm, _ = frontmatter(ap)
    if fm is None:
        err.append(f"agente '{ag}' sem frontmatter"); continue
    for req in ("name", "description", "model", "tools"):
        if not fm.get(req):
            err.append(f"agente '{ag}' sem campo '{req}'")
    if all(fm.get(r) for r in ("name", "description", "model", "tools")):
        ok.append(f"agente '{ag}': frontmatter completo")

# 5. Consistência do caminho de config em todos os .md
CONFIG = "~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md"
refs = 0
for dp, _, fn in os.walk(plugin_dir):
    for f in fn:
        if f.endswith(".md"):
            with open(os.path.join(dp, f), encoding="utf-8") as fh:
                if CONFIG in fh.read(): refs += 1
if refs >= 4:
    ok.append(f"caminho de config referenciado consistentemente em {refs} arquivos")
else:
    warn.append(f"caminho de config aparece em só {refs} arquivos (esperado ≥4)")

# 6. Paridade estrutural com o padrão de referência
for needed in [".claude-plugin/plugin.json", ".mcp.json", "hooks/hooks.json",
               "CLAUDE.md", "README.md"]:
    p = os.path.join(plugin_dir, needed)
    (ok if os.path.isfile(p) else err).append(
        f"{'ok' if os.path.isfile(p) else 'FALTA'} arquivo-padrão: {needed}")

# Relatório
print("=" * 60)
print(f"  VALIDAÇÃO — {len(ok)} ok · {len(warn)} avisos · {len(err)} erros")
print("=" * 60)
for m in ok:   print(f"  ✅ {m}")
for m in warn: print(f"  ⚠️  {m}")
for m in err:  print(f"  🔴 {m}")
print("=" * 60)
sys.exit(1 if err else 0)
