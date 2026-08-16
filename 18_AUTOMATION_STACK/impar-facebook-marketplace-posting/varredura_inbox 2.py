#!/usr/bin/env python3
"""
Varredura Messenger Marketplace v3 — Impar Imóveis.
Correções: deduplicação por Y, press_sequentially para input, verificação de envio por screenshot.
"""
import csv, json, re, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path
from openai import OpenAI

_PROFILE_LOCAL  = Path.home() / ".local/impar-automation/messenger/browser-profile"
_PROFILE_ICLOUD = Path("/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-profile")
PROFILE = _PROFILE_LOCAL if (_PROFILE_LOCAL / "Default").exists() else _PROFILE_ICLOUD
CSV_PATH   = Path("/Users/user/.local/impar-automation/messenger/leads_marketplace_captura.csv")
CSV_ICLOUD = Path("/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/leads_marketplace_captura.csv")
LOG_PATH   = Path("/Users/user/.local/impar-automation/messenger/messenger-rodadas.md")
JONATA_WA  = "554796876631"
INBOX_URL  = "https://www.facebook.com/marketplace/inbox/"
OPENAI_KEY = "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"
OPENAI_MODEL = "gpt-4o-mini"
PHONE_RE  = re.compile(
    r'(?:\+?55[\s.\-]?)?'        # +55 opcional
    r'(?:\(?\d{2}\)?[\s.\-]?)?'  # DDD opcional
    r'(?:9[\s.\-]?)?'            # 9º dígito móvel com possível espaço
    r'\d{4}[\s.\-]?\d{4}'        # 8 dígitos principais
)

NOTIF_ICLOUD     = Path("/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/notificar_lead_whatsapp.py")
NOTIF_LOCAL      = Path.home() / ".local/impar-automation/messenger/notificar_lead_whatsapp.py"
SELF_ICLOUD      = Path("/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/varredura_inbox.py")
NOTIFICADOS_PATH = Path.home() / ".local/impar-automation/messenger/notificados-varredura.json"

def _sync_notif_script():
    """Copia notificar_lead_whatsapp.py e varredura_inbox.py do kit → local se kit for mais novo."""
    try:
        if NOTIF_ICLOUD.exists():
            if not NOTIF_LOCAL.exists() or NOTIF_ICLOUD.stat().st_mtime > NOTIF_LOCAL.stat().st_mtime:
                shutil.copy2(NOTIF_ICLOUD, NOTIF_LOCAL)
    except Exception:
        pass
    try:
        self_local = Path(__file__).resolve()
        if SELF_ICLOUD.exists() and SELF_ICLOUD.stat().st_mtime > self_local.stat().st_mtime:
            shutil.copy2(SELF_ICLOUD, self_local)
    except Exception:
        pass

def _sync_csv_from_icloud():
    """Copia iCloud → local se iCloud for mais novo ou local não existir."""
    try:
        if CSV_ICLOUD.exists():
            if not CSV_PATH.exists() or CSV_ICLOUD.stat().st_mtime > CSV_PATH.stat().st_mtime:
                shutil.copy2(CSV_ICLOUD, CSV_PATH)
    except Exception:
        pass

def _sync_csv_to_icloud():
    """Copia local → iCloud após escrita. Falha silenciosa se TCC bloquear."""
    try:
        shutil.copy2(CSV_PATH, CSV_ICLOUD)
    except Exception:
        pass

def load_known_phones():
    if not CSV_PATH.exists():
        return set()
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        return {re.sub(r'[^\d]', '', r[1]) for r in csv.reader(f)
                if len(r) > 1 and r[1].strip()}

def load_notified_today() -> set:
    """Retorna set de phones notificados hoje (evita dupla notificação na mesma execução)."""
    today = datetime.now().strftime('%Y-%m-%d')
    if not NOTIFICADOS_PATH.exists():
        return set()
    try:
        data = json.loads(NOTIFICADOS_PATH.read_text())
        return {e.split('|')[0] for e in data if e.endswith(f'|{today}')}
    except Exception:
        return set()

def mark_notified(notif_set: set, phone: str):
    today = datetime.now().strftime('%Y-%m-%d')
    notif_set.add(phone)
    key = f"{phone}|{today}"
    try:
        existing = json.loads(NOTIFICADOS_PATH.read_text()) if NOTIFICADOS_PATH.exists() else []
        if key not in existing:
            existing.append(key)
        NOTIFICADOS_PATH.write_text(json.dumps(existing[-500:]))
    except Exception:
        pass

def load_phones_to_names():
    """Retorna dict phone_digits → nome, para validação anti-falso-positivo do sidebar."""
    if not CSV_PATH.exists():
        return {}
    result = {}
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            fone = re.sub(r'[^\d]', '', str(row.get('Telefone') or ''))
            if fone and len(fone) >= 8:
                result[fone] = row.get('Nome', '')
    return result

def append_lead(nome, telefone, tipo, link, obs):
    header = ['Nome','Telefone','Tipo Imóvel','Link','Bairro','Status','Data','Fonte','Observações']
    exists = CSV_PATH.exists()
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        w.writerow([nome, telefone, tipo, link, '', 'novo',
                    datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'Messenger Marketplace', obs])
    _sync_csv_to_icloud()

def mensagem_cliente(nome, link):
    """Template padrão de resposta ao lead."""
    return (f"Ola {nome.split()[0]}\n"
            f"Estavamos conversando sobre o imóvel\n"
            f"{link}\n"
            f"Você deseja tirar mais duvidas ou gostaria de agendar uma visita?")

def wa_link(telefone):
    """Gera link wa.me clicável para o número do lead (formato 55 + dígitos)."""
    digits = re.sub(r'[^\d]', '', telefone)
    if not digits.startswith('55'):
        digits = '55' + digits
    return f"https://wa.me/{digits}"

GRUPO_LEADS = "Novos leads"

def notificar_jonata(nome, telefone, imovel, link_anuncio) -> bool:
    """Envia alerta via notificar_lead_whatsapp.py (método CGEvent validado + formato correto).
    Retorna True somente se o envio ao WhatsApp foi confirmado (exit 0)."""
    notif_script = Path.home() / ".local/impar-automation/messenger/notificar_lead_whatsapp.py"
    try:
        result = subprocess.run(
            [sys.executable, str(notif_script),
             '--nome', nome,
             '--telefone', telefone,
             '--resumo', imovel,
             '--link-imovel', link_anuncio or '',
             '--origem', 'marketplace'],
            timeout=60
        )
        if result.returncode == 0:
            print(f"    📱 Grupo '{GRUPO_LEADS}' notificado: {nome} / {telefone}")
            return True
        else:
            print(f"    ⚠ notificar_jonata: exit {result.returncode} — NÃO marcando como notificado")
            return False
    except Exception as e:
        print(f"    ⚠ notificar_jonata: {e} — NÃO marcando como notificado")
        return False

def update_log(stats, leads, status, ts):
    if status == "INBOX_VAZIA":
        entry = f"\n## {ts} -03 (Varredura automática) — ✅ INBOX VAZIA\n\n[{ts}] inbox vazia\n\n**Status: ✅ Encerrado.**\n\n---\n"
    elif status == "LOGIN_EXPIRADO":
        entry = f"\n## {ts} -03 — ⛔ LOGIN EXPIRADO\n\nExecutar `login-facebook.py`.\n\n---\n"
    elif status.startswith("BLOQUEIO"):
        entry = f"\n## {ts} -03 — ⛔ {status}\n\nCaptcha/2FA. Ação manual necessária.\n\n---\n"
    else:
        leads_txt = "".join(f"  - {l['nome']}: {l['telefone']} ({l['imovel']})\n" for l in leads)
        entry = (f"\n## {ts} -03 (Varredura automática) — ✅ EXECUTADA\n\n"
                 f"**Verificadas:** {stats['v']} | **Respondidas:** {stats['r']} | "
                 f"**Telefones:** {stats['t']} | **Puladas:** {stats['p']} | **Erros:** {stats['e']}\n\n")
        if leads:
            entry += f"**Leads:**\n{leads_txt}\n"
        entry += "**Status: ✅ Concluída.**\n\n---\n"
    txt = LOG_PATH.read_text(encoding='utf-8') if LOG_PATH.exists() else "# Log de Varreduras — Marketplace Inbox\n"
    cut = txt.find('\n\n')
    LOG_PATH.write_text((txt[:cut+2] + entry + txt[cut+2:]) if cut != -1 else txt + entry, encoding='utf-8')

NOSSAS_FRASES = [
    "Certo, vou atualizar",
    "Obrigado, vou entrar em contato",
    "Qual seu whatsapp para retorno",
    "Recebi seu n",
    "Vou verificar com o corretor",
]
TIMESTAMP_RE_STR = r'^\d{1,2}:\d{2}$|^(Seg|Ter|Qua|Qui|Sex|Sáb|Dom)$|^\d{1,2}/\d{1,2}$'

def get_unique_threads(page, messages_mode=False):
    """
    Detecção compatível com a UI atual do Facebook (2026-07/08).
    messages_mode=True: layout facebook.com/messages/ (sidebar esquerdo x<450)
    messages_mode=False: layout marketplace/inbox/ (thread list x>=300)
    """
    import re as _re
    ts_pat = _re.compile(TIMESTAMP_RE_STR)

    # Palavras da UI do Facebook que não são nomes de lead
    UI_WORDS = {'mais', 'more', 'vendendo', 'comprando', 'marketplace', 'inbox',
                'conversas', 'mensagens', 'filtros', 'all', 'todos', 'arquivadas',
                'spam', 'solicitações', 'requests', 'bate-papo', 'chats',
                'recarregar', 'reload', 'tentar novamente', 'tentar de novo',
                # categorias da sidebar do marketplace
                'suprimentos', 'venda', 'vestuário', 'grupos', 'eletrônicos',
                'veículos', 'casa e jardim', 'itens', 'hobbies', 'brinquedos',
                'esporte', 'jardim', 'ferramentas', 'roupas', 'calçados',
                'moveis', 'móveis', 'livros', 'jogos', 'animais', 'pets',
                'colecionáveis', 'instrumentos', 'beleza', 'saúde', 'bebês',
                'artes', 'antiguidades', 'alimentos', 'serviços', 'alugueis',
                'aluguel', 'propriedades', 'imóveis', 'imoveis',
                # itens de navegação do sidebar do marketplace/inbox
                'explorar', 'notificações', 'notificacoes', 'caixa', 'acesso',
                'compra', 'locação', 'locacao', 'artigos', 'veículos', 'criar',
                'conta', 'central', 'ajuda', 'configurações', 'configuracoes'}

    x_min = 60 if messages_mode else 60
    x_max = 450 if messages_mode else 9999

    raw = page.evaluate(f"""
    () => {{
        const x_min = {x_min}, x_max = {x_max};
        const byName = {{}};
        document.querySelectorAll('div, a').forEach(el => {{
            const bb = el.getBoundingClientRect();
            if (bb.width < 200 || bb.height < 20 || bb.height > 120) return;
            if (bb.x < x_min || bb.x > x_max) return;
            if (bb.y < 160 || bb.y > 850) return;  // exclui topo e categorias da sidebar abaixo do viewport
            // Excluir links de navegação do Marketplace (não são conversas)
            if (el.tagName === 'A') {{
                const href = el.href || '';
                const navPaths = ['/marketplace/notifications', '/marketplace/status',
                    '/marketplace/you', '/marketplace/category', '/marketplace/search',
                    '/marketplace/create', '/marketplace/help'];
                if (navPaths.some(p => href.includes(p))) return;
                if (/facebook\\.com\\/marketplace\\/?$/.test(href)) return;
            }}
            const txt = (el.innerText || '').trim();
            if (txt.length < 3 || txt.length > 500) return;
            const lines = txt.split('\\n').map(s => s.trim()).filter(Boolean);
            const nome = lines[0] || '';
            if (!nome || nome.length > 40 || nome.startsWith('·')) return;
            if (!byName[nome] || bb.y < byName[nome].y) {{
                byName[nome] = {{
                    nome, lines, txt: txt.slice(0, 300),
                    cx: Math.round(bb.x + bb.width / 2),
                    cy: Math.round(bb.y + bb.height / 2),
                    y: bb.y
                }};
            }}
        }});
        return Object.values(byName);
    }}
    """)

    unique = []
    for t in raw:
        if not t['nome']:
            continue
        # Filtro: ignorar palavras da UI de navegação do Facebook
        nome_lower = t['nome'].lower()
        nome_first = nome_lower.split()[0] if nome_lower else ''
        if nome_lower in UI_WORDS or nome_first in UI_WORDS \
                or nome_lower[:3] == 'voc' \
                or nome_lower.startswith('recarreg') or nome_lower.startswith('reload') \
                or nome_lower.startswith('tentar'):
            continue
        # Preview = última linha de conteúdo, excluindo timestamps
        content = [l for l in t['lines'] if l and not ts_pat.match(l) and l != '·']
        content = content[1:] if len(content) > 1 else content  # remove nome
        preview = content[-1] if content else ''
        # Thread pendente se a última mensagem NÃO é explicitamente nossa
        # Preview vazio = pode ser mensagem nova sem texto visível — incluir
        is_our_reply = preview and any(p in preview for p in NOSSAS_FRASES)
        if not is_our_reply:
            unique.append({'text': t['nome'], 'preview': preview,
                           'imovel_hint': t['txt'],
                           'cx': t['cx'], 'cy': t['cy'], 'y': t['cy']})

    return unique

def get_nome(text):
    return text.split()[0] if text else ""

def click_thread(page, nome_full):
    """
    v4 — usa page.mouse.click (CDP) em vez de el.click() (JS).
    el.click() não dispara eventos sintéticos React; CDP sim.
    """
    nome_first = nome_full.split()[0]

    # Strategy 1: Playwright locator (CDP nativo, melhor para React SPA)
    for selector in [
        f'[role="link"]:has-text("{nome_first}")',
        f'[role="button"]:has-text("{nome_first}")',
        f'a:has-text("{nome_first}")',
    ]:
        try:
            loc = page.locator(selector)
            count = loc.count()
            for i in range(min(count, 5)):
                el = loc.nth(i)
                bb = el.bounding_box()
                if bb and bb['y'] > 160 and bb['width'] > 80:
                    el.click(timeout=3000)
                    return True
        except Exception:
            continue

    # Strategy 2: JS acha coordenada → page.mouse.click (CDP, não JS click)
    result = page.evaluate(f"""
    () => {{
        let best = null, bestScore = -1;
        for (const el of document.querySelectorAll('div, a')) {{
            const txt = (el.innerText || '').trim();
            const first_line = txt.split('\\n')[0].trim();
            if (first_line !== '{nome_first}' && !first_line.startsWith('{nome_first} ')) continue;
            const bb = el.getBoundingClientRect();
            if (bb.width < 100 || bb.height < 20 || bb.height > 120 || bb.y < 160) continue;
            const score = bb.width + (bb.height > 30 ? 10 : 0);
            if (score > bestScore) {{ bestScore = score; best = {{cx: bb.x + bb.width / 2, cy: bb.y + bb.height / 2}}; }}
        }}
        return best;
    }}
    """)
    if result:
        page.mouse.click(result['cx'], result['cy'])
        return True

    return False

def get_conv_text(page):
    """Lê apenas o log de mensagens — evita contaminar com sidebar."""
    for sel in ['[role="log"]', '[aria-label="Conversa"]', '[aria-label="Conversation"]']:
        try:
            el = page.query_selector(sel)
            if el:
                return el.inner_text()
        except Exception:
            pass
    try: return page.inner_text('[role="main"]')
    except Exception:
        try: return page.inner_text('body')
        except Exception: return ""

def get_listing_url(page):
    """Extrai link do anúncio da conversa — card acima + DOM completo + URL atual + scroll."""
    pat = re.compile(r'marketplace/item/(\d+)')

    def _eval(js):
        try:
            return page.evaluate(js)
        except Exception:
            return None

    # 1. Card do anúncio visível acima da conversa
    url = _eval("""
    () => {
        const pat = /marketplace\\/item\\/(\\d+)/;
        for (const a of document.querySelectorAll('a[href*="/marketplace/item/"]')) {
            const m = (a.href || '').match(pat);
            if (m) return 'https://www.facebook.com/marketplace/item/' + m[1] + '/';
        }
        return null;
    }
    """)
    if url:
        return url

    # 2. URL atual já contém o item (quando FB navega para a thread do item)
    cur = page.url or ''
    m = pat.search(cur)
    if m:
        return f'https://www.facebook.com/marketplace/item/{m.group(1)}/'

    # 3. Scroll para o topo da conversa e tentar de novo (card pode estar acima do scroll)
    try:
        page.evaluate("() => { const log = document.querySelector('[role=\"log\"]'); if (log) log.scrollTop = 0; window.scrollTo(0,0); }")
        time.sleep(1.5)
    except Exception:
        pass
    url = _eval("""
    () => {
        const pat = /marketplace\\/item\\/(\\d+)/;
        for (const a of document.querySelectorAll('a[href]')) {
            const m = (a.href || '').match(pat);
            if (m) return 'https://www.facebook.com/marketplace/item/' + m[1] + '/';
        }
        // Fallback: varrer todo o innerHTML em busca do padrão
        const html = document.body.innerHTML || '';
        const fm = html.match(/marketplace\\/item\\/(\\d+)/);
        if (fm) return 'https://www.facebook.com/marketplace/item/' + fm[1] + '/';
        return null;
    }
    """)
    return url

def get_conv_nome(page):
    """Extrai o nome do contato da conversa aberta (cabeçalho da conversa)."""
    try:
        return page.evaluate("""
        () => {
            const skipWords = ['marketplace', 'conversas', 'inbox', 'mensagens', 'messages', 'messenger', 'chats', 'explorar', 'escrever', 'write', 'compose'];
            const candidates = [...document.querySelectorAll('h1, h2, [role="heading"]')];
            for (const el of candidates) {
                const txt = (el.innerText || '').trim();
                const low = txt.toLowerCase();
                if (txt && txt.length > 1 && txt.length < 60
                    && !skipWords.some(w => low.includes(w)))
                    return txt;
            }
            return null;
        }
        """)
    except Exception:
        return None

def extract_imovel(text):
    """Extrai título do imóvel do texto da conversa — card de anúncio ou palavras-chave."""
    # 1. Padrão típico de título de anúncio: "Apartamento X quartos em Bairro"
    title_pat = re.compile(
        r'((?:Apartamento|Apto|Casa|Sobrado|Terreno|Sala|Galpão|Kitnet|Studio|Cobertura|Loft|Lote|Chácara|Sítio)'
        r'[^\n\.!?]{5,80})',
        re.IGNORECASE
    )
    m = title_pat.search(text)
    if m:
        titulo = m.group(1).strip()
        if len(titulo) > 10:
            return titulo[:120]

    # 2. Fallback: primeira linha não-vazia que contém palavra de imóvel
    tipos = ['Casa','Terreno','Comercial','Sala','Galpão','Kitnet','Studio','Sobrado',
             'Cobertura','Loft','Lote','Chácara','Sítio','Apartamento','Apto']
    for line in text.split('\n'):
        line = line.strip()
        if 5 < len(line) < 120:
            for kw in tipos:
                if kw.lower() in line.lower():
                    return line

    # 3. Última reserva: tipo genérico
    for kw in tipos:
        if kw.lower() in text.lower():
            return kw
    return 'Apartamento'

def wait_for_conversation_open(page, timeout=15, base_url=None):
    """
    v4 — polling a cada 0.5s até timeout.
    Verifica URL, role=log e contenteditable em loop.
    Aceita tanto marketplace/inbox/THREAD como messages/t/THREAD.
    """
    base_url = (base_url or INBOX_URL).rstrip('/')
    deadline = time.time() + timeout

    CE_SELECTORS = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[contenteditable="true"]',
        '[aria-label="Aa"]',
        '[aria-placeholder="Aa"]',
        '[aria-label*="essagem"]',
        '[aria-label*="message"]',
        '[aria-label*="Escreva"]',
        '[aria-label*="Write"]',
    ]

    while time.time() < deadline:
        # 1. URL mudou para thread individual (marketplace ou messages)
        cur = page.url
        url_opened = (
            ('/marketplace/inbox/' in cur and cur.rstrip('/') != base_url) or
            ('/messages/t/' in cur) or
            ('/messages/e2ee/t/' in cur)
        )
        if url_opened:
            return True

        # 2. Log de conversa visível
        try:
            el = page.query_selector('[role="log"]')
            if el and el.is_visible():
                return True
        except Exception:
            pass

        # 3. Campo de input visível
        for sel in CE_SELECTORS:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    return True
            except Exception:
                pass

        time.sleep(0.5)

    # Debug ao expirar
    try:
        cur_url = page.url
        has_ce  = bool(page.query_selector('div[contenteditable="true"]'))
        has_log = bool(page.query_selector('[role="log"]'))
        print(f"    ⚠ Conversa não abriu | url_diff={cur_url.rstrip('/') != base_url} | ce={has_ce} | log={has_log}")
    except Exception:
        print("    ⚠ Conversa não abriu (debug falhou)")

    return False

def send_message(page, text):
    """
    Envia mensagem no popup do Messenger Marketplace.
    O popup abre com quick-reply buttons que interceptam cliques.
    Solução: Escape → clicar direto no input com force=True → type() → Enter.
    """
    try:
        # Fechar quick-reply suggestions com Escape
        page.keyboard.press('Escape')
        time.sleep(0.4)

        # Aguardar textbox (popup input "Aa")
        box = page.wait_for_selector(
            'div[contenteditable="true"][role="textbox"]',
            timeout=8000, state='visible'
        )
        if not box:
            print("    ⚠ Textbox não encontrado após Escape")
            return False

        bb = box.bounding_box()
        print(f"    debug: textbox em x={bb['x']:.0f} y={bb['y']:.0f} w={bb['width']:.0f} h={bb['height']:.0f}" if bb else "    debug: textbox sem bounding box")

        # Clicar com force para bypassar qualquer overlay residual
        box.click(force=True)
        time.sleep(0.4)

        # type() — método ElementHandle no Playwright 1.60
        box.type(text, delay=15)
        time.sleep(0.5)

        # Enviar com Enter
        page.keyboard.press('Enter')
        time.sleep(2.5)

        return True

    except Exception as e:
        print(f"    ⚠ send_message erro: {e}")
        return False

def is_thread_open(page):
    """Verifica se uma conversa está aberta (URL diferente do inbox)."""
    return '/marketplace/inbox/' in page.url and page.url != INBOX_URL

def is_marketplace_conv(page):
    """
    Guard obrigatório — verifica se a conversa aberta é do Marketplace.
    Critério: presença de a[href*="/marketplace/item/"] OU URL com /marketplace/.
    Aguarda até 6s pelo link do item (carregamento assíncrono em messages/ mode).
    Se retornar False → pular com stats['p'], NUNCA enviar.
    """
    if '/marketplace/' in page.url:
        return True
    # Aguardar carregamento assíncrono do link do item (comum em messages/ mode)
    try:
        page.wait_for_selector('a[href*="/marketplace/item/"]', timeout=6000)
        return True
    except Exception:
        pass
    # Verificação DOM como último recurso
    try:
        return bool(page.evaluate(
            "() => document.querySelector('a[href*=\"/marketplace/item/\"]') !== null"
        ))
    except Exception:
        return False

def analisar_com_regras(conv_text, nome, preview):
    """Análise por regras — sem API externa, zero custo.
    1. Telefone na conversa → CAPTUROU_CONTATO
    2. Última mensagem é nossa → SEM_ACAO
    3. Lead respondeu algo → PEDIR_CONTATO
    """
    # 1. Qualquer telefone mencionado na conversa
    phones = PHONE_RE.findall(conv_text)
    if phones:
        raw = phones[-1]
        telefone = re.sub(r'[^\d]', '', raw)
        if len(telefone) >= 8:
            return {"acao": "CAPTUROU_CONTATO", "telefone": telefone}

    # 2. Verificar se última mensagem relevante é nossa
    ts_pat = re.compile(TIMESTAMP_RE_STR)
    lines = [l.strip() for l in conv_text.split('\n')
             if l.strip() and not ts_pat.match(l.strip()) and l.strip() != '·']
    last_block = ' '.join(lines[-8:]) if lines else ''
    if any(p in last_block for p in NOSSAS_FRASES):
        return {"acao": "SEM_ACAO", "telefone": None}

    # 3. Preview existe → lead aguarda resposta
    if preview and preview.strip() and len(preview.strip()) > 2:
        return {"acao": "PEDIR_CONTATO", "telefone": None}

    return {"acao": "SEM_ACAO", "telefone": None}


# Mantido como fallback caso OpenAI seja reativada no futuro
def analisar_com_ia(conv_text, nome, preview):
    try:
        from openai import OpenAI as _OAI
        client = _OAI(api_key=OPENAI_KEY)
        system = (
            "Você é assistente de atendimento da Impar Imóveis. "
            "Analise a conversa do Facebook Messenger e retorne APENAS JSON válido.\n\n"
            "Regras:\n"
            "1. Telefone/WhatsApp em qualquer mensagem → acao: CAPTUROU_CONTATO, telefone em dígitos.\n"
            "2. Última mensagem nossa + lead não respondeu depois → acao: SEM_ACAO.\n"
            "3. Lead respondeu sem telefone → acao: PEDIR_CONTATO.\n"
            "4. Sem resposta nova → acao: SEM_ACAO.\n\n"
            "Formato: {\"acao\": \"CAPTUROU_CONTATO|PEDIR_CONTATO|SEM_ACAO\", \"telefone\": \"digitos ou null\"}"
        )
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": f"Lead: {nome}\nPreview: {preview}\n\n{conv_text[-3000:]}"}],
            response_format={"type": "json_object"}, temperature=0
        )
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return analisar_com_regras(conv_text, nome, preview)


def run():
    from playwright.sync_api import sync_playwright

    ts         = datetime.now().strftime('%Y-%m-%d %H:%M')
    stats      = {'v':0,'r':0,'t':0,'p':0,'e':0}
    leads      = []
    known      = load_known_phones()
    notificados = load_notified_today()
    phone2name = load_phones_to_names()

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=True,
            viewport={"width": 1280, "height": 900},
            args=["--no-sandbox","--disable-dev-shm-usage"],
        )
        page = ctx.new_page()

        print(f"→ Acessando inbox ({ts})...")
        page.goto(INBOX_URL, wait_until="domcontentloaded", timeout=25000)

        # Verificar login
        try:
            page.wait_for_selector('div[role="button"]', timeout=15000)
        except Exception:
            url = page.url
            ctx.close()
            status = "LOGIN_EXPIRADO" if 'login' in url else "INBOX_VAZIA"
            update_log(stats, leads, status, ts)
            return status

        # Verificar se está na página do inbox (não login)
        if 'login' in page.url or 'checkpoint' in page.url:
            ctx.close()
            update_log(stats, leads, "LOGIN_EXPIRADO", ts)
            return "LOGIN_EXPIRADO"

        time.sleep(6)

        # Detectar bloqueio temporário do marketplace/inbox
        MESSAGES_URL = "https://www.facebook.com/messages/"
        effective_base = INBOX_URL
        messages_mode = False
        thread_urls = []   # usado apenas em messages_mode

        cur_url = page.url
        body_text = page.inner_text('body') if page.query_selector('body') else ''
        # Bloqueio: texto explícito na página OU redirecionamento para fora do marketplace
        is_blocked = ('bloqueado temporariamente' in body_text
                      or 'bloqueamos temporariamente' in body_text.lower()
                      or ('marketplace/inbox' not in cur_url and 'marketplace' not in cur_url))
        if is_blocked:
            print(f"  ⚠ marketplace/inbox bloqueado — fallback messages/ (url={cur_url[-50:]})")
            # Forçar navegação real (não React router) para carregar o sidebar do inbox
            page.evaluate(f"window.location.replace('{MESSAGES_URL}')")
            try:
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            except Exception:
                pass
            # Aguardar sidebar de threads aparecer (a[href*="/messages/t/"] ou [role="row"])
            try:
                page.wait_for_selector('a[href*="/messages/t/"], [role="row"]', timeout=10000)
            except Exception:
                pass
            time.sleep(3)
            effective_base = MESSAGES_URL
            messages_mode = True
            via_marketplace_indicator = False

            # Tentar clicar no indicador "MarketplaceMensagem não lida" para filtrar view
            try:
                mp_nav = page.evaluate("""
                () => {
                    for (const el of document.querySelectorAll('[role="button"], a, div[tabindex]')) {
                        const t = (el.innerText || '').trim();
                        if (t.toLowerCase().includes('mensagem não lida') && t.toLowerCase().includes('marketplace')) {
                            el.click(); return t.slice(0, 60);
                        }
                        if (t.toLowerCase().includes('marketplace') && t.toLowerCase().includes('não lida')) {
                            el.click(); return t.slice(0, 60);
                        }
                    }
                    return null;
                }
                """)
                if mp_nav:
                    print(f"  → Indicador marketplace clicado: '{mp_nav[:50]}'")
                    time.sleep(4)
                    via_marketplace_indicator = True
                    effective_base = page.url  # atualizar base após filtro
            except Exception as _e:
                print(f"  [WARN] Indicador marketplace: {_e}")

            # Extrair links de thread diretamente do DOM (sidebar esquerdo x<500)
            raw_links = page.evaluate("""
            () => {
                const seen = new Set();
                const results = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.href || '';
                    if (!href.includes('/messages/t/') && !href.includes('/messages/e2ee/t/')) return;
                    const bb = a.getBoundingClientRect();
                    if (bb.x > 500 || bb.y < 150 || bb.width < 80) return;
                    if (seen.has(href)) return;
                    seen.add(href);
                    const lines = (a.innerText || '').trim().split('\\n').filter(Boolean);
                    results.push({
                        url: href,
                        text: lines[0] || 'Lead',
                        preview: lines[lines.length - 1] || '',
                        y: bb.y
                    });
                });
                return results;
            }
            """)
            # Filtrar threads onde o preview já tem resposta nossa
            thread_urls = [l for l in raw_links
                           if not any(p in l.get('preview', '') for p in NOSSAS_FRASES)]
            print(f"  Threads messages/ detectadas: {len(thread_urls)}")

            # Fallback secundário: raw_links encontrou 0 → tentar get_unique_threads
            if not thread_urls:
                gt = get_unique_threads(page, messages_mode=True)
                print(f"  Threads get_unique_threads (fallback): {len(gt)}")
                thread_urls = [{'url': None, 'text': t['text'], 'preview': t.get('preview', ''),
                                'cx': t.get('cx', 300), 'cy': t.get('cy', t['y']), 'y': t['y']}
                               for t in gt]

            # Fallback terciário: clicar no indicador "MarketplaceMensagem não lida"
            if not thread_urls:
                print(f"  → Tentando acesso via indicador de não lidas do Marketplace...")
                mp_indicator_url = page.evaluate("""
                () => {
                    // Buscar link de conversa marketplace não lida no DOM
                    for (const el of document.querySelectorAll('a[href], [role="link"]')) {
                        const href = el.href || el.getAttribute('href') || '';
                        const txt = (el.innerText || '').trim().toLowerCase();
                        if ((href.includes('/marketplace/') || txt.includes('marketplace')) && txt.includes('não lida'))
                            return href || null;
                    }
                    // Fallback: clicar no botão de indicador
                    for (const el of document.querySelectorAll('[role="button"]')) {
                        const t = (el.innerText || '').trim();
                        if (t.toLowerCase().includes('mensagem não lida') && t.toLowerCase().includes('marketplace')) {
                            el.click(); return '__clicked__';
                        }
                    }
                    return null;
                }
                """)
                if mp_indicator_url and mp_indicator_url != '__clicked__':
                    page.goto(mp_indicator_url, wait_until="domcontentloaded", timeout=20000)
                    time.sleep(5)
                    thread_urls = [{'url': mp_indicator_url, 'text': 'Lead Marketplace', 'preview': ''}]
                    print(f"  → URL direta marketplace: {mp_indicator_url[-60:]}")
                elif mp_indicator_url == '__clicked__':
                    time.sleep(5)
                    # Agora estamos na conversa — processar diretamente
                    cur_after = page.url
                    thread_urls = [{'url': cur_after, 'text': 'Lead Marketplace', 'preview': ''}]
                    print(f"  → Indicador clicado, url: {cur_after[-60:]}")

            # Processar cada thread por URL direta
            for turl in thread_urls:
                nome = turl['text'].split()[0] if turl['text'] else 'Lead'
                print(f"\n  → {nome} (messages/t)")
                stats['v'] += 1
                try:
                    if turl.get('url'):
                        page.goto(turl['url'], wait_until="domcontentloaded", timeout=20000)
                    else:
                        clicked = click_thread(page, turl['text'])
                        if not clicked:
                            page.mouse.click(turl.get('cx', 300), turl.get('cy', turl['y']))
                    time.sleep(5)  # 5s para carregamento assíncrono do link do item

                    nome_real = get_conv_nome(page)
                    _INBOX_HEADS = {'conversas','marketplace','inbox','mensagens','messages','messenger','bate-papo','chats','selecione'}
                    if nome_real and any(w in nome_real.lower() for w in _INBOX_HEADS):
                        nome_real = None
                    if nome_real:
                        nome = nome_real
                    # Se nome ainda é placeholder, retry com 2s de espera
                    if not nome or nome == 'Lead':
                        time.sleep(2)
                        nome_retry = get_conv_nome(page)
                        if nome_retry and not any(w in nome_retry.lower() for w in _INBOX_HEADS):
                            nome = nome_retry
                    if not nome:
                        nome = 'Interessado(a)'

                    # Guard obrigatório: só processar se for conversa do Marketplace
                    # Se viemos do indicador de marketplace no messages/, confiar no filtro de origem
                    mp_ok = is_marketplace_conv(page)
                    if not mp_ok and not via_marketplace_indicator:
                        print(f"    ⏭ Não é Marketplace (is_marketplace=False) — pulando")
                        stats['p'] += 1
                        page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                        time.sleep(2)
                        continue
                    if not mp_ok and via_marketplace_indicator:
                        print(f"    ⚠ Link item não encontrado (via indicador marketplace — processando mesmo assim)")

                    conv_text = get_conv_text(page)
                    if len(conv_text.strip()) < 20:
                        print(f"    ⚠ Conversa não carregou — pulando")
                        stats['e'] += 1
                        continue

                    link = get_listing_url(page)
                    if not link:
                        time.sleep(2)
                        link = get_listing_url(page)
                    if link:
                        print(f"    🔗 Link: {link}")
                    else:
                        print(f"    ⚠ Link do anúncio não encontrado")
                    imovel = extract_imovel(conv_text)

                    resultado_ia = analisar_com_regras(conv_text, nome, turl.get('preview', ''))
                    acao_ia = resultado_ia.get('acao', 'SEM_ACAO')
                    telefone_ia = resultado_ia.get('telefone')
                    if telefone_ia:
                        telefone_ia = re.sub(r'[^\d]', '', str(telefone_ia))
                        if len(telefone_ia) < 8: telefone_ia = None
                        elif len(telefone_ia) in (8, 9): telefone_ia = '47' + telefone_ia
                    print(f"    🤖 IA → {acao_ia}{' / tel: ' + telefone_ia if telefone_ia else ''}")

                    if acao_ia == 'CAPTUROU_CONTATO' and telefone_ia:
                        if telefone_ia in known:
                            if telefone_ia not in notificados:
                                ok = notificar_jonata(nome, telefone_ia, imovel, link or '')
                                if ok:
                                    mark_notified(notificados, telefone_ia)
                                    print(f"    ↳ {telefone_ia} já no CSV — notificando grupo (1ª vez hoje)")
                                else:
                                    print(f"    ↳ {telefone_ia} já no CSV — falha no envio, será tentado novamente")
                            else:
                                print(f"    ↳ {telefone_ia} já no CSV e já notificado hoje — pulando")
                            stats['p'] += 1
                        else:
                            sent = send_message(page, "Obrigado, vamos entrar em contato via whatsapp.")
                            if sent:
                                stats['r'] += 1
                                print(f"    ✓ Agradecimento enviado — {telefone_ia}")
                            append_lead(nome, telefone_ia, imovel, link or '', 'Messenger IA')
                            known.add(telefone_ia)
                            leads.append({'nome': nome, 'telefone': telefone_ia, 'imovel': imovel})
                            stats['t'] += 1
                            ok = notificar_jonata(nome, telefone_ia, imovel, link or '')
                            if ok:
                                mark_notified(notificados, telefone_ia)
                    elif acao_ia == 'PEDIR_CONTATO':
                        resp = "Certo, vou atualizar essa informação e retorno.\nQual seu whatsapp para retorno ?"
                        sent = send_message(page, resp)
                        if sent:
                            stats['r'] += 1
                            print(f"    ✓ Pedido WhatsApp enviado")
                        else:
                            stats['e'] += 1
                    else:
                        print(f"    ↳ SEM_ACAO")
                        stats['p'] += 1

                except Exception as e:
                    print(f"    ⚠ Erro em {nome}: {e}")
                    stats['e'] += 1

            # Encerrar após processar todas as threads em messages_mode
            ctx.close()
            update_log(stats, leads, "OK", ts)
            print(f"\n📊 Status: OK (messages/ fallback)")
            print(f"✅ Log atualizado.")
            return "OK"

        # Coletar threads únicas (modo normal marketplace/inbox)
        threads = get_unique_threads(page)

        # Detectar se carregou browse mode em vez de inbox (ex: filtro de localização visível)
        if not threads:
            in_browse_mode = page.evaluate("""
            () => {
                const btns = Array.from(document.querySelectorAll('[role="button"]'));
                return btns.some(b => {
                    const t = (b.innerText||'').trim();
                    return t.includes('km') || t.includes(' · No raio') || t.includes('Localização');
                });
            }
            """)
            if in_browse_mode:
                print(f"  ⚠ Browse mode detectado — navegando para inbox")
                page.evaluate(f"window.location.replace('{INBOX_URL}')")
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=20000)
                except Exception:
                    pass
                time.sleep(6)
                threads = get_unique_threads(page)
                # Se ainda vazio após navegação → forçar fallback messages/
                if not threads:
                    print(f"  ⚠ Inbox ainda vazio após navegação — forçando fallback messages/")
                    page.evaluate(f"window.location.replace('{MESSAGES_URL}')")
                    try:
                        page.wait_for_load_state("domcontentloaded", timeout=15000)
                    except Exception:
                        pass
                    time.sleep(4)
                    effective_base = MESSAGES_URL
                    messages_mode = True
                    try:
                        page.wait_for_selector('a[href*="/messages/t/"], [role="row"]', timeout=8000)
                    except Exception:
                        pass
                    time.sleep(2)
                    raw_links = page.evaluate("""
                    () => {
                        const seen = new Set();
                        const results = [];
                        document.querySelectorAll('a[href]').forEach(a => {
                            const href = a.href || '';
                            if (!href.includes('/messages/t/') && !href.includes('/messages/e2ee/t/')) return;
                            const bb = a.getBoundingClientRect();
                            if (bb.x > 500 || bb.y < 150 || bb.width < 80) return;
                            if (seen.has(href)) return;
                            seen.add(href);
                            const lines = (a.innerText || '').trim().split('\\n').filter(Boolean);
                            results.push({
                                text: lines[0] || 'Lead',
                                preview: lines[lines.length - 1] || '',
                                url: href,
                                cx: bb.x + bb.width / 2,
                                cy: bb.y + bb.height / 2,
                                y: bb.y
                            });
                        });
                        return results;
                    }
                    """)
                    NOSSAS_FRASES_LOCAL = ["Certo, vou atualizar", "Obrigado, vamos entrar em contato",
                                           "Qual seu whatsapp para retorno", "Recebi seu n",
                                           "Vou verificar com o corretor"]
                    threads = [t for t in raw_links
                               if not any(p in t.get('preview', '') for p in NOSSAS_FRASES_LOCAL)]
                    print(f"  Threads messages/ (fallback Browse): {len(threads)}")

        # Se inbox em estado de erro (Recarregar), clicar e tentar de novo
        if not threads:
            try:
                recarregado = page.evaluate("""
                () => {
                    for (const btn of document.querySelectorAll('[role="button"]')) {
                        const t = (btn.innerText || '').trim().toLowerCase();
                        if (t === 'recarregar' || t === 'reload' || t === 'tentar novamente') {
                            btn.click(); return true;
                        }
                    }
                    return false;
                }
                """)
                if recarregado:
                    print(f"  ⚠ Inbox em estado de erro — Recarregar clicado, aguardando...")
                    time.sleep(7)
                    threads = get_unique_threads(page)
            except Exception:
                pass

        # Fase 0: threads com telefone visível no preview (captura imediata)
        phone_threads = page.evaluate(f"""
        () => {{
            const re = /(?:\\+?55\\s?)?(?:\\(?\\d{{2}}\\)?\\s?)?\\d{{4,5}}[-\\s]?\\d{{4}}/g;
            const results = [];
            document.querySelectorAll('span').forEach(s => {{
                const t = s.textContent.trim();
                if (re.test(t) && t.length < 30) {{
                    const r = s.getBoundingClientRect();
                    if (r.y > 100 && r.y < 900 && r.width > 30) {{
                        results.push({{text: t, x: r.x, y: r.y, type: 'phone_preview'}});
                    }}
                }}
            }});
            return results;
        }}
        """)
        # Adicionar phone_threads se não duplicar Y com threads existentes
        seen_y = [t['y'] for t in threads]
        for pt in phone_threads:
            too_close = any(abs(pt['y'] - sy) < 30 for sy in seen_y)
            if not too_close:
                threads.append(pt)
                seen_y.append(pt['y'])

        print(f"  Threads não lidas detectadas: {len(threads)}")

        for thread in threads:
            nome = get_nome(thread['text'])
            print(f"\n  → {nome} (y={thread['y']:.0f})")
            stats['v'] += 1

            try:
                # Navegar por URL direta (messages/ fallback) ou clicar via DOM
                if messages_mode and thread.get('url'):
                    page.goto(thread['url'], wait_until="domcontentloaded", timeout=20000)
                else:
                    clicked = click_thread(page, thread['text'])
                    if not clicked:
                        page.mouse.click(thread.get('cx', 700), thread.get('cy', thread['y']))
                time.sleep(1.5)

                # Aguardar input de mensagem aparecer (confirma que conversa abriu)
                conv_open = wait_for_conversation_open(page, timeout=10, base_url=effective_base)
                if not conv_open:
                    cur_url = page.url
                    has_ce = bool(page.query_selector('div[contenteditable="true"]'))
                    has_log = bool(page.query_selector('[role="log"]'))
                    print(f"    ⚠ Conversa não abriu | ce={has_ce} | log={has_log} | url={cur_url[-60:]}")
                    stats['e'] += 1
                    page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(2)
                    if messages_mode:
                        page.evaluate("""
                        () => { const rows = document.querySelectorAll('[role="row"]');
                                for (const r of rows) { if (r.textContent.includes('Marketplace')) { r.click(); break; } } }
                        """)
                        time.sleep(1.5)
                    continue

                time.sleep(2)

                # Verificar nome real da conversa aberta (evita processar conversa errada)
                nome_real = get_conv_nome(page)
                # Filtro extra: headings do inbox não são nomes de lead
                _INBOX_HEADS = {'conversas', 'marketplace', 'inbox', 'mensagens',
                                'messages', 'messenger', 'bate-papo', 'chats', 'selecione'}
                if nome_real and any(w in nome_real.lower() for w in _INBOX_HEADS):
                    nome_real = None

                # Detectar bloqueio temporário do Facebook mid-loop
                if nome_real and 'bloqueado temporariamente' in nome_real.lower():
                    print(f"    ⛔ Facebook bloqueou temporariamente — encerrando rodada para não acumular restrições")
                    ctx.close()
                    update_log(stats, leads, "OK", ts)
                    print(f"\n📊 Status: OK (interrompido por bloqueio FB)")
                    print(f"✅ Log atualizado.")
                    return "OK"

                nome_esperado_first = nome.split()[0].lower()
                if nome_real and nome_esperado_first not in nome_real.lower():
                    print(f"    ⚠ Conversa errada abriu: esperado '{nome}', abriu '{nome_real}' — pulando")
                    stats['e'] += 1
                    page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(3)
                    if messages_mode:
                        page.evaluate("""() => { const rows = document.querySelectorAll('[role="row"]'); for (const r of rows) { if (r.textContent.includes('Marketplace')) { r.click(); break; } } }""")
                        time.sleep(1.5)
                    continue

                # Usar nome real da conversa se disponível (mais preciso que o sidebar)
                if nome_real:
                    nome = nome_real
                # Se nome ainda é placeholder, retry com 2s de espera
                if not nome or nome == 'Lead':
                    time.sleep(2)
                    nome_retry = get_conv_nome(page)
                    if nome_retry and not any(w in nome_retry.lower() for w in _INBOX_HEADS):
                        nome = nome_retry
                if not nome:
                    nome = 'Interessado(a)'

                # Guard obrigatório: só processar se for conversa do Marketplace
                if not is_marketplace_conv(page):
                    print(f"    ⏭ Não é Marketplace (is_marketplace=False) — pulando")
                    stats['p'] += 1
                    page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(2)
                    continue

                conv_text = get_conv_text(page)
                link = get_listing_url(page)
                if not link:
                    time.sleep(2)
                    link = get_listing_url(page)
                imovel = extract_imovel(conv_text) if not link else (
                    'Sala Comercial' if 'sala' in (link + conv_text).lower()
                    else ('Casa' if 'casa' in (link + conv_text).lower()
                    else ('Terreno' if 'terreno' in (link + conv_text).lower()
                    else ('Kitnet' if 'kitnet' in (link + conv_text).lower()
                    else extract_imovel(conv_text)))))

                # Guard: conv_text muito curto indica falha de leitura da conversa
                if len(conv_text.strip()) < 20:
                    print(f"    ⚠ Conversa não carregou ({len(conv_text)} chars) — pulando")
                    stats['e'] += 1
                    page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(3)
                    if messages_mode:
                        page.evaluate("""() => { const rows = document.querySelectorAll('[role="row"]'); for (const r of rows) { if (r.textContent.includes('Marketplace')) { r.click(); break; } } }""")
                        time.sleep(1.5)
                    continue

                resultado_ia = analisar_com_regras(conv_text, nome, thread.get('preview', ''))
                acao_ia = resultado_ia.get('acao', 'SEM_ACAO')
                telefone_ia = resultado_ia.get('telefone')
                if telefone_ia:
                    telefone_ia = re.sub(r'[^\d]', '', str(telefone_ia))
                    if len(telefone_ia) < 8:
                        telefone_ia = None
                    elif len(telefone_ia) in (8, 9):
                        telefone_ia = '47' + telefone_ia
                print(f"    🤖 IA → {acao_ia}{' / tel: ' + telefone_ia if telefone_ia else ''}")

                if acao_ia == 'CAPTUROU_CONTATO' and telefone_ia:
                    if telefone_ia in known:
                        if telefone_ia not in notificados:
                            ok = notificar_jonata(nome, telefone_ia, imovel, link)
                            if ok:
                                mark_notified(notificados, telefone_ia)
                                print(f"    ↳ Telefone {telefone_ia} já no CSV — notificando grupo (1ª vez hoje)")
                            else:
                                print(f"    ↳ Telefone {telefone_ia} já no CSV — falha no envio, será tentado novamente")
                        else:
                            print(f"    ↳ Telefone {telefone_ia} já no CSV e já notificado hoje — pulando")
                        stats['p'] += 1
                    else:
                        link = link or ''
                        resp = "Obrigado, vamos entrar em contato via whatsapp."
                        sent = send_message(page, resp)
                        if sent:
                            stats['r'] += 1
                            print(f"    ✓ Agradecimento enviado — {telefone_ia}")
                        append_lead(nome, telefone_ia, imovel, link, 'Messenger IA')
                        known.add(telefone_ia)
                        leads.append({'nome': nome, 'telefone': telefone_ia, 'imovel': imovel})
                        stats['t'] += 1
                        ok = notificar_jonata(nome, telefone_ia, imovel, link)
                        if ok:
                            mark_notified(notificados, telefone_ia)

                elif acao_ia == 'PEDIR_CONTATO':
                    resp = "Certo, vou atualizar essa informação e retorno.\nQual seu whatsapp para retorno ?"
                    sent = send_message(page, resp)
                    if sent:
                        stats['r'] += 1
                        print(f"    ✓ Pedido WhatsApp enviado")
                    else:
                        stats['e'] += 1
                        print(f"    ⚠ Falha ao enviar")

                else:
                    print(f"    ↳ SEM_ACAO — aguardando resposta do lead")
                    stats['p'] += 1

                # Voltar ao inbox via navigate (mais limpo que go_back)
                page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                time.sleep(2)
                if messages_mode:
                    page.evaluate("""() => { const rows = document.querySelectorAll('[role="row"]'); for (const r of rows) { if (r.textContent.includes('Marketplace')) { r.click(); break; } } }""")
                    time.sleep(1.5)

            except Exception as e:
                print(f"    ⚠ Erro em {nome}: {e}")
                stats['e'] += 1
                try:
                    page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(3)
                    if messages_mode:
                        page.evaluate("""() => { const rows = document.querySelectorAll('[role="row"]'); for (const r of rows) { if (r.textContent.includes('Marketplace')) { r.click(); break; } } }""")
                        time.sleep(1.5)
                except Exception: pass

        # Fase 2 removida — a IA detecta telefones diretamente na conversa aberta

        ctx.close()

    update_log(stats, leads, "OK", ts)
    return "OK"


if __name__ == "__main__":
    import fcntl, os as _os
    LOCK_PATH = Path.home() / ".local/impar-automation/messenger/.varredura.lock"
    try:
        lock_fd = open(LOCK_PATH, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("⏳ Outra instância da varredura está rodando — saindo.")
        sys.exit(0)

    _sync_notif_script()
    _sync_csv_from_icloud()
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"\n🔍 Varredura Messenger v3 — {ts}")
    print("=" * 60)
    try:
        status = run()
        print(f"\n📊 Status: {status}")
        print("✅ Log atualizado.")
    except Exception as e:
        import traceback; traceback.print_exc()
        ts2 = datetime.now().strftime('%Y-%m-%d %H:%M')
        entry = f"\n## {ts2} -03 — ⛔ ERRO FATAL\n\n{e}\n\n---\n"
        txt = LOG_PATH.read_text(encoding='utf-8') if LOG_PATH.exists() else "# Log\n"
        cut = txt.find('\n\n')
        LOG_PATH.write_text((txt[:cut+2]+entry+txt[cut+2:]) if cut != -1 else txt+entry, encoding='utf-8')
        sys.exit(1)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()
