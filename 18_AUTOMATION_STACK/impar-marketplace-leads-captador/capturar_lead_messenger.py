#!/usr/bin/env python3
"""
capturar_lead_messenger.py
Lê conversas não respondidas do Facebook Marketplace Messenger via Playwright,
extrai nome + telefone, salva lead e aciona notificação WhatsApp.

Dependências: pip install playwright && playwright install chromium
Roda via LaunchAgent a cada 5 minutos.
"""
import json
import re
import subprocess
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

NOMES_BLOQUEADOS = {
    "facebook marketplace assistant",
    "marketplace assistant",
    "facebook assistant",
    "assistant",
}

# ⛔ Assinaturas de conteúdo do "Facebook Marketplace Assistant" (bot do Facebook).
# Guard de última linha: se a thread abre sob rótulo errado do sidebar, o texto denuncia.
FRASES_BOT_FACEBOOK = (
    "nao podemos responder a mensagens agora",
    "acesse a nossa central de ajuda",
    "seu classificado nao foi renovado",
    "gostaria de renova-lo agora",
    "renovar classificado",
    "renewed your listing",
    "renew your listing again after",
)


def _norm_txt(v: str) -> str:
    v = unicodedata.normalize("NFKD", str(v or ""))
    v = "".join(c for c in v if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", v.lower()).strip()


def is_conteudo_bot_facebook(texto: str) -> bool:
    t = _norm_txt(texto)
    return any(f in t for f in FRASES_BOT_FACEBOOK)

STATE_DIR    = Path.home() / ".impar-n8n-core/state"
CONFIG       = STATE_DIR / "config.json"
PROCESSED    = Path.home() / ".local/impar-automation/marketplace-leads/capture-processed.json"
LAST_PHONE_F = Path.home() / ".local/impar-automation/marketplace-leads/.last-phone.json"
SCRIPTS_DIR  = Path.home() / ".local/impar-automation"
LOG          = Path.home() / ".local/impar-automation/marketplace-leads/captador.log"
# Usa o mesmo perfil do navegador da varredura_inbox.py (já autenticado)
BROWSER_PROFILE = Path.home() / ".local/impar-automation/messenger/browser-profile"


def log(msg: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")


def load_config() -> dict:
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    return {}


def load_processed() -> set:
    if PROCESSED.exists():
        try:
            return set(json.loads(PROCESSED.read_text()))
        except Exception:
            return set()
    return set()


def save_processed(ids: set):
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.write_text(json.dumps(list(ids), ensure_ascii=False))


def load_last_phone() -> str:
    """Retorna último telefone capturado, mas só se foi há menos de 30 minutos.
    Expirar evita que telefone de sessão anterior contamine nova sessão horas depois."""
    try:
        data = json.loads(LAST_PHONE_F.read_text())
        ts = data.get("ts", 0)
        if time.time() - ts > 1800:  # expirado após 30 min
            return ""
        return data.get("phone", "")
    except Exception:
        return ""


def save_last_phone(phone: str):
    try:
        LAST_PHONE_F.write_text(json.dumps({"phone": phone, "ts": time.time()}, ensure_ascii=False))
    except Exception:
        pass


RESPOSTA_PADRAO = (
    "Olá! Obrigado pelo seu interesse no nosso imóvel. 😊\n"
    "Para que possamos te ajudar melhor, poderia nos informar seu nome completo "
    "e um número de WhatsApp para contato?\n\n"
    "Em breve um de nossos corretores especializados entrará em contato!"
)


def extrair_telefone(texto: str) -> str:
    padrao = re.compile(
        r'(?:\+?55\s?)?'
        r'(?:\(?\d{2}\)?\s?)'
        r'(?:9\s?)?\d{4}[-\s]?\d{4}'
    )
    m = padrao.search(texto)
    if m:
        digits = re.sub(r'\D', '', m.group())
        if not digits.startswith("55"):
            digits = "55" + digits
        if len(digits) >= 12:
            return digits
    return ""


def dismiss_notifications_panel(page):
    """
    Fecha painel de Notificações do Facebook se estiver sobreposto ao inbox.
    Sem isso, o painel cobre a lista de conversas e a detecção por div encontra 0 threads.
    """
    try:
        has_notif = page.evaluate("""
        () => {
            const heads = [...document.querySelectorAll('h1, h2, [role="heading"]')];
            return heads.some(el => {
                const t = (el.innerText || '').trim().toLowerCase();
                return t === 'notificações' || t === 'notifications';
            });
        }
        """)
        if has_notif:
            page.keyboard.press('Escape')
            time.sleep(0.5)
            page.mouse.click(640, 60)
            time.sleep(0.8)
            page.keyboard.press('Escape')
            time.sleep(0.5)
    except Exception:
        pass


def run_capture():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("ERRO: Playwright não instalado. Execute: pip install playwright && playwright install chromium")
        sys.exit(1)

    processed = load_processed()
    novos_leads = []

    # Reutiliza a sessão autenticada da varredura_inbox.py (sem novo login)
    with sync_playwright() as p:
        BROWSER_PROFILE.mkdir(parents=True, exist_ok=True)
        browser = p.chromium.launch_persistent_context(
            str(BROWSER_PROFILE),
            headless=True,
            viewport={"width": 1920, "height": 1080},
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        page = browser.new_page()

        # Acessa Marketplace inbox (sessão já autenticada)
        page.goto("https://www.facebook.com/marketplace/inbox/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)

        if "login" in page.url:
            log("AVISO: Sessão expirada. Rode varredura_inbox.py primeiro para autenticar.")
            browser.close()
            return

        # O painel da caixa de entrada às vezes renderiza "Ocorreu um erro" (falha
        # intermitente de carregamento em modo headless) — sem reload, a detecção
        # de threads sempre dá 0, mesmo com sessão válida e conversas reais pendentes.
        def tem_erro_de_carregamento():
            try:
                return page.evaluate("""
                () => document.body.innerText.toLowerCase().includes('ocorreu um erro')
                """)
            except Exception:
                return False

        for _tentativa_reload in range(3):
            if not tem_erro_de_carregamento():
                break
            log(f"[AVISO] Painel da caixa de entrada com erro — recarregando (tentativa {_tentativa_reload + 1})")
            page.reload(wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)

        dismiss_notifications_panel(page)

        # Detecta conversas por div — igual varredura_inbox.py (marketplace mode: x>=300, viewport 1920x1080)
        # A UI atual do Facebook não usa mais <a href> nas linhas do inbox — são divs.
        # A linha que começa com '·' é o nome do anúncio Marketplace.
        UI_WORDS_JS = '["localização","location","pesquisar","search","mensagens","messages","marketplace","início","home","notificações","notifications","ver mais","see more","recarregar","reload","tentar novamente"]'
        DETECT_JS = f"""
        () => {{
            const uiWords = {UI_WORDS_JS};
            const byName = {{}};
            const guardar = (nome, txt, cx, cy, listagem, naoLida) => {{
                if (byName[nome]) return;
                byName[nome] = {{nome, txt, cx, cy, listagem, naoLida}};
            }};
            document.querySelectorAll('div').forEach(el => {{
                const bb = el.getBoundingClientRect();
                if (bb.width < 280 || bb.width > 800) return;
                if (bb.height < 45 || bb.height > 120) return;
                if (bb.x < 200) return;
                if (bb.y < 100) return;
                const txt = (el.innerText || '').trim();
                if (txt.length < 5 || txt.length > 600) return;
                const lines = txt.split('\\n').map(s => s.trim()).filter(Boolean);
                if (lines.length < 2) return;
                const linhaListagem = lines.find(l => l.startsWith('·'));
                if (!linhaListagem) return;
                const nome = lines[0] || '';
                if (!nome || nome.length > 80 || nome.startsWith('·')) return;
                if (uiWords.includes(nome.toLowerCase())) return;
                // Bolinha azul de não lida: elemento pequeno e arredondado à esquerda da linha
                let naoLida = false;
                el.querySelectorAll('div').forEach(sub => {{
                    const sb = sub.getBoundingClientRect();
                    if (sb.width >= 6 && sb.width <= 14 && Math.abs(sb.width - sb.height) < 3
                        && sb.x < bb.x + 20) {{
                        naoLida = true;
                    }}
                }});
                guardar(nome, txt, Math.round(bb.x + bb.width / 2), Math.round(bb.y + bb.height / 2),
                        linhaListagem.replace(/^·\\s*/, ''), naoLida);
            }});
            return Object.values(byName);
        }}
        """
        SCROLL_SIDEBAR_JS = """
        (px) => {
            const els = Array.from(document.querySelectorAll('*'));
            for (const el of els) {
                const s = window.getComputedStyle(el);
                const bb = el.getBoundingClientRect();
                if ((s.overflowY === 'auto' || s.overflowY === 'scroll')
                    && el.scrollHeight > el.clientHeight + 50
                    && bb.x < 650 && bb.width > 150 && bb.height > 300) {
                    const before = el.scrollTop;
                    el.scrollTop += px;
                    if (el.scrollTop !== before) return true;
                }
            }
            return false;
        }
        """

        # Rola a lista lateral coletando conversas mais abaixo — sem isso o script
        # só via as ~6-10 conversas do topo e nunca alcançava leads reais mais antigos.
        byName_all = {}
        for t in page.evaluate(DETECT_JS):
            byName_all[t["nome"]] = t

        # Retry: a SPA do Facebook às vezes ainda não terminou de hidratar a lista
        # 5s após domcontentloaded, ou o painel de Notificações cobre o inbox —
        # sem isso o ciclo inteiro registrava 0 threads.
        if not byName_all:
            if tem_erro_de_carregamento():
                log("[AVISO] Painel com erro na 2ª checagem — recarregando")
                page.reload(wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)
            dismiss_notifications_panel(page)
            time.sleep(5)
            for t in page.evaluate(DETECT_JS):
                byName_all[t["nome"]] = t
        for _ in range(8):
            moved = page.evaluate(SCROLL_SIDEBAR_JS, 500)
            if not moved:
                break
            time.sleep(1)
            novos = 0
            for t in page.evaluate(DETECT_JS):
                if t["nome"] not in byName_all:
                    byName_all[t["nome"]] = t
                    novos += 1
            if novos == 0:
                break

        raw_threads = list(byName_all.values())
        log(f"Threads encontradas: {len(raw_threads)}")

        # Volta a lista ao topo (coordenadas dos itens ficam obsoletas após rolar
        # para coletar nomes mais abaixo — cada item é relocalizado antes do clique).
        page.evaluate(SCROLL_SIDEBAR_JS, -100000)
        time.sleep(0.8)

        def localizar_e_clicar(nome_alvo: str):
            """Relocaliza a conversa pelo nome (a lista pode ter rolado) e clica."""
            dismiss_notifications_panel(page)
            for _tentativa in range(10):
                for t in page.evaluate(DETECT_JS):
                    if t["nome"] == nome_alvo:
                        page.mouse.click(t["cx"], t["cy"])
                        return True
                if not page.evaluate(SCROLL_SIDEBAR_JS, 500):
                    break
                time.sleep(0.8)
            return False

        # Carrega o último telefone da sessão anterior para detectar contaminação
        # também no PRIMEIRO lead de cada nova sessão do captador.
        _last_phone_extracted = load_last_phone()

        for t in raw_threads:
            try:
                nome = t.get("nome", "Desconhecido").strip()

                if not nome:
                    continue

                # ⛔ Guard: nunca processar bots do Facebook
                nome_lower = nome.strip().lower()
                if nome_lower in NOMES_BLOQUEADOS or any(nome_lower in b for b in NOMES_BLOQUEADOS):
                    log(f"[IGNORADO] {nome} — nome bloqueado (bot do Facebook)")
                    processed.add(nome)
                    continue

                if nome in processed:
                    continue

                # Captura log ANTES de clicar para detectar quando ele atualizar.
                try:
                    _log_before_click = page.evaluate(
                        "() => { const el = document.querySelector('[role=\"log\"]'); "
                        "return el ? el.innerText.slice(0, 300) : ''; }"
                    )
                except Exception:
                    _log_before_click = ""

                # Relocaliza e abre a conversa (rolagem pode ter mudado a posição)
                if not localizar_e_clicar(nome):
                    log(f"[ERRO] {nome} — não localizada na lista após rolagem, pulando")
                    continue
                time.sleep(1)

                # Obtém thread ID da URL se disponível (para deduplicação futura)
                tid_match = re.search(r'/t/(\d+)', page.url)
                tid = tid_match.group(1) if tid_match else nome

                if tid != nome and tid in processed:
                    continue

                # Aguarda heading E log estabilizarem na nova conversa.
                # Estratégia: heading deve mostrar o nome esperado; depois aguarda o
                # log mudar do conteúdo pré-clique E ficar estável por 2 verificações
                # seguidas (sinal de que o carregamento terminou).
                nome_first = nome.split()[0].lower()

                # 1) Espera heading
                for _ in range(20):  # até 10s
                    try:
                        headings = page.evaluate(
                            """() => [...document.querySelectorAll('h1,h2,[role="heading"]')]
                                       .filter(e => e.getBoundingClientRect().x > 300)
                                       .map(e => (e.innerText || '').trim().toLowerCase())
                                       .filter(Boolean)"""
                        )
                        if any(nome_first in h for h in headings):
                            break
                    except Exception:
                        pass
                    time.sleep(0.5)

                # 2) Espera log CORRETO (painel da conversa, x>380) mudar, não conter o telefone
                # anterior, e estabilizar. Filtro geométrico obrigatório: Facebook tem múltiplos
                # [role="log"] no DOM — o primeiro pode ser a sidebar com preview de TODOS os leads,
                # incluindo telefone do lead anterior. Só aceitar elemento com bounding box x>380.
                _prev_check = ""
                _stable = 0
                _last_phone_digits = re.sub(r'\D', '', _last_phone_extracted) if _last_phone_extracted else ""
                _GET_CONV_LOG_JS = """
                () => {
                    let best = '';
                    for (const el of document.querySelectorAll('[role="log"]')) {
                        const bb = el.getBoundingClientRect();
                        if (bb.x < 380 || bb.width < 200 || bb.height < 60) continue;
                        const t = (el.innerText || '').trim();
                        if (t.length > best.length) best = t;
                    }
                    return best;
                }
                """
                for _ in range(40):  # até 20s
                    try:
                        _log_now = page.evaluate(_GET_CONV_LOG_JS)
                        _log_digits = re.sub(r'\D', '', _log_now)
                        _still_contaminated = bool(_last_phone_digits and _last_phone_digits in _log_digits)
                        if _log_now != _log_before_click and len(_log_now) > 30 and not _still_contaminated:
                            if _log_now == _prev_check:
                                _stable += 1
                                if _stable >= 3:  # estável por ~1.5s
                                    break
                            else:
                                _stable = 0
                                _prev_check = _log_now
                        else:
                            _stable = 0  # reset se log ainda tem conteúdo antigo
                    except Exception:
                        pass
                    time.sleep(0.5)

                # Lê texto completo da conversa — usa o mesmo filtro geométrico (x>380)
                # para garantir que lemos o painel da conversa, nunca a sidebar.
                try:
                    texto_conversa = page.evaluate(_GET_CONV_LOG_JS)
                    if len(texto_conversa.strip()) < 20:
                        # fallback: qualquer log visível no painel direito
                        texto_conversa = page.evaluate("""
                        () => {
                            for (const el of document.querySelectorAll('[role="log"], [aria-label*="onvers"]')) {
                                const bb = el.getBoundingClientRect();
                                if (bb.x < 300 || bb.width < 200) continue;
                                const t = (el.innerText || '').trim();
                                if (t.length >= 20) return t;
                            }
                            return '';
                        }
                        """)
                    if len(texto_conversa.strip()) < 20:
                        texto_conversa = page.inner_text('body') if page.query_selector('body') else ""
                except Exception:
                    texto_conversa = page.inner_text('body') if page.query_selector('body') else ""

                # ⛔ Guard de conteúdo: bot do Facebook Marketplace Assistant
                if is_conteudo_bot_facebook(texto_conversa):
                    log(f"[IGNORADO] {nome} | {tid} — conteúdo de bot do Facebook")
                    processed.add(tid)
                    processed.add(nome)
                    continue

                telefone = extrair_telefone(texto_conversa)

                # Guard anti-contaminação: mesmo telefone em dois leads seguidos =
                # [role="log"] ainda exibindo a conversa anterior (React reutiliza o DOM).
                # _last_phone_extracted é persistido entre sessões para pegar também o
                # primeiro lead de cada nova rodada do captador.
                if telefone and telefone == _last_phone_extracted:
                    log(f"[SEM_TEL] {nome} | {tid} — telefone idêntico ao anterior ({telefone}), possível contaminação")
                    telefone = ""
                elif telefone:
                    _last_phone_extracted = telefone
                    save_last_phone(telefone)

                # Extrai link real do anúncio Marketplace.
                # IMPORTANTE: escolher o link com MENOR y (mais no topo do painel, x>380) —
                # o card do anúncio fica no topo; mensagens nossas enviadas anteriormente
                # também contêm o link e aparecem mais abaixo, causando link incorreto se
                # pegarmos "o primeiro <a>" do DOM sem filtro geométrico.
                link_imovel = ""
                for _link_try in range(3):
                    try:
                        page.wait_for_selector('a[href*="/marketplace/item/"]', timeout=5000)
                    except Exception:
                        pass
                    link_imovel = page.evaluate("""
                    () => {
                        let melhor = null, melhorY = Infinity;
                        for (const a of document.querySelectorAll('a[href]')) {
                            const href = a.href || a.getAttribute('href') || '';
                            const m = href.match(/marketplace\\/item\\/(\\d{6,})/);
                            if (!m) continue;
                            const bb = a.getBoundingClientRect();
                            if (bb.x < 380) continue;  // nunca sidebar
                            if (bb.y < melhorY) { melhorY = bb.y; melhor = m[1]; }
                        }
                        if (melhor) return 'https://www.facebook.com/marketplace/item/' + melhor + '/';
                        // fallback: JSON embutido nos scripts da página
                        for (const s of document.querySelectorAll('script')) {
                            const t = s.textContent || '';
                            if (!t.includes('marketplace')) continue;
                            const m2 = t.match(/"(?:item_id|marketplace_listing_id|listing_id)"\\s*:\\s*"?(\\d{10,})"?/);
                            if (m2) return 'https://www.facebook.com/marketplace/item/' + m2[1] + '/';
                        }
                        return '';
                    }
                    """)
                    if link_imovel:
                        break
                    if _link_try < 2:
                        time.sleep(3)

                listagem = t.get("listagem", "").strip()
                resumo_imovel = link_imovel or listagem or "Marketplace Facebook"
                if not link_imovel:
                    log(f"[AVISO] {nome} | {tid} — sem URL do anúncio, usando título: {listagem}")

                # Sem telefone: não marca como processado — retry no próximo ciclo
                if not telefone:
                    log(f"[SEM_TEL] {nome} | {tid} — sem telefone ainda, aguardando próxima varredura")
                    continue

                novos_leads.append({
                    "nome":      nome,
                    "telefone":  telefone,
                    "link":      resumo_imovel,
                    "thread_id": tid,
                })
                processed.add(tid)
                processed.add(nome)
                time.sleep(1)

            except Exception as e:
                log(f"Erro ao processar thread: {e}")
                continue

        browser.close()

    save_processed(processed)
    log(f"Novos leads capturados: {len(novos_leads)}")

    BASE = Path.home() / ".local/impar-automation/marketplace-leads"
    py3 = sys.executable

    for lead in novos_leads:
        nome     = lead["nome"]
        telefone = lead["telefone"]
        link     = lead["link"]

        log(f"[LEAD] {nome} | {telefone} | {link or 'sem link'}")

        # 1. Salva no Google Sheets (leads + follow-up)
        cmd_planilha = [
            py3, str(BASE / "atualizar_planilha.py"),
            "--nome", nome,
            "--telefone", telefone,
            "--link", link,
            "--origem", "marketplace",
        ]
        r = subprocess.run(cmd_planilha, timeout=30, capture_output=True, text=True)
        if r.returncode == 0:
            log(f"[SHEETS OK] {nome}")
        else:
            log(f"[SHEETS ERRO] {nome}: {r.stderr.strip()[:200]}")

        # 2. Notifica Telegram da Impar Imóveis
        cmd_notif = [
            py3, str(BASE / "notificar_lead_whatsapp.py"),
            "--nome", nome,
            "--telefone", telefone,
            "--resumo", "Marketplace Facebook",
            "--link-imovel", link,
            "--origem", "marketplace",
        ]
        r2 = subprocess.run(cmd_notif, timeout=30, capture_output=True, text=True)
        if r2.returncode == 0:
            log(f"[TELEGRAM OK] {nome}")
        else:
            log(f"[TELEGRAM ERRO] {nome}: {r2.stderr.strip()[:200]}")


if __name__ == "__main__":
    run_capture()
