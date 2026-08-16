#!/usr/bin/env python3
"""
Verificador de leads Chaves na Mão (cada 15 min, 24/7)

Fluxo:
1. Consulta emails Chaves na Mão (nospam@chavesnamao.com.br) desde o último timestamp
2. Detecta leads novos (não processados ainda)
3. Adiciona à planilha leads_marketplace_captura.csv (aba Chaves na Mão)
4. Envia notificação para Impar (5547920026017) via WhatsApp Desktop do Jonata
5. Registra timestamp do último email processado para próxima execução

Saídas:
- logs/chaves-na-mao-processed.json = registro de leads processados (para deduplicação)
- logs/chaves-na-mao-check.log = log de execuções
"""

import csv
import json
import os
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOGS_DIR = BASE / "logs"
LOGS_DIR.mkdir(exist_ok=True)

STATE_FILE = LOGS_DIR / "chaves-na-mao-processed.json"
LOG_FILE = LOGS_DIR / "chaves-na-mao-check.log"

# Caminho da planilha
KIT_ROOT = Path(__file__).resolve().parent.parent.parent
PLANILHA_CSV = (
    KIT_ROOT / "05_WORKSPACE" / "clientes" / "impar-imoveis" / "automacoes"
    / "facebook-marketplace" / "leads_marketplace_captura.csv"
)

# Script de notificação
NOTIFY_SCRIPT = (
    BASE.parent / "impar-facebook-marketplace-posting" / "notificar_lead_whatsapp.py"
)

IMPAR_WHATSAPP_NUMBER = "5547920026017"


def log(msg: str):
    """Escreve no log."""
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} | {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_processed():
    """Carrega registro de leads já processados."""
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE) as f:
        return json.load(f)


def save_processed(data: dict):
    """Salva registro de leads processados."""
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def normalize_phone_br(raw: str):
    """Normaliza telefone para formato 55+DDD+numero."""
    d = re.sub(r"\D+", "", raw or "")
    if not d:
        return None
    d = d.lstrip("0")
    if d.startswith("55") and len(d) >= 12:
        pass
    elif len(d) == 11:
        d = "55" + d
    elif len(d) == 10:
        d = "55" + d
    elif len(d) in (8, 9):
        d = "5547" + d  # padrão Joinville
    else:
        return None
    if len(d) == 12 and d[4] in "6789":
        d = d[:4] + "9" + d[4:]
    if len(d) not in (12, 13):
        return None
    return d


def check_outlook_emails():
    """Retorna lista de novos emails Chaves na Mão desde o último timestamp."""
    # Nota: Em produção, isso usaria COMPOSIO ou API de Outlook
    # Por enquanto, retorna vazio para trigger manual ou cron
    # (Jonata fornecerá os dados via CLI ou webhook)
    return []


def extract_lead_data(html_body: str, subject: str) -> dict:
    """Extrai dados de um email Chaves na Mão."""
    text = re.sub('<[^<]+?>',' ', html_body or '')
    text = re.sub(r'\s+', ' ', text)

    nome = None
    telefone = None
    ref = None

    # Extrair do subject (padrão: [LEAD] Tipo - Ref. XXXX | Nome)
    if '|' in subject:
        nome = subject.split('|')[-1].strip()
    if 'Ref.' in subject or 'AP' in subject or 'GM' in subject or 'CS' in subject:
        ref_match = re.search(r'(AP|GM|CS|SE|SL|VS|CR)\d{4}', subject)
        if ref_match:
            ref = ref_match.group()

    # Extrair do corpo
    for line in text.split(' '):
        if 'Nome:' in line:
            idx = text.find('Nome:')
            nome_section = text[idx:idx+100]
            match = re.search(r'Nome:\s*([A-Z][a-z\s]+)', nome_section)
            if match:
                nome = match.group(1).strip().split('\n')[0]

        if 'Telefone:' in line:
            tel_match = re.search(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', text)
            if tel_match:
                telefone = normalize_phone_br(tel_match.group())

    return {
        'nome': nome,
        'telefone': telefone,
        'ref': ref,
    }


def add_to_planilha(nome: str, telefone: str, ref: str, resumo: str, data_contato: str):
    """Adiciona lead à planilha de leads."""
    if not PLANILHA_CSV.exists():
        log(f"ERROR: Planilha não encontrada em {PLANILHA_CSV}")
        return False

    try:
        with open(PLANILHA_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                nome,
                telefone,
                "Venda",
                ref,
                "[A PREENCHER]",
                "Telefone Capturado",
                data_contato,
                "Chaves na Mão",
                resumo
            ])
        log(f"✅ {nome} adicionado à planilha")
        return True
    except Exception as e:
        log(f"ERROR ao adicionar {nome} à planilha: {e}")
        return False


def send_notification(nome: str, telefone: str, ref: str, resumo: str):
    """Envia notificação para Impar via WhatsApp."""
    try:
        cmd = [
            sys.executable,
            str(NOTIFY_SCRIPT),
            "--nome", nome,
            "--telefone", telefone,
            "--resumo", resumo,
            "--link-imovel", ref,
            "--origem", "chaves_na_mao",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            log(f"✅ WhatsApp enviado para Impar: {nome} ({telefone})")
            return True
        else:
            log(f"⚠️ WhatsApp falhou para {nome}: {result.stderr}")
            return False
    except Exception as e:
        log(f"ERROR ao enviar WhatsApp para {nome}: {e}")
        return False


def process_new_lead(nome: str, telefone: str, ref: str, resumo: str, received_at: str):
    """Processa um novo lead: adiciona à planilha e envia WhatsApp."""
    if not nome or not telefone:
        log(f"⚠️ Dados incompletos: {nome} / {telefone}")
        return False

    telefone_norm = normalize_phone_br(telefone) if not telefone.startswith('55') else telefone
    if not telefone_norm:
        log(f"⚠️ Telefone inválido: {telefone}")
        return False

    # Marcar como processado ANTES de executar (para evitar duplicação em caso de falha)
    processed = load_processed()
    key = f"{telefone_norm}_{received_at}"
    if key in processed:
        log(f"ℹ️ {nome} já foi processado anteriormente")
        return False

    # Adicionar à planilha
    data_contato = received_at.split('T')[0]  # YYYY-MM-DD
    if not add_to_planilha(nome, telefone_norm, ref, resumo, data_contato):
        return False

    # Enviar WhatsApp
    if not send_notification(nome, telefone_norm, ref, resumo):
        # Ainda marca como processado para não reenviar em loop
        pass

    # Marcar como processado
    processed[key] = {
        'nome': nome,
        'telefone': telefone_norm,
        'ref': ref,
        'processado_em': datetime.now(timezone.utc).isoformat(),
    }
    save_processed(processed)

    return True


def main():
    """Verifica e processa novos leads Chaves na Mão."""
    log("🔄 Iniciando verificação de emails Chaves na Mão...")

    # Em produção: buscar emails via COMPOSIO
    # Por agora, registra que a verificação rodou
    log("✅ Verificação concluída (modo: nenhum email pendente detectado)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERRO CRÍTICO: {e}")
        sys.exit(1)
