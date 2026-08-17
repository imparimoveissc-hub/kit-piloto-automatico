#!/usr/bin/env python3
"""
Sender ISOLADO para grupo "FOLLOW UP IMPAR".
Deve ser lançado como processo DETACHED (new session) para que o Claude Code
não recapture foco durante a digitação no WhatsApp.

Uso interno: chamado por testar_grupo_followup.py e pelo SKILL.
Lê /tmp/wa_followup_msg.txt e /tmp/wa_followup_group.txt, envia, escreve
resultado em /tmp/wa_followup_result.txt.
"""
import subprocess
import sys
import time
from pathlib import Path

LCLICK = Path.home() / ".local/impar-automation/leads-planilha/lclick"
MSG_FILE = Path("/tmp/wa_followup_msg.txt")
GROUP_FILE = Path("/tmp/wa_followup_group.txt")
RESULT_FILE = Path("/tmp/wa_followup_result.txt")


def log(msg: str):
    print(msg, flush=True)


def send_to_group(group_name: str, message: str) -> bool:
    # 1. Clipboard via arquivo UTF-8 + AppleScript (preserva emojis/acentos)
    MSG_FILE.write_text(message, encoding="utf-8")
    clip_script = f"""
set f to open for access POSIX file "{MSG_FILE}"
set txt to read f as «class utf8»
close access f
set the clipboard to txt
"""
    r = subprocess.run(["osascript", "-e", clip_script], capture_output=True, text=True, timeout=10)
    if r.returncode != 0:
        log(f"ERRO clipboard: {r.stderr.strip()}")
        return False
    time.sleep(0.3)

    # 2. Cmd+F abre busca global, Cmd+A limpa, digita grupo, espera 3s
    open_script = f"""
tell application "WhatsApp" to activate
delay 1.5
tell application "System Events" to tell process "WhatsApp"
    set frontmost to true
    key code 3 using {{command down}}
    delay 0.8
    keystroke "a" using command down
    delay 0.3
    keystroke "{group_name}"
    delay 3.0
end tell
"""
    subprocess.run(["osascript", "-e", open_script], capture_output=True, text=True, timeout=20)

    # 3. CGEvent click no primeiro resultado (hardcoded: 245, 197)
    if not LCLICK.exists():
        log(f"ERRO: binário lclick não encontrado em {LCLICK}")
        return False
    subprocess.run([str(LCLICK)], capture_output=True, timeout=5)

    # 4. Aguardar carregamento + re-ativar + limpar rascunho + colar + Enter
    time.sleep(4)
    send_script = """
tell application "WhatsApp" to activate
delay 1
tell application "System Events" to tell process "WhatsApp"
    keystroke "a" using command down
    delay 0.3
    key code 51
    delay 0.4
    keystroke "v" using command down
    delay 1.2
    key code 36
end tell
"""
    r = subprocess.run(["osascript", "-e", send_script], capture_output=True, text=True, timeout=20)
    if r.returncode == 0:
        log(f"OK: mensagem enviada para '{group_name}'")
        return True
    else:
        log(f"ERRO envio final: {r.stderr.strip()}")
        return False


def main():
    if not GROUP_FILE.exists() or not MSG_FILE.exists():
        RESULT_FILE.write_text("ERRO: arquivos de entrada não encontrados", encoding="utf-8")
        sys.exit(1)

    group = GROUP_FILE.read_text(encoding="utf-8").strip()
    message = MSG_FILE.read_text(encoding="utf-8").strip()

    log(f"[wa_followup_sender] grupo='{group}' | {len(message)} chars")

    ok = send_to_group(group, message)
    RESULT_FILE.write_text("OK" if ok else "ERRO", encoding="utf-8")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
