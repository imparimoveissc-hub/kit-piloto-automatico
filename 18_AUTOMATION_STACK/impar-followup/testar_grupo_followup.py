#!/usr/bin/env python3
"""
Teste real: envia notificação para grupo "FOLLOW UP IMPAR" via processo DETACHED.

O sender roda em nova sessão (os.setsid) para que o Claude Code não recapture
foco durante a digitação no WhatsApp.

Uso:
    python3 testar_grupo_followup.py
    python3 testar_grupo_followup.py --lead Adriana
"""
import argparse
import os
import subprocess
import time
import urllib.parse
from pathlib import Path

SENDER = Path(__file__).parent / "wa_followup_sender.py"
GROUP_FILE = Path("/tmp/wa_followup_group.txt")
MSG_FILE = Path("/tmp/wa_followup_msg.txt")
RESULT_FILE = Path("/tmp/wa_followup_result.txt")
LOG_FILE = Path("/tmp/wa_followup_sender.log")
GRUPO = "FOLLOW UP IMPAR"

LEADS_TESTE = {
    "Gustavo": {
        "nome": "Gustavo Meneses",
        "telefone": "5594992929919",
        "imovel": "Marketplace FB",
        "passo": "D7",
        "data_passo": "2026-08-14",
        "link": "https://www.facebook.com/messages/t/122235963230246003",
        "msg_lead": "Gustavo, só queria checar: tem algum horário que faria sentido dar uma olhada rápida, sem compromisso? Posso facilitar tudo por aqui.",
    },
    "Adriana": {
        "nome": "Adriana",
        "telefone": "554784513193",
        "imovel": "Apto Aventureiro 110m2 - venda R$480.000",
        "passo": "D30",
        "data_passo": "2026-08-12",
        "link": "https://www.chavesnamao.com.br/imovel/a-venda-com-garagem-sc-joinville-aventureiro-110m2-RS480000/id-41261690/",
        "msg_lead": "Adriana, vou pausar meus contatos por aqui pra não ficar pesando na sua caixa. Mas posso deixar um alerta ativo e só te chamar se aparecer algo realmente bom no perfil que você buscou — sem spam, só quando valer a pena. Quer que eu faça isso?",
    },
}


def build_notification(lead: dict) -> str:
    wa_url = f"https://wa.me/{lead['telefone']}?text={urllib.parse.quote(lead['msg_lead'])}"
    notif = (
        f"🔁 FOLLOW-UP DEVIDO — {lead['passo']}\n"
        f"👤 Nome: {lead['nome']}\n"
        f"📞 Telefone: {lead['telefone']}\n"
        f"🏠 Imóvel: {lead['imovel']}\n"
        f"📅 Passo devido em: {lead['data_passo']}\n"
    )
    if lead.get("link"):
        notif += f"🔗 Anúncio: {lead['link']}\n"
    notif += f"\n👉 Toque para enviar a mensagem pronta:\n{wa_url}"
    return notif


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lead", default="Gustavo", choices=list(LEADS_TESTE.keys()))
    args = parser.parse_args()

    lead = LEADS_TESTE[args.lead]
    notif = build_notification(lead)

    print(f"\n📋 Notificação para '{GRUPO}':")
    print("─" * 60)
    print(notif)
    print("─" * 60)

    # Escrever inputs para o sender
    GROUP_FILE.write_text(GRUPO, encoding="utf-8")
    MSG_FILE.write_text(notif, encoding="utf-8")
    RESULT_FILE.unlink(missing_ok=True)

    print(f"\n🚀 Lançando sender DETACHED (nova sessão, sem herança de foco)...")
    print("   O WhatsApp vai abrir em ~3s. Não clique em nada até terminar (~15s).\n")

    # Lançar completamente detached: nova sessão + fds fechados
    proc = subprocess.Popen(
        ["python3", str(SENDER)],
        start_new_session=True,
        stdout=open(LOG_FILE, "w"),
        stderr=subprocess.STDOUT,
        close_fds=True,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

    # Aguardar até 20s pelo resultado
    for i in range(20):
        time.sleep(1)
        print(f"  aguardando... {i+1}s", end="\r")
        if RESULT_FILE.exists():
            result = RESULT_FILE.read_text(encoding="utf-8").strip()
            print(f"\n\n{'✅' if result == 'OK' else '❌'} Resultado: {result}")
            if LOG_FILE.exists():
                print("\n📄 Log do sender:")
                print(LOG_FILE.read_text(encoding="utf-8"))
            return

    print("\n⚠️  Timeout (20s) — verifique:", LOG_FILE)
    if LOG_FILE.exists():
        print(LOG_FILE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
