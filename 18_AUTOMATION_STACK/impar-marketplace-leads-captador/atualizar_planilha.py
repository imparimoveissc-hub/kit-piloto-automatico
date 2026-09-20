#!/usr/bin/env python3
"""
atualizar_planilha.py
Adiciona um lead na planilha Google Sheets da Impar (via Drive API, sem nova auth).
Uso: python3 atualizar_planilha.py --nome "Stefany" --telefone "47999358096"
     --link "https://..." --titulo "Casa à venda" --tipo "venda" --origem "marketplace"
"""
import argparse
import configparser
import csv
import io
import json
import subprocess
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_gdrive import (
    LEADS_SHEET_ID, FOLLOWUP_SHEET_ID,
    get_token, export_dicts, append_dict
)

CONFIG_PATH  = Path.home() / ".impar-n8n-core/state/config.json"
LEADS_JSON   = Path.home() / ".impar-n8n-core/state/leads.json"
RCLONE_CONF  = Path.home() / ".config/rclone/rclone.conf"
RCLONE_REMOTE = "gdrive-impar"
SHEET_ID     = LEADS_SHEET_ID


# ── Google Drive / Sheets helpers ─────────────────────────────────────────────

def _get_token() -> str:
    """Pede ao rclone para renovar o token se necessário e o retorna."""
    subprocess.run(
        ["rclone", "about", f"{RCLONE_REMOTE}:", "--json"],
        capture_output=True, timeout=30
    )
    conf = configparser.ConfigParser()
    conf.read(RCLONE_CONF)
    return json.loads(conf[RCLONE_REMOTE]["token"])["access_token"]


def _export_sheet(token: str) -> list[list]:
    """Exporta o Google Sheet como lista de linhas CSV."""
    url = f"https://www.googleapis.com/drive/v3/files/{SHEET_ID}/export?mimeType=text/csv"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    content = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    return list(csv.reader(io.StringIO(content)))


def _upload_sheet(rows: list[list], token: str):
    """Faz upload das linhas de volta ao Google Sheet (converte CSV → Sheets)."""
    out = io.StringIO()
    csv.writer(out).writerows(rows)
    csv_bytes = out.getvalue().encode("utf-8")

    boundary = "impar_gdrive_2026"
    metadata = json.dumps({"mimeType": "application/vnd.google-apps.spreadsheet"}).encode()
    body = (
        b"--" + boundary.encode() + b"\r\n"
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n" +
        metadata + b"\r\n"
        b"--" + boundary.encode() + b"\r\n"
        b"Content-Type: text/csv\r\n\r\n" +
        csv_bytes + b"\r\n"
        b"--" + boundary.encode() + b"--"
    )
    url = f"https://www.googleapis.com/upload/drive/v3/files/{SHEET_ID}?uploadType=multipart"
    req = urllib.request.Request(url, data=body, method="PATCH")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    try:
        urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Erro no upload para o Sheet: {e.code} — {e.read().decode()}")


def append_to_sheet(lead: dict):
    """Adiciona uma linha ao Google Sheet com os dados do lead."""
    token = _get_token()
    rows = _export_sheet(token)
    nova_linha = [
        lead.get("nome", ""),
        lead.get("telefone", ""),
        lead.get("titulo", ""),
        lead.get("link_imovel", ""),
        lead.get("data_captura", ""),
        lead.get("tipo_interesse", ""),
        lead.get("origem", ""),
        lead.get("status", "ativo"),
    ]
    rows.append(nova_linha)
    _upload_sheet(rows, token)
    print(f"✓ Lead adicionado ao Google Sheet ({len(rows)} linhas total)")


# ── JSON local (usado pelo follow-up scheduler) ───────────────────────────────

def load_leads() -> list:
    if LEADS_JSON.exists():
        try:
            return json.loads(LEADS_JSON.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_leads(leads: list):
    LEADS_JSON.parent.mkdir(parents=True, exist_ok=True)
    LEADS_JSON.write_text(json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Utilidades ────────────────────────────────────────────────────────────────

def inferir_tipo(link: str, titulo: str) -> str:
    texto = (link + " " + titulo).lower()
    if any(w in texto for w in ["alug", "locar", "locaç", "alugar", "rent"]):
        return "locacao"
    return "venda"


# ── Registro no leads_followup ───────────────────────────────────────────────

def _registrar_followup(lead: dict):
    """Adiciona o lead na planilha de follow-up se ainda não existir."""
    token = get_token()
    headers, existentes = export_dicts(FOLLOWUP_SHEET_ID, token)
    tel = lead.get("telefone", "")
    # Evita duplicata por telefone
    if any(r.get("telefone", "").strip() == tel for r in existentes):
        print(f"Lead já existe no follow-up: {tel}")
        return

    data_entrada = datetime.now().strftime("%Y-%m-%d")
    data_proximo = (datetime.now() + timedelta(hours=23)).strftime("%Y-%m-%d")

    row = {
        "telefone":              tel,
        "nome":                  lead.get("nome", ""),
        "link_imovel":           lead.get("link_imovel", ""),
        "ref_imovel":            "",
        "descricao_imovel":      lead.get("titulo", ""),
        "canal_entrada":         lead.get("origem", "marketplace"),
        "data_entrada":          data_entrada,
        "ultimo_passo_enviado":  "",
        "data_ultimo_passo":     "",
        "proximo_passo":         "D1",
        "data_proximo_passo":    data_proximo,
        "respondeu_whatsapp":    "nao",
        "opt_out":               "nao",
        "status":                "ativo",
        "observacao":            "",
    }
    append_dict(FOLLOWUP_SHEET_ID, row, token)
    print(f"✓ Lead registrado no follow-up: {lead.get('nome')} (próximo: D1 em {data_proximo})")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nome",     required=True)
    parser.add_argument("--telefone", required=True)
    parser.add_argument("--link",     default="")
    parser.add_argument("--titulo",   default="")
    parser.add_argument("--tipo",     default="")
    parser.add_argument("--origem",   default="marketplace")
    args = parser.parse_args()

    tel = "".join(c for c in args.telefone if c.isdigit())
    if not tel.startswith("55"):
        tel = "55" + tel

    tipo = args.tipo if args.tipo else inferir_tipo(args.link, args.titulo)

    lead = {
        "id":                   str(uuid.uuid4()),
        "nome":                 args.nome,
        "telefone":             tel,
        "titulo":               args.titulo,
        "data_captura":         datetime.now().isoformat(timespec="seconds"),
        "link_imovel":          args.link,
        "tipo_interesse":       tipo,
        "origem":               args.origem,
        "follow_ups_enviados":  [],
        "status":               "ativo",
    }

    # Salva no JSON local (usado pelo follow-up scheduler — não muda)
    leads = load_leads()
    hoje = datetime.now().date().isoformat()
    duplicata = any(
        l.get("telefone") == tel and l.get("data_captura", "").startswith(hoje)
        for l in leads
    )
    if not duplicata:
        leads.append(lead)
        save_leads(leads)
        print(f"Lead salvo no JSON: {args.nome} ({tel})")

        # Escreve no leads_marketplace_captura (registro de captura)
        try:
            append_to_sheet(lead)
        except Exception as e:
            print(f"AVISO: não foi possível gravar no Sheet de captura: {e}", file=sys.stderr)

        # Registra no leads_followup para entrar na cadência automática
        try:
            _registrar_followup(lead)
        except Exception as e:
            print(f"AVISO: não foi possível registrar no Sheet de follow-up: {e}", file=sys.stderr)
    else:
        print(f"Lead já existe hoje: {args.nome} ({tel})")


if __name__ == "__main__":
    main()
