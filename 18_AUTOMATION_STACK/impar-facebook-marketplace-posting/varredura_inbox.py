#!/usr/bin/env python3
"""
Varredura Messenger Marketplace v3 — Impar Imóveis.
Correções: deduplicação por Y, press_sequentially para input, verificação de envio por screenshot.
"""
import csv, json, os, re, shutil, subprocess, sys, time, unicodedata
from datetime import datetime
from pathlib import Path
from openai import OpenAI

PROFILE    = Path("/Users/usuario/.local/impar-automation/messenger/browser-profile")
CSV_PATH   = Path("/Users/usuario/.local/impar-automation/messenger/leads_marketplace_captura.csv")
CSV_ICLOUD = Path("/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/leads_marketplace_captura.csv")
LOG_PATH   = Path("/Users/usuario/.local/impar-automation/messenger/messenger-rodadas.md")
JONATA_WA  = "554796876631"
INBOX_URL  = "https://www.facebook.com/marketplace/inbox/"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"
ACCOUNT_ID = os.environ.get("IMPAR_ACCOUNT_ID", "jonata")
PHONE_RE  = re.compile(
    r'(?:\+?55[\s.\-]?)?'        # +55 opcional
    r'(?:\(?\d{2}\)?[\s.\-]?)?'  # DDD opcional
    r'(?:9[\s.\-]?)?'            # 9º dígito móvel com possível espaço
    r'\d{4}[\s.\-]?\d{4}'        # 8 dígitos principais
)

NOTIF_ICLOUD     = Path("/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/notificar_lead_whatsapp.py")
NOTIF_LOCAL      = Path.home() / ".local/impar-automation/messenger/notificar_lead_whatsapp.py"
NOTIFICADOS_PATH = Path.home() / ".local/impar-automation/messenger/notificados-varredura.json"
PENDING_NOTIF    = Path.home() / ".local/impar-automation/messenger/pending-notif.json"

def _sync_notif_script():
    """Copia notificar_lead_whatsapp.py do iCloud → local se iCloud for mais novo."""
    try:
        if NOTIF_ICLOUD.exists():
            if not NOTIF_LOCAL.exists() or NOTIF_ICLOUD.stat().st_mtime > NOTIF_LOCAL.stat().st_mtime:
                shutil.copy2(NOTIF_ICLOUD, NOTIF_LOCAL)
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

def _sync_csv_to_gsheet():
    """Espelha o CSV local na planilha do Google Drive (leads_marketplace_captura).
    Sobrescreve a planilha inteira com o conteúdo do CSV — idempotente. Falha silenciosa."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from sheets_gdrive import LEADS_SHEET_ID, get_token, upload_rows
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            rows = [r for r in csv.reader(f) if r]
        if not rows:
            return
        upload_rows(LEADS_SHEET_ID, rows, get_token())
        print(f"    📊 Planilha Google Drive atualizada ({len(rows)} linhas)")
    except Exception as e:
        print(f"    ⚠ sync planilha Google Drive falhou: {e}")

def _append_lead_to_gsheet(nome, telefone, tipo, link, obs, data_captura):
    """Adiciona apenas o lead novo ao Google Sheet, sem sobrescrever a planilha inteira."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from sheets_gdrive import LEADS_SHEET_ID, get_token, append_dict
        append_dict(LEADS_SHEET_ID, {
            'Nome': nome,
            'Telefone': telefone,
            'Tipo Imóvel': tipo,
            'Link': link,
            'Bairro': '',
            'Status': 'novo',
            'Data': data_captura,
            'Fonte': f'Messenger Marketplace/{ACCOUNT_ID}',
            'Observações': obs,
        }, get_token())
        print("    📊 Lead adicionado ao Google Sheet")
    except Exception as e:
        print(f"    ⚠ append planilha Google Drive falhou: {e}")

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

def load_pending_notif() -> list:
    if not PENDING_NOTIF.exists():
        return []
    try:
        return json.loads(PENDING_NOTIF.read_text())
    except Exception:
        return []

def add_pending_notif(nome: str, telefone: str, imovel: str, link: str):
    items = load_pending_notif()
    if not any(i.get('telefone') == telefone for i in items):
        items.append({'nome': nome, 'telefone': telefone, 'imovel': imovel,
                      'link': link, 'ts': datetime.now().isoformat()})
        PENDING_NOTIF.write_text(json.dumps(items, ensure_ascii=False, indent=2))

def retry_pending_notif():
    items = load_pending_notif()
    if not items:
        return
    remaining = []
    notif_script = NOTIF_LOCAL
    for item in items:
        stored_link = item.get('link', '')
        if stored_link and not stored_link.startswith('https://'):
            print(f"  ⚠ Renotificação descartada para '{item['nome']}': link inválido ('{stored_link[:60]}')")
            continue
        print(f"  🔄 Renotificando pendente: {item['nome']} / {item['telefone']}")
        try:
            result = subprocess.run(
                [sys.executable, str(notif_script),
                 '--nome', item['nome'], '--telefone', item['telefone'],
                 '--resumo', item.get('imovel', ''),
                 '--link-imovel', stored_link,
                 '--origem', 'marketplace'],
                timeout=60
            )
            if result.returncode == 0:
                print(f"    ✅ Renotificação OK: {item['nome']}")
            else:
                print(f"    ⚠ Renotificação falhou — mantendo na fila")
                remaining.append(item)
        except Exception as e:
            print(f"    ⚠ Renotificação erro: {e} — mantendo na fila")
            remaining.append(item)
    PENDING_NOTIF.write_text(json.dumps(remaining, ensure_ascii=False, indent=2))

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
    data_captura = datetime.now().strftime('%Y-%m-%d %H:%M')
    exists = CSV_PATH.exists()
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        w.writerow([nome, telefone, tipo, link, '', 'novo',
                    data_captura,
                    'Messenger Marketplace', obs])
    _sync_csv_to_icloud()
    _append_lead_to_gsheet(nome, telefone, tipo, link, obs, data_captura)

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

GRUPO_LEADS = "NOVOS LEADS"

def notificar_jonata(nome, telefone, imovel, link_anuncio):
    """Envia alerta via notificar_lead_whatsapp.py (método CGEvent validado + formato correto)."""
    notif_script = NOTIF_LOCAL
    try:
        result = subprocess.run(
            [sys.executable, str(notif_script),
             '--nome', nome,
             '--telefone', telefone,
             '--resumo', imovel,
             '--link-imovel', link_anuncio or '',
             '--origem', 'marketplace',
             '--account-id', ACCOUNT_ID],
            timeout=60
        )
        if result.returncode == 0:
            print(f"    📱 Grupo '{GRUPO_LEADS}' notificado: {nome} / {telefone}")
        else:
            print(f"    ⚠ notificar_jonata: exit {result.returncode} — adicionando à fila de pendentes")
            add_pending_notif(nome, telefone, imovel, link_anuncio or '')
    except Exception as e:
        print(f"    ⚠ notificar_jonata: {e} — adicionando à fila de pendentes")
        add_pending_notif(nome, telefone, imovel, link_anuncio or '')

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
    "Vou verificar essa informação",
    "Obrigado, vou entrar em contato",
    "Obrigado, vamos entrar em contato",
    "Qual seu whatsapp para retorno",
    "Recebi seu n",
    "Vou verificar com o corretor",
    "reagiu com",          # reação a uma mensagem nossa — não é pergunta
    "Aqui é a Impar Imóveis",
    "Vi que você demonstrou interesse",
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
                'recarregar', 'reload', 'tentar novamente', 'tentar de novo'}

    x_min = 60 if messages_mode else 300
    x_max = 450 if messages_mode else 9999

    raw = page.evaluate(f"""
    () => {{
        const x_min = {x_min}, x_max = {x_max};
        const byName = {{}};

        // Guarda mantendo sempre a linha mais ao topo (threads pendentes ficam em cima)
        const guardar = (nome, lines, txt, bb, href) => {{
            if (byName[nome] && byName[nome].y <= bb.y) return;
            byName[nome] = {{
                nome, lines, txt: txt.slice(0, 300),
                cx: Math.round(bb.x + bb.width / 2),
                cy: Math.round(bb.y + bb.height / 2),
                y: bb.y, url: href
            }};
        }};

        // Detector principal: a UI atual do Facebook não usa mais <a href> nas
        // linhas do inbox — são divs. Cada linha tem uma sublinha que começa
        // com "·" (o anúncio ao qual a conversa se refere).
        document.querySelectorAll('div').forEach(el => {{
            const bb = el.getBoundingClientRect();
            if (bb.width < 350) return;
            if (bb.x < x_min || bb.x > x_max) return;
            if (bb.height < 45 || bb.height > 115) return;
            if (bb.y < 150) return;
            const txt = (el.innerText || '').trim();
            if (txt.length < 8 || txt.length > 600) return;
            const lines = txt.split('\\n').map(s => s.trim()).filter(Boolean);
            if (lines.length < 2) return;
            if (!lines.some(l => l.startsWith('·'))) return;
            const nome = lines[0] || '';
            if (!nome || nome.length > 60 || nome.startsWith('·')) return;
            guardar(nome, lines, txt, bb, '');
        }});

        // Fallback 1: layouts antigos com link direto para o thread
        document.querySelectorAll('a[href*="/marketplace/inbox/"]').forEach(el => {{
            const bb = el.getBoundingClientRect();
            if (bb.width < 100 || bb.height < 20 || bb.height > 120) return;
            if (bb.x < x_min || bb.x > x_max) return;
            if (bb.y < 160) return;
            const txt = (el.innerText || '').trim();
            if (txt.length < 3 || txt.length > 500) return;
            const lines = txt.split('\\n').map(s => s.trim()).filter(Boolean);
            const nome = lines[0] || '';
            if (!nome || nome.length > 40 || nome.startsWith('·')) return;
            guardar(nome, lines, txt, bb, el.href || '');
        }});

        // Fallback 2: qualquer div/a na área de threads (layout /messages/)
        document.querySelectorAll('div, a').forEach(el => {{
            const bb = el.getBoundingClientRect();
            if (bb.width < 200 || bb.height < 20 || bb.height > 120) return;
            if (bb.x < x_min || bb.x > x_max) return;
            if (bb.y < 160) return;
            const txt = (el.innerText || '').trim();
            if (txt.length < 3 || txt.length > 500) return;
            const lines = txt.split('\\n').map(s => s.trim()).filter(Boolean);
            const nome = lines[0] || '';
            if (!nome || nome.length > 40 || nome.startsWith('·')) return;
            if (byName[nome]) return;  // já detectado com mais precisão acima
            guardar(nome, lines, txt, bb, (el.tagName === 'A') ? (el.href || '') : '');
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
        if nome_lower in UI_WORDS or nome_lower[:3] == 'voc' \
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
                           'url': t.get('url', ''),
                           'cx': t['cx'], 'cy': t['cy'], 'y': t['cy']})

    return unique

def get_nome(text):
    return text.split()[0] if text else ""

def click_thread(page, nome_full, coords=None):
    """
    v5 — prioriza a coordenada já calculada por get_unique_threads().

    Buscar por texto (:has-text) casa com qualquer ancestral que contenha o
    nome, incluindo itens do painel de notificações — era isso que abria
    "Anteriores" no lugar da conversa. A coordenada da linha é inequívoca.
    """
    nome_first = nome_full.split()[0]

    # Strategy 0: clique direto na coordenada da linha detectada
    if coords:
        try:
            page.mouse.click(coords[0], coords[1])
            return True
        except Exception:
            pass

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
    """Lê apenas o log de mensagens do painel de conversa aberto (direita, x>380).

    BUG histórico: page.query_selector('[role="log"]') pega o PRIMEIRO elemento
    com esse role no DOM, que pode ser a lista de threads da sidebar (que também
    usa role="log" ou acaba tendo texto >20 chars) — isso misturava mensagens de
    vários leads diferentes no mesmo texto e causava falsos SEM_ACAO (frase nossa
    de OUTRO lead "casava" no last_block deste). A busca agora é geométrica:
    só aceita candidatos com bb.x > 380 (fora da sidebar esquerda).
    """
    try:
        text = page.evaluate("""
        () => {
            const clean = (s) => (s || '')
                .replace(/\\n{3,}/g, '\\n\\n')
                .trim();
            const visible = (el) => {
                const bb = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return bb.width > 0 && bb.height > 0
                    && style.visibility !== 'hidden'
                    && style.display !== 'none';
            };
            const looksLikeConversation = (txt) => {
                const low = txt.toLowerCase();
                return txt.length >= 20 && (
                    low.includes('mensagem enviada') ||
                    low.includes('message sent') ||
                    low.includes('pressione enter') ||
                    low.includes('press enter') ||
                    low.includes('está disponível') ||
                    low.includes('esta disponível') ||
                    low.includes('is this available') ||
                    low.includes('disponivel') ||
                    low.includes('disponível') ||
                    low.includes('boa tarde') ||
                    low.includes('bom dia') ||
                    low.includes('boa noite') ||
                    low.includes('whatsapp') ||
                    low.includes('telefone') ||
                    low.includes('interesse') ||
                    low.includes('imóvel') ||
                    low.includes('imovel') ||
                    low.includes('aluguel') ||
                    low.includes('alugar') ||
                    low.includes('venda') ||
                    low.includes('valor') ||
                    low.includes('contato') ||
                    low.includes('visita') ||
                    low.includes('enviar') ||
                    low.includes('obrigad')
                );
            };

            const sels = [
                '[role="log"]',
                '[aria-label="Conversa"]',
                '[aria-label="Conversation"]',
                '[aria-label*="essage"]',
                '[aria-label*="ensage"]',
                '[data-testid="message-container"]'
            ];
            let best = '';

            // Pass 1: strict — requer keywords de conversa
            for (const sel of sels) {
                for (const el of document.querySelectorAll(sel)) {
                    const bb = el.getBoundingClientRect();
                    if (bb.x < 300 || bb.width < 200 || bb.height < 60) continue;
                    if (!visible(el)) continue;
                    const t = clean(el.innerText || el.textContent || '');
                    if (looksLikeConversation(t) && t.length > best.length) best = t;
                }
                if (best.length >= 20) return best;
            }

            // Pass 2: relaxed — qualquer texto > 20 chars nos mesmos seletores
            for (const sel of sels) {
                for (const el of document.querySelectorAll(sel)) {
                    const bb = el.getBoundingClientRect();
                    if (bb.x < 300 || bb.width < 200 || bb.height < 60) continue;
                    if (!visible(el)) continue;
                    const t = clean(el.innerText || el.textContent || '');
                    if (t.length >= 20 && t.length > best.length) best = t;
                }
                if (best.length >= 20) return best;
            }

            // Pass 3: broad — container scrollavel grande no painel direito
            for (const el of document.querySelectorAll('div, section, main')) {
                const bb = el.getBoundingClientRect();
                if (bb.x < 350 || bb.width < 250 || bb.height < 150) continue;
                const style = window.getComputedStyle(el);
                const isScroll = (style.overflowY === 'auto' || style.overflowY === 'scroll'
                    || el.scrollHeight > el.clientHeight + 50);
                if (!isScroll) continue;
                if (!visible(el)) continue;
                const t = clean(el.innerText || el.textContent || '');
                if (t.length >= 30 && t.length > best.length) best = t;
            }

            return best;
        }
        """)
        if text and len(text.strip()) >= 20:
            return text.strip()
    except Exception as _e:
        print(f"    debug get_conv_text exception: {_e}")
    # Debug: mostra o que existe no DOM quando falha
    try:
        dbg = page.evaluate("""
        () => {
            const info = [];
            for (const sel of ['[role="log"]', '[aria-label*="onvers"]', '[aria-label*="essag"]',
                                'div[contenteditable="true"]']) {
                const els = document.querySelectorAll(sel);
                els.forEach(el => {
                    const bb = el.getBoundingClientRect();
                    const txt = (el.innerText || '').trim();
                    info.push(sel + ' x=' + Math.round(bb.x) + ' y=' + Math.round(bb.y)
                        + ' w=' + Math.round(bb.width) + ' h=' + Math.round(bb.height)
                        + ' len=' + txt.length + ' start=' + JSON.stringify(txt.slice(0,80)));
                });
            }
            return info.slice(0, 8).join(' | ');
        }
        """)
        if dbg:
            print(f"    debug DOM: {dbg}")
    except Exception:
        pass
    return ""

def get_listing_url(page):
    """Extrai link do anúncio da conversa.
    Estratégias em ordem de confiabilidade:
    1. Link <a> do CARD do anúncio (o mais no topo do painel, x>380 — nunca a sidebar)
    2. Dados JSON embutidos no HTML (item_id, marketplace_listing_id)
    3. HTML bruto da página via regex

    IMPORTANTE: a Estratégia 1 pega o link com MENOR y (mais no topo) entre os
    candidatos — não o primeiro do DOM. Uma mensagem NOSSA já enviada (com o link
    do imóvel, ex: montar_mensagem_boas_vindas) vira um <a href> clicável dentro da
    bolha da conversa; pegar "o primeiro <a> que bate" migrava esse link antigo
    (às vezes errado) para leads novos, porque ele aparecia antes do card real no
    DOM em alguns layouts. O card do anúncio sempre renderiza acima das mensagens.
    """
    url = page.evaluate("""
    () => {
        const findItemId = (value) => {
            const txt = String(value || '').replace(/\\\\\\//g, '/').replace(/&amp;/g, '&');
            const m = txt.match(/marketplace\\/item\\/(\\d{6,})/);
            return m ? m[1] : null;
        };

        // 1. Entre todos os <a> que batem o padrão, escolher o de MENOR y
        // (mais próximo do topo do painel) — é o card do anúncio, não uma
        // mensagem enviada por nós ou pelo lead.
        let melhor = null, melhorY = Infinity;
        for (const a of document.querySelectorAll('a[href]')) {
            const itemId = findItemId(a.href || a.getAttribute('href') || a.outerHTML || '');
            if (!itemId) continue;
            const bb = a.getBoundingClientRect();
            if (bb.x < 380) continue;  // nunca considerar sidebar
            if (bb.y < melhorY) {
                melhorY = bb.y;
                melhor = itemId;
            }
        }
        if (melhor) return 'https://www.facebook.com/marketplace/item/' + melhor + '/';

        // 1b. Alguns layouts deixam o card como div clicavel, com o link em
        // atributos internos/outerHTML em vez de href direto.
        melhor = null; melhorY = Infinity;
        for (const el of document.querySelectorAll('div, span, [role="link"], [role="button"]')) {
            const bb = el.getBoundingClientRect();
            if (bb.x < 380 || bb.width < 80 || bb.height < 20) continue;
            const raw = [
                el.getAttribute('href'),
                el.getAttribute('aria-label'),
                el.getAttribute('data-hovercard'),
                el.getAttribute('data-store'),
                el.outerHTML
            ].filter(Boolean).join(' ');
            const itemId = findItemId(raw);
            if (!itemId) continue;
            if (bb.y < melhorY) {
                melhorY = bb.y;
                melhor = itemId;
            }
        }
        if (melhor) return 'https://www.facebook.com/marketplace/item/' + melhor + '/';

        // 2. JSON embutido nos <script> — Facebook embute item_id no pageData
        const idPats = [
            /"item_id"\s*:\s*"?(\d{10,})"?/,
            /"marketplace_listing_id"\s*:\s*"?(\d{10,})"?/,
            /"listing_id"\s*:\s*"?(\d{10,})"?/,
        ];
        for (const s of document.querySelectorAll('script')) {
            const t = s.textContent || '';
            if (!t.includes('marketplace')) continue;
            for (const p of idPats) {
                const m = t.match(p);
                if (m) return 'https://www.facebook.com/marketplace/item/' + m[1] + '/';
            }
        }

        return null;
    }
    """)
    if url:
        return url

    # 3. HTML bruto via Python regex (captura o que JS não renderiza)
    try:
        html = page.content()
        m = re.search(r'/marketplace/item/(\d{10,})', html)
        if m:
            return f"https://www.facebook.com/marketplace/item/{m.group(1)}/"
    except Exception:
        pass

    return None

def get_conv_nome(page):
    """Extrai o nome do contato da conversa aberta (cabeçalho da conversa)."""
    try:
        return page.evaluate("""
        () => {
            const skipWords = [
                'marketplace', 'conversas', 'inbox', 'mensagens', 'messages',
                'messenger', 'chats', 'explorar', 'escrever', 'write', 'compose',
                'histórico', 'historico', 'faltando', 'notificações', 'notifications',
                'selecione uma conversa', 'select a conversation',
                'novas', 'nova', 'novas mensagens', 'new messages', 'new',
                'solicitações', 'requests', 'spam', 'arquivadas', 'archived',
                'filtros', 'filters', 'todos', 'all', 'bate-papo', 'pessoas',
                'people', 'grupos', 'groups'
            ];
            // Prioridade: headings fora do sidebar esquerdo (x > 380px = área de conversa)
            const candidates = [...document.querySelectorAll('h1, h2, [role="heading"]')];
            // Primeiro tenta heading na área de conversa (direita)
            for (const el of candidates) {
                const bb = el.getBoundingClientRect();
                if (bb.x < 380) continue;  // ignora sidebar esquerdo
                const txt = (el.innerText || '').trim();
                const low = txt.toLowerCase();
                if (txt && txt.length > 1 && txt.length < 60
                    && !skipWords.some(w => low.includes(w)))
                    return txt;
            }
            // Fallback: qualquer heading fora do skipWords
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

def get_listing_url_retry(page, tentativas=4, espera=2):
    """Tenta capturar o link do anúncio várias vezes — o card do anúncio
    às vezes renderiza alguns segundos depois do resto da conversa."""
    for i in range(tentativas):
        link = get_listing_url(page)
        if link:
            return link
        if i < tentativas - 1:
            time.sleep(espera)
    return None

def normalize_marketplace_item_link(value):
    """Retorna link real de anuncio/imovel, nunca link de conversa."""
    if not value:
        return ""
    value = str(value)
    m = re.search(r'(?:https?://(?:www\.)?facebook\.com)?/marketplace/item/(\d{6,})', value)
    if m:
        return f"https://www.facebook.com/marketplace/item/{m.group(1)}/"
    m = re.search(r'https?://(?:www\.)?imparimoveis\.com/imovel/\d+/[^\s,"\')<]+', value)
    return m.group(0) if m else ""

def _norm_text(value):
    value = re.sub(r'<[^>]+>', ' ', str(value or ''))
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r'\s+', ' ', value.lower()).strip()

def lookup_imovel_link_from_hint(hint):
    """Acha o link oficial Impar pelo texto do anúncio visto no inbox."""
    hint_norm = _norm_text(hint)
    if not hint_norm:
        return ""

    price_match = re.search(r'r\$\s*[\d\.\,]+', hint_norm)
    price = price_match.group(0).replace(' ', '') if price_match else ""
    type_terms = [t for t in ('casa', 'apartamento', 'terreno', 'sala', 'comercial', 'kitnet') if t in hint_norm]
    place_terms = [t for t in ('joao costa', 'vila nova', 'itinga', 'paranaguamirim', 'floresta', 'centro') if t in hint_norm]

    base = CSV_ICLOUD.parent
    candidates = [
        base / 'fila-ciclo-marketplace.csv',
        base / 'fila-postagens.csv',
        base / 'fila-postagens-venda.csv',
        base / 'imoveis-venda.csv',
        base / 'imoveis-locacao.csv',
    ]
    best_url, best_score = "", 0
    for path in candidates:
        if not path.exists():
            continue
        try:
            with path.open(newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    row_text = _norm_text(' '.join(str(v or '') for v in row.values()))
                    if not row_text:
                        continue
                    score = 0
                    if price and price in row_text.replace(' ', ''):
                        score += 4
                    score += sum(2 for t in type_terms if t in row_text)
                    score += sum(3 for t in place_terms if t in row_text)
                    for key in ('codigo_imovel', 'codigo', 'referencia', 'ref'):
                        val = _norm_text(row.get(key, ''))
                        if val and val in hint_norm:
                            score += 5
                    url = row.get('url_impar') or row.get('url') or ''
                    if score > best_score and normalize_marketplace_item_link(url):
                        best_score = score
                        best_url = normalize_marketplace_item_link(url)
        except Exception:
            continue

    return best_url if best_score >= 7 else ""

def require_listing_link(link, nome):
    """Bloqueia lead capturado sem link de anuncio/imovel para evitar Telegram incompleto."""
    link = normalize_marketplace_item_link(link)
    if not link:
        print(f"    ⚠ Link real do anúncio/imóvel ausente para '{nome}' — não envia Telegram nem grava; tenta novamente no próximo ciclo")
        return ""
    return link

def montar_mensagem_boas_vindas(nome, link):
    primeiro_nome = nome.split()[0] if nome else "tudo"
    link_txt = link or ""
    return (
        f"Oi {primeiro_nome}, tudo bem? Aqui é a Impar Imóveis!\n"
        f"Vi que você demonstrou interesse em um dos nossos imóveis {link_txt}\n\n"
        f"Gostaria de retirar mais duvidas sobre o imóvel?"
    )

def ultimo_remetente_suspeito(conv_text, nome_esperado):
    """Facebook expõe cada mensagem com texto tipo 'Mensagem enviada ... por Fulano:'.
    Se o último remetente marcado no texto não é nem o lead esperado nem 'Você',
    é sinal forte de que o painel ainda mostra conteúdo do lead ANTERIOR (o React
    ainda não trocou o corpo da conversa, mesmo com o heading já atualizado)."""
    if not nome_esperado:
        return False
    matches = re.findall(r'por ([A-ZÀ-Ý][\wÀ-ÿ]*)\s*:', conv_text)
    if not matches:
        return False
    ultimo = matches[-1].lower()
    esperado_first = nome_esperado.split()[0].lower()
    if ultimo == 'você':
        return False
    if esperado_first in ultimo or ultimo in esperado_first:
        return False
    return True

def extract_imovel(text):
    for kw in ['Casa','Terreno','Comercial','Sala','Galpão','Kitnet','Studio','Sobrado']:
        if kw.lower() in text.lower(): return kw
    return 'Apartamento'

def trigger_conv_loading(page, hard=False):
    """Força o lazy loading do painel de conversa.
    Normal: scroll + click + focus no [role="log"].
    hard=True: page.goto(page.url) para forçar reload completo da página."""
    if hard:
        try:
            cur = page.url
            print(f"    🔄 Hard reload: {cur[-60:]}")
            page.goto(cur, wait_until="domcontentloaded", timeout=15000)
            time.sleep(18)
        except Exception as e:
            print(f"    ⚠ Hard reload falhou: {e}")
            try:
                page.reload(wait_until="domcontentloaded", timeout=15000)
                time.sleep(3)
            except Exception:
                pass
        return
    try:
        page.evaluate("""
        () => {
            for (const el of document.querySelectorAll('[role="log"]')) {
                const bb = el.getBoundingClientRect();
                if (bb.x < 300 || bb.width < 200) continue;
                el.scrollTop = el.scrollHeight;
                el.scrollTop = 0;
                el.dispatchEvent(new Event('scroll', {bubbles: true}));
                el.click();
                el.focus();
            }
            // Clique no centro do painel de conversa
            const cx = Math.max(window.innerWidth * 0.7, 800);
            const cy = window.innerHeight * 0.5;
            document.elementFromPoint(cx, cy)?.click();
        }
        """)
    except Exception:
        pass

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
        # URL sozinha não garante que o React já renderizou a conversa.
        # Continuamos aguardando o log/input do painel para evitar texto vazio.

        # 2. Log de conversa visível no painel da direita, não na sidebar
        # IMPORTANTE: rejeitar "Carregando..." / "Loading..." — o Facebook
        # renderiza o container do log antes de carregar as mensagens reais.
        try:
            has_conversation_log = page.evaluate("""
            () => {
                const loading = ['carregando', 'loading', 'aguarde', 'wait'];
                for (const el of document.querySelectorAll('[role="log"]')) {
                    const bb = el.getBoundingClientRect();
                    if (bb.x < 300 || bb.width < 200 || bb.height < 80) continue;
                    const t = (el.innerText || '').trim();
                    if (t.length > 20 && !loading.some(w => t.toLowerCase().startsWith(w))) {
                        return true;
                    }
                }
                return false;
            }
            """)
            if has_conversation_log:
                return True
        except Exception:
            pass

        # 3. Campo de input visível — indica que o frame da conversa abriu,
        # mas as mensagens podem ainda estar em "Carregando...".
        # Dispara trigger_conv_loading para forçar o lazy load e continua
        # polling para dar chance ao [role="log"] carregar com conteúdo real.
        _found_textbox = False
        for sel in CE_SELECTORS:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    _found_textbox = True
                    break
            except Exception:
                pass
        if _found_textbox:
            trigger_conv_loading(page)
            if time.time() + 5 > deadline:
                return True

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

    Texto com '\\n' é enviado como mensagens separadas, uma por linha. O type()
    do Playwright traduz '\\n' em Enter, que no Messenger ENVIA a mensagem — a
    primeira linha saía sozinha e a segunda se perdia quando o popup
    re-renderizava. Cada linha é digitada e enviada no seu próprio ciclo.
    """
    partes = [p.strip() for p in text.split('\n') if p.strip()]
    if not partes:
        return False

    enviadas = 0
    for i, parte in enumerate(partes):
        try:
            # Fechar quick-reply suggestions com Escape
            page.keyboard.press('Escape')
            time.sleep(0.4)

            # Aguardar textbox (popup input "Aa") — reobtido a cada parte,
            # porque o popup remonta o input depois de cada envio
            box = page.wait_for_selector(
                'div[contenteditable="true"][role="textbox"]',
                timeout=8000, state='visible'
            )
            if not box:
                print(f"    ⚠ Textbox não encontrado (parte {i+1}/{len(partes)})")
                break

            if i == 0:
                bb = box.bounding_box()
                print(f"    debug: textbox em x={bb['x']:.0f} y={bb['y']:.0f} w={bb['width']:.0f} h={bb['height']:.0f}" if bb else "    debug: textbox sem bounding box")

            # Clicar com force para bypassar qualquer overlay residual
            box.click(force=True)
            time.sleep(0.4)

            # type() — método ElementHandle no Playwright 1.60
            box.type(parte, delay=15)
            time.sleep(0.5)

            # Enviar com Enter
            page.keyboard.press('Enter')
            time.sleep(2.5)
            enviadas += 1

        except Exception as e:
            print(f"    ⚠ send_message erro (parte {i+1}/{len(partes)}): {e}")
            break

    if enviadas < len(partes):
        print(f"    ⚠ enviadas {enviadas}/{len(partes)} partes da resposta")
    return enviadas == len(partes)

def send_message_single(page, text):
    """
    Envia `text` como UMA ÚNICA mensagem no Messenger, mesmo contendo quebras
    de linha ('\\n'). Diferente de send_message() — que envia cada linha como
    mensagem separada — aqui a quebra de linha interna usa Shift+Enter (não
    dispara o envio) e só o Enter final envia tudo junto, em uma bolha só.
    """
    linhas = [l.strip() for l in text.split('\n') if l.strip()]
    if not linhas:
        return False
    try:
        page.keyboard.press('Escape')
        time.sleep(0.4)

        box = page.wait_for_selector(
            'div[contenteditable="true"][role="textbox"]',
            timeout=8000, state='visible'
        )
        if not box:
            print("    ⚠ Textbox não encontrado")
            return False

        box.click(force=True)
        time.sleep(0.4)

        for i, linha in enumerate(linhas):
            box.type(linha, delay=15)
            if i < len(linhas) - 1:
                page.keyboard.press('Shift+Enter')
                time.sleep(0.2)

        time.sleep(0.4)
        page.keyboard.press('Enter')
        time.sleep(2.5)
        return True

    except Exception as e:
        print(f"    ⚠ send_message_single erro: {e}")
        return False

def dismiss_notifications_panel(page):
    """
    Fecha painel de Notificações do Facebook se estiver sobreposto ao inbox.
    Sem isso, clicks nas threads abrem o painel em vez da conversa.
    """
    try:
        # Verifica se painel de notificações está visível
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
            # Clicar numa área neutra (canto superior esquerdo da página, fora do inbox)
            page.mouse.click(640, 60)
            time.sleep(0.8)
            page.keyboard.press('Escape')
            time.sleep(0.5)
    except Exception:
        pass

def is_thread_open(page):
    """Verifica se uma conversa está aberta (URL diferente do inbox)."""
    return '/marketplace/inbox/' in page.url and page.url != INBOX_URL

def is_marketplace_conv(page):
    """
    Guard obrigatório — verifica se a conversa aberta é do Marketplace.

    ⛔ REGRA: este script responde SOMENTE conversas do Facebook Marketplace.
    Conversas pessoais, de grupos, de páginas ou qualquer outra origem
    devem ser IGNORADAS — nunca enviar mensagem nesses casos.

    Critério (em ordem):
    1. URL com /marketplace/
    2. a[href*="/marketplace/item/"] (até 10s — links de card de anúncio)
    3. DOM ampliado: qualquer link /marketplace/ OU label "Marketplace" isolado
       no painel de conversa (x > 380px) — detecta modo messages/ onde o card
       de anúncio pode não renderizar mas o label de contexto aparece.
    Se retornar False → stats['p'] += 1, NUNCA enviar.
    """
    if '/marketplace/' in page.url:
        return True
    # Aguardar carregamento assíncrono do link do item (comum em messages/ mode)
    try:
        page.wait_for_selector('a[href*="/marketplace/item/"]', timeout=10000)
        return True
    except Exception:
        pass
    # Verificação DOM ampliada — inclui qualquer link /marketplace/ e label de contexto
    try:
        return bool(page.evaluate("""
        () => {
            // Link direto de item ou perfil de vendedor no Marketplace
            if (document.querySelector('a[href*="/marketplace/item/"]')) return true;
            if (document.querySelector('a[href*="/marketplace/"]')) return true;
            // Label "Marketplace" isolado no painel de conversa (direita, x > 380)
            for (const el of document.querySelectorAll('span, div, a, h1, h2, h3, [role="heading"]')) {
                try {
                    const bb = el.getBoundingClientRect();
                    if (bb.x < 380 || bb.width < 5) continue;
                    const txt = (el.innerText || '').trim();
                    if (txt.toLowerCase() === 'marketplace') return true;
                } catch (_) {}
            }
            return false;
        }
        """))
    except Exception:
        return False

def analisar_com_regras(conv_text, nome, preview):
    """Análise por regras — sem API externa, zero custo.
    1. Telefone na conversa → CAPTUROU_CONTATO
    2. Última mensagem é nossa → SEM_ACAO
    3. Última mensagem não é nossa (é do lead) → PEDIR_CONTATO

    NOTA: o campo `preview` (sidebar) não é mais exigido no passo 3 — a UI em
    div do Facebook frequentemente entrega preview vazio mesmo com mensagem
    nova do lead na conversa, e isso travava leads reais em SEM_ACAO por horas.
    A decisão agora se baseia só no conteúdo real da conversa (conv_text).
    """
    # 1. Qualquer telefone mencionado na conversa.
    # IMPORTANTE: remover URLs antes de buscar — o link do anúncio que NÓS mandamos
    # (ex: .../marketplace/item/1078184554783477/) tem sequências de 8+ dígitos que
    # o regex de telefone casava como se fosse um número real do lead.
    conv_sem_url = re.sub(r'https?://\S+', ' ', conv_text)
    # Remover também linhas que são mensagens NOSSAS — nomes de anúncio, texto de
    # confirmação etc podem conter dígitos que não são telefone do lead.
    conv_sem_nossas = '\n'.join(
        l for l in conv_sem_url.split('\n')
        if not any(p in l for p in NOSSAS_FRASES)
    )
    phones = PHONE_RE.findall(conv_sem_nossas)
    if phones:
        raw = phones[-1]
        telefone = re.sub(r'[^\d]', '', raw)
        if len(telefone) >= 8:
            print(f"    debug telefone: match='{raw}' → {telefone} | contexto='...{conv_sem_nossas[-250:]}'")
            return {"acao": "CAPTUROU_CONTATO", "telefone": telefone}

    # 2. Verificar se última mensagem relevante é nossa
    # Janela de 2 linhas (era 8): nossa mensagem de PEDIR_CONTATO ocupa exatamente
    # 2 linhas ("Vou verificar essa informação" / "Qual seu whatsapp para retorno?").
    # Com janela de 8, qualquer resposta curta do lead depois disso ficava "escondida"
    # atrás da nossa frase por 2-3 rodadas e o lead travava em SEM_ACAO. Com -2, basta
    # o lead mandar UMA mensagem nova pra voltar a cair em PEDIR_CONTATO.
    ts_pat = re.compile(TIMESTAMP_RE_STR)
    lines = [l.strip() for l in conv_text.split('\n')
             if l.strip() and not ts_pat.match(l.strip()) and l.strip() != '·']
    last_block = ' '.join(lines[-2:]) if lines else ''
    _matched = next((p for p in NOSSAS_FRASES if p in last_block), None)
    if _matched:
        print(f"    debug SEM_ACAO: frase '{_matched}' casou em last_block='{last_block[-200:]}'")
        return {"acao": "SEM_ACAO", "telefone": None}

    # 3. Chegou até aqui: tem conteúdo real e a última mensagem não é nossa
    # → é do lead, aguardando nossa resposta.
    if lines:
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
            # headless=True: sob launchd o browser com janela não tem acesso
            # pleno à GUI e os cliques não chegam à página ("Conversa não abriu"
            # com ce=False/log=False). Headless é determinístico aqui.
            headless=True,
            viewport={"width": 1920, "height": 1080},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-sync",
                "--password-store=basic",
                "--use-mock-keychain",
                "--aggressive-cache-discard",
                "--disable-back-forward-cache",
                "--disable-features=BackForwardCache",
            ],
        )
        page = ctx.new_page()

        # Limpar cache e service workers para evitar "Carregando..." travado
        try:
            client = page.context.new_cdp_session(page)
            client.send("Network.clearBrowserCache")
            client.send("Storage.clearDataForOrigin", {
                "origin": "https://www.facebook.com",
                "storageTypes": "cache_storage,service_workers"
            })
            client.detach()
            print("  🧹 Cache/SW limpos")
        except Exception:
            pass

        print(f"→ Acessando inbox ({ts})...")
        try:
            page.goto(INBOX_URL, wait_until="domcontentloaded", timeout=60000)
        except Exception as _goto_err:
            err_str = str(_goto_err)
            if "ERR_TOO_MANY_REDIRECTS" in err_str or "ERR_" in err_str:
                # marketplace/inbox bloqueado — tentar direto pelo messages/
                print(f"  ⚠ marketplace/inbox bloqueado ({err_str[:60]}) — indo para messages/")
                try:
                    page.goto("https://www.facebook.com/messages/",
                              wait_until="domcontentloaded", timeout=30000)
                except Exception as _msg_err:
                    print(f"  ⚠ messages/ também falhou: {_msg_err}")
                    ctx.close()
                    update_log(stats, leads, "LOGIN_EXPIRADO", ts)
                    return "LOGIN_EXPIRADO"
            else:
                raise

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

        # Bloco real: texto de bloqueio apenas em headings/alertas (não texto solto na página)
        # Evita falso-positivo com notificações ou anúncios que usam a mesma palavra.
        block_in_heading = page.evaluate("""
        () => {
            const selectors = ['h1','h2','h3','[role="heading"]','[role="alert"]','[role="dialog"] p'];
            const terms = ['bloqueado temporariamente','bloqueamos temporariamente',
                           'temporarily blocked','we temporarily blocked'];
            for (const sel of selectors) {
                for (const el of document.querySelectorAll(sel)) {
                    const t = (el.innerText || '').toLowerCase();
                    if (terms.some(w => t.includes(w))) return true;
                }
            }
            return false;
        }
        """) if page.query_selector('body') else False

        url_redirected = ('marketplace/inbox' not in cur_url and 'marketplace' not in cur_url)
        is_blocked = block_in_heading or url_redirected

        if not is_blocked and 'bloqueado temporariamente' in body_text.lower():
            # Texto aparece mas não em heading — pode ser notificação/modal. Tentar fechar.
            try:
                page.evaluate("""
                () => {
                    // Tentar fechar qualquer diálogo/overlay com botão X ou Fechar
                    for (const el of document.querySelectorAll('[aria-label*="echar"],[aria-label*="lose"],[data-testid*="dismiss"]')) {
                        if (el.offsetParent !== null) { el.click(); return; }
                    }
                }
                """)
                time.sleep(2)
                # Refresh suave para limpar o estado
                page.reload(wait_until="domcontentloaded", timeout=20000)
                time.sleep(4)
                body_text = page.inner_text('body') if page.query_selector('body') else ''
                block_in_heading = page.evaluate("""
                () => {
                    const selectors = ['h1','h2','h3','[role="heading"]','[role="alert"]'];
                    const terms = ['bloqueado temporariamente','bloqueamos temporariamente'];
                    for (const sel of selectors) {
                        for (const el of document.querySelectorAll(sel)) {
                            if (terms.some(w => (el.innerText||'').toLowerCase().includes(w))) return true;
                        }
                    }
                    return false;
                }
                """)
                is_blocked = block_in_heading
                if not is_blocked:
                    print("  ℹ Modal/overlay fechado — continuando normalmente")
            except Exception as _be:
                print(f"  [WARN] Tentativa de fechar modal: {_be}")
                is_blocked = True

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
                        full_text: (a.innerText || '').trim(),
                        y: bb.y
                    });
                });
                return results;
            }
            """)
            # Filtrar threads onde o preview já tem resposta nossa
            thread_urls = [l for l in raw_links
                           if not any(p in l.get('preview', '') for p in NOSSAS_FRASES)]
            # Marcar hint de Marketplace por texto do sidebar ou pelo indicador clicado
            _MP_SIDEBAR_HINTS = {'marketplace', 'solicitação', 'solicitacao'}
            for _t in thread_urls:
                _ft = _t.get('full_text', '').lower()
                _t['is_marketplace_hint'] = (
                    via_marketplace_indicator
                    or any(h in _ft for h in _MP_SIDEBAR_HINTS)
                )
            print(f"  Threads messages/ detectadas: {len(thread_urls)}")

            # Fallback secundário: raw_links encontrou 0 → tentar get_unique_threads
            if not thread_urls:
                gt = get_unique_threads(page, messages_mode=True)
                print(f"  Threads get_unique_threads (fallback): {len(gt)}")
                thread_urls = [{'url': None, 'text': t['text'], 'preview': t.get('preview', ''),
                                'imovel_hint': t.get('imovel_hint', ''),
                                'full_text': t.get('imovel_hint', ''),
                                'cx': t.get('cx', 300), 'cy': t.get('cy', t['y']), 'y': t['y']}
                               for t in gt]

            # Fallback secundário-b: marketplace bloqueado mas mensagens/ aberto
            # Remove o filtro de Marketplace e exibe TODAS as mensagens não lidas
            if not thread_urls:
                print(f"  → Marketplace bloqueado: tentando inbox geral de messages/...")
                try:
                    page.goto("https://www.facebook.com/messages/", wait_until="domcontentloaded", timeout=15000)
                    time.sleep(4)
                    all_links = page.evaluate("""
                    () => {
                        const seen = new Set();
                        const results = [];
                        document.querySelectorAll('a[href]').forEach(a => {
                            const href = a.href || '';
                            if (!href.includes('/messages/t/') && !href.includes('/messages/e2ee/t/')) return;
                            const bb = a.getBoundingClientRect();
                            if (bb.x > 500 || bb.y < 100 || bb.width < 50) return;
                            if (seen.has(href)) return;
                            seen.add(href);
                            const lines = (a.innerText || '').trim().split('\\n').filter(Boolean);
                            results.push({url: href, text: lines[0] || 'Lead',
                                          preview: lines[lines.length-1] || '',
                                          full_text: (a.innerText || '').trim(),
                                          imovel_hint: (a.innerText || '').trim(),
                                          y: bb.y});
                        });
                        return results;
                    }
                    """)
                    thread_urls = [l for l in all_links
                                   if not any(p in l.get('preview', '') for p in NOSSAS_FRASES)]
                    print(f"  Threads inbox geral: {len(thread_urls)}")
                    if thread_urls:
                        effective_base = "https://www.facebook.com/messages/"
                except Exception as _fe:
                    print(f"  [WARN] Inbox geral: {_fe}")

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
            _prev_conv_text_mm = ""  # detecta DOM ainda não trocou (conteúdo do lead anterior)
            for turl in thread_urls:
                nome = turl['text'].split()[0] if turl['text'] else 'Lead'
                print(f"\n  → {nome} (messages/t)")
                stats['v'] += 1
                try:
                    if turl.get('url'):
                        page.goto(turl['url'], wait_until="domcontentloaded", timeout=20000)
                    else:
                        clicked = click_thread(page, turl['text'],
                                               coords=(turl.get('cx'), turl.get('cy'))
                                               if turl.get('cx') else None)
                        if not clicked:
                            page.mouse.click(turl.get('cx', 300), turl.get('cy', turl['y']))

                    # Aguarda heading da conversa carregar com nome correto antes de ler o conteúdo.
                    # Sem isso, o [role="log"] pode ainda exibir mensagens da conversa anterior
                    # (race condition: domcontentloaded dispara antes do React atualizar o log).
                    _INBOX_HEADS = {'conversas','marketplace','inbox','mensagens','messages','messenger','bate-papo','chats','selecione'}
                    expected_first = (turl.get('text', '').split()[0]).lower() if turl.get('text') else ''
                    nome_real = None
                    _wait_elapsed = 0
                    while _wait_elapsed < 12:
                        time.sleep(1)
                        _wait_elapsed += 1
                        cand = get_conv_nome(page)
                        if cand and any(w in cand.lower() for w in _INBOX_HEADS):
                            cand = None
                        if cand:
                            nome_real = cand
                            if expected_first and expected_first in nome_real.lower():
                                break  # heading correto apareceu — conteúdo pronto
                    if (
                        _wait_elapsed >= 12
                        and expected_first
                        and expected_first not in {'lead', 'marketplace', 'interessado(a)'}
                        and (not nome_real or expected_first not in (nome_real or '').lower())
                    ):
                        print(f"    ⚠ Heading '{nome_real}' ≠ esperado '{expected_first}' após 12s — pulando para não responder conversa errada")
                        stats['e'] += 1
                        continue
                    if nome_real:
                        nome = nome_real
                    if not nome or nome == 'Lead':
                        nome = 'Interessado(a)'
                    # Extra 2s: garante que o [role="log"] termina de renderizar após o heading aparecer
                    time.sleep(2)

                    # Guard obrigatório: só processar se for conversa do Marketplace.
                    # Conversas pessoais são SEMPRE ignoradas — nunca enviar.
                    _is_mp = is_marketplace_conv(page)
                    _mp_hint = turl.get('is_marketplace_hint', False)
                    if not _is_mp and not _mp_hint:
                        print(f"    ⏭ CONVERSA PESSOAL — is_marketplace=False hint=False — ignorando")
                        stats['p'] += 1
                        page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                        time.sleep(2)
                        continue
                    if not _is_mp and _mp_hint:
                        print(f"    ⚠ is_marketplace=False mas hint=True (sidebar/indicador) — prosseguindo")

                    # Comparação com texto do lead anterior removida como bloqueio —
                    # ver nota equivalente no outro bloco (marketplace/inbox) sobre
                    # o caso Kaua/Guarajara com pergunta padrão idêntica.
                    conv_text = ""
                    for _ct_try in range(18):
                        conv_text = get_conv_text(page)
                        if len(conv_text.strip()) >= 20 and not ultimo_remetente_suspeito(conv_text, nome):
                            break
                        if _ct_try == 0:
                            trigger_conv_loading(page)
                        elif _ct_try == 5:
                            trigger_conv_loading(page, hard=True)
                        elif _ct_try == 12:
                            trigger_conv_loading(page, hard=True)
                        elif _ct_try in (3, 8, 15):
                            trigger_conv_loading(page)
                        time.sleep(1)
                    if len(conv_text.strip()) < 20:
                        print(f"    ⚠ Conversa não carregou — pulando")
                        stats['e'] += 1
                        continue
                    if ultimo_remetente_suspeito(conv_text, nome):
                        print(f"    ⚠ Último remetente no texto não bate com '{nome}' — pulando para não misturar dados")
                        stats['e'] += 1
                        continue
                    _prev_conv_text_mm = conv_text.strip()

                    link = get_listing_url_retry(page)
                    if link:
                        print(f"    🔗 Link: {link}")
                    else:
                        link = (
                            normalize_marketplace_item_link(conv_text)
                            or lookup_imovel_link_from_hint(turl.get('full_text', ''))
                            or lookup_imovel_link_from_hint(turl.get('imovel_hint', ''))
                            or lookup_imovel_link_from_hint(turl.get('text', ''))
                            or lookup_imovel_link_from_hint(turl.get('preview', ''))
                        )
                    link = normalize_marketplace_item_link(link)
                    if link:
                        print(f"    🔗 Link: {link}")
                    else:
                        print(f"    ⚠ Link real do anúncio ainda não encontrado")
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
                            print(f"    ↳ {telefone_ia} já no CSV — pulando (lead já capturado)")
                            stats['p'] += 1
                        else:
                            existing_owner = phone2name.get(telefone_ia, '')
                            if existing_owner and existing_owner.split()[0].lower() != nome.split()[0].lower():
                                print(f"    ⚠ Telefone {telefone_ia} pertence a '{existing_owner}', não a '{nome}' — possível vazamento de conversa, pulando")
                                stats['e'] += 1
                            else:
                                link = require_listing_link(link, nome)
                                if not link:
                                    stats['e'] += 1
                                    continue
                                # Só um agradecimento curto no Facebook — o discurso completo
                                # (Oi {nome}... Vi que você demonstrou interesse...) vai
                                # só pelo link de WhatsApp que o Jonata recebe no Telegram
                                # (notificar_lead_whatsapp.py). Decisão do Jonata em 2026-08-29
                                # depois do Guarajara receber a mensagem completa nos dois canais.
                                resp = "Obrigado, vamos entrar em contato via whatsapp."
                                sent = send_message(page, resp)
                                if sent:
                                    stats['r'] += 1
                                    print(f"    ✓ Agradecimento enviado — {telefone_ia}")
                                append_lead(nome, telefone_ia, imovel, link or '', 'Messenger IA')
                                known.add(telefone_ia)
                                phone2name[telefone_ia] = nome
                                leads.append({'nome': nome, 'telefone': telefone_ia, 'imovel': imovel})
                                stats['t'] += 1
                                notificar_jonata(nome, telefone_ia, imovel, link or '')
                                mark_notified(notificados, telefone_ia)
                    elif acao_ia == 'PEDIR_CONTATO':
                        resp = "Vou verificar essa informação\nQual seu whatsapp para retorno?"
                        sent = send_message_single(page, resp)
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
                print(f"  ⚠ Browse mode detectado — reload para inbox")
                page.reload(wait_until="domcontentloaded", timeout=20000)
                time.sleep(5)
                threads = get_unique_threads(page)

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

        _prev_conv_text = ""  # detecta DOM ainda não trocou (conteúdo do lead anterior)
        for thread in threads:
            nome = get_nome(thread['text'])
            print(f"\n  → {nome} (y={thread['y']:.0f})")
            stats['v'] += 1

            try:
                # Abrir a conversa certa às vezes falha (coordenada cai numa linha
                # vizinha por causa de reordenação da lista) — tenta até 3x antes
                # de desistir desse lead nesta rodada.
                sucesso_abertura = False
                for _tentativa_abertura in range(3):
                    # Navegar direto pela URL se disponível (evita click interceptado por painel Notificações)
                    thread_url = thread.get('url', '')
                    _nav_patterns = ('/marketplace/inbox/', '/messages/t/', '/messages/e2ee/t/')
                    if thread_url and any(p in thread_url for p in _nav_patterns):
                        print(f"    → navegando por URL direta")
                        page.goto(thread_url, wait_until="domcontentloaded", timeout=20000)
                    else:
                        # Fechar painel de Notificações e clicar
                        dismiss_notifications_panel(page)
                        # Scroll sidebar ao topo antes de re-detectar (coordenadas mudam
                        # quando Facebook re-ordena após enviarmos mensagem)
                        try:
                            page.wait_for_load_state("networkidle", timeout=3000)
                        except Exception:
                            pass
                        # Rolar sidebar ao topo via JS (mouse.wheel pode acertar o elemento errado)
                        page.evaluate("""
                        () => {
                            const els = Array.from(document.querySelectorAll('*'));
                            for (const el of els) {
                                const s = window.getComputedStyle(el);
                                const bb = el.getBoundingClientRect();
                                if ((s.overflowY === 'auto' || s.overflowY === 'scroll')
                                    && el.scrollHeight > el.clientHeight + 50
                                    && bb.x < 650 && bb.width > 150 && bb.height > 300) {
                                    el.scrollTop = 0;
                                }
                            }
                        }
                        """)
                        time.sleep(1.2)
                        # Re-detectar na lista atual (coordenadas iniciais ficam obsoletas
                        # depois que abrimos conversas anteriores)
                        coords = None
                        try:
                            for atual in get_unique_threads(page, messages_mode=False):
                                if atual['text'] == thread['text']:
                                    coords = (atual['cx'], atual['cy'])
                                    break
                        except Exception:
                            pass
                        # Se thread abaixo do viewport (y > 700), rolar sidebar até ele via JS
                        if coords and coords[1] > 700:
                            scroll_px = int(coords[1] - 400)
                            page.evaluate(f"""
                            () => {{
                                const els = Array.from(document.querySelectorAll('*'));
                                for (const el of els) {{
                                    const s = window.getComputedStyle(el);
                                    const bb = el.getBoundingClientRect();
                                    if ((s.overflowY === 'auto' || s.overflowY === 'scroll')
                                        && el.scrollHeight > el.clientHeight + 50
                                        && bb.x < 650 && bb.width > 150 && bb.height > 300) {{
                                        el.scrollTop += {scroll_px};
                                    }}
                                }}
                            }}
                            """)
                            time.sleep(0.6)
                            try:
                                for atual in get_unique_threads(page, messages_mode=False):
                                    if atual['text'] == thread['text']:
                                        coords = (atual['cx'], atual['cy'])
                                        break
                            except Exception:
                                pass
                        # Não usar coordenadas velhas como fallback — causam clique na thread errada
                        if coords is None:
                            print(f"    ⚠ Thread '{thread['text']}' não encontrado após re-detecção (tentativa {_tentativa_abertura+1}/3)")
                            time.sleep(1.5)
                            continue
                        clicked = click_thread(page, thread['text'], coords=coords)
                        if not clicked:
                            page.mouse.click(coords[0], coords[1])
                    time.sleep(1.5)

                    # Aguardar input de mensagem aparecer (confirma que conversa abriu)
                    conv_open = wait_for_conversation_open(page, timeout=20, base_url=effective_base)
                    if not conv_open:
                        cur_url = page.url
                        has_ce = bool(page.query_selector('div[contenteditable="true"]'))
                        has_log = bool(page.query_selector('[role="log"]'))
                        print(f"    ⚠ Conversa não abriu | ce={has_ce} | log={has_log} | url={cur_url[-60:]} (tentativa {_tentativa_abertura+1}/3)")
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
                        print(f"    ⚠ Conversa errada abriu: esperado '{nome}', abriu '{nome_real}' (tentativa {_tentativa_abertura+1}/3)")
                        page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                        time.sleep(3)
                        if messages_mode:
                            page.evaluate("""() => { const rows = document.querySelectorAll('[role="row"]'); for (const r of rows) { if (r.textContent.includes('Marketplace')) { r.click(); break; } } }""")
                            time.sleep(1.5)
                        continue

                    sucesso_abertura = True
                    break

                if not sucesso_abertura:
                    print(f"    ⚠ Não consegui abrir a conversa certa de '{nome}' após 3 tentativas — pulando")
                    stats['e'] += 1
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

                # Guard obrigatório: só processar se for conversa do Marketplace.
                # Conversas pessoais são SEMPRE ignoradas — nunca envia mensagem aqui.
                if not is_marketplace_conv(page):
                    print(f"    ⏭ CONVERSA PESSOAL — is_marketplace=False — ignorando (nunca envia aqui)")
                    stats['p'] += 1
                    page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(2)
                    continue

                # Aguardar conversa carregar E o DOM realmente trocar do lead anterior.
                # O painel de conversa às vezes ainda mostra o conteúdo do lead anterior
                # por 1-2s depois do heading já ter trocado (React atualiza em passos
                # diferentes) — ler cedo demais mistura mensagens de leads diferentes.
                # NOTA: a checagem de "texto idêntico ao lead anterior" foi removida
                # como bloqueio — dois leads diferentes às vezes mandam a MESMA
                # pergunta padrão sugerida pelo Facebook ("Gostaria de retirar mais
                # duvidas sobre o imóvel?"), o que travava o segundo lead pra sempre
                # (2026-08-29, caso Kaua sempre depois de Guarajara). A verificação
                # de remetente (ultimo_remetente_suspeito) é mais confiável — usa o
                # nome real marcado em cada mensagem, não o texto.
                conv_text = ""
                _navigated_to_messages = False
                for _ct_try in range(18):
                    conv_text = get_conv_text(page)
                    if len(conv_text.strip()) >= 20 and not ultimo_remetente_suspeito(conv_text, nome):
                        break
                    if _ct_try == 0:
                        trigger_conv_loading(page)
                    elif _ct_try == 5 and not _navigated_to_messages and not messages_mode:
                        import re as _re_tid
                        _tid = None
                        _m = _re_tid.search(r'/marketplace/inbox/(\d+)', page.url)
                        if _m:
                            _tid = _m.group(1)
                        else:
                            try:
                                _tid = page.evaluate("""
                                () => {
                                    for (const a of document.querySelectorAll('a[href]')) {
                                        const m = (a.href || '').match(/\\/messages\\/t\\/(\\d+)/);
                                        if (m) return m[1];
                                        const m2 = (a.href || '').match(/\\/marketplace\\/inbox\\/(\\d+)/);
                                        if (m2) return m2[1];
                                    }
                                    return null;
                                }
                                """)
                            except Exception:
                                pass
                        if _tid:
                            print(f"    🔄 marketplace stuck — tentando /messages/t/{_tid}")
                            try:
                                page.goto(f"https://www.facebook.com/messages/t/{_tid}",
                                          wait_until="domcontentloaded", timeout=20000)
                                time.sleep(4)
                                _navigated_to_messages = True
                            except Exception as _nav_e:
                                print(f"    ⚠ /messages/t/ falhou: {_nav_e}")
                                trigger_conv_loading(page, hard=True)
                        else:
                            trigger_conv_loading(page, hard=True)
                    elif _ct_try == 5 and (messages_mode or _navigated_to_messages):
                        trigger_conv_loading(page, hard=True)
                    elif _ct_try == 12:
                        trigger_conv_loading(page, hard=True)
                    elif _ct_try in (3, 8, 15):
                        trigger_conv_loading(page)
                    time.sleep(1)
                else:
                    if ultimo_remetente_suspeito(conv_text, nome):
                        print(f"    ⚠ Último remetente no texto não bate com '{nome}' após 18s — pulando para não misturar dados")
                        stats['e'] += 1
                        page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                        time.sleep(3)
                        continue
                _prev_conv_text = conv_text.strip()
                link = get_listing_url_retry(page)
                if not link:
                    link = (
                        normalize_marketplace_item_link(conv_text)
                        or lookup_imovel_link_from_hint(thread.get('imovel_hint', ''))
                        or lookup_imovel_link_from_hint(thread.get('text', ''))
                        or lookup_imovel_link_from_hint(thread.get('preview', ''))
                    )
                link = normalize_marketplace_item_link(link)
                if link:
                    print(f"    🔗 Link: {link}")
                else:
                    print(f"    ⚠ Link real do anúncio ainda não encontrado")
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
                        print(f"    ↳ {telefone_ia} já no CSV — pulando (lead já capturado)")
                        stats['p'] += 1
                    else:
                        existing_owner = phone2name.get(telefone_ia, '')
                        if existing_owner and existing_owner.split()[0].lower() != nome.split()[0].lower():
                            print(f"    ⚠ Telefone {telefone_ia} pertence a '{existing_owner}', não a '{nome}' — possível vazamento de conversa, pulando")
                            stats['e'] += 1
                        else:
                            link = require_listing_link(link, nome)
                            if not link:
                                stats['e'] += 1
                                page.goto(effective_base, wait_until="domcontentloaded", timeout=15000)
                                time.sleep(3)
                                continue
                            # Só um agradecimento curto no Facebook — ver nota no outro
                            # bloco CAPTUROU_CONTATO acima sobre a decisão de 2026-08-29.
                            resp = "Obrigado, vamos entrar em contato via whatsapp."
                            sent = send_message(page, resp)
                            if sent:
                                stats['r'] += 1
                                print(f"    ✓ Agradecimento enviado — {telefone_ia}")
                            append_lead(nome, telefone_ia, imovel, link, 'Messenger IA')
                            known.add(telefone_ia)
                            phone2name[telefone_ia] = nome
                            leads.append({'nome': nome, 'telefone': telefone_ia, 'imovel': imovel})
                            stats['t'] += 1
                            notificar_jonata(nome, telefone_ia, imovel, link)
                            mark_notified(notificados, telefone_ia)

                elif acao_ia == 'PEDIR_CONTATO':
                    resp = "Vou verificar essa informação\nQual seu whatsapp para retorno?"
                    sent = send_message_single(page, resp)
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
                time.sleep(3)
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

    # Redirecionar stdout/stderr para os arquivos de log quando não interativo.
    # Cobre rodadas manuais em background (python3 script.py &) onde o LaunchAgent
    # não está presente para redirecionar. Em modo interativo (tty) mantém o terminal.
    _STDOUT_LOG = Path("/Users/usuario/Library/Logs/impar-varredura-auto.log")
    _STDERR_LOG = Path("/Users/usuario/Library/Logs/impar-varredura-auto-error.log")
    try:
        if not _os.isatty(sys.stdout.fileno()):
            _stdout_log_fd = open(_STDOUT_LOG, "a", buffering=1, encoding="utf-8")
            _stderr_log_fd = open(_STDERR_LOG, "a", buffering=1, encoding="utf-8")
            _os.dup2(_stdout_log_fd.fileno(), sys.stdout.fileno())
            _os.dup2(_stderr_log_fd.fileno(), sys.stderr.fileno())
    except Exception:
        pass

    LOCK_PATH = Path.home() / ".local/impar-automation/messenger/.varredura-python.lock"
    LOCK_MAX_AGE = 900  # 15 min — mata processo travado automaticamente
    try:
        lock_fd = open(LOCK_PATH, 'a+')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        age = time.time() - LOCK_PATH.stat().st_mtime if LOCK_PATH.exists() else 0
        if age > LOCK_MAX_AGE:
            print(f"⚠ Lock preso há {age:.0f}s — matando processo travado e reiniciando...")
            import signal as _sig
            try:
                pid = int(LOCK_PATH.read_text().strip()) if LOCK_PATH.read_text().strip().isdigit() else None
                if pid:
                    _os.kill(pid, _sig.SIGTERM)
                    time.sleep(2)
            except Exception:
                pass
            LOCK_PATH.unlink(missing_ok=True)
            lock_fd = open(LOCK_PATH, 'w')
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        else:
            print(f"⏳ Outra instância rodando há {age:.0f}s — saindo.")
            sys.exit(0)

    lock_fd.seek(0)
    lock_fd.truncate()
    lock_fd.write(f"{_os.getpid()}\n{int(time.time())}\n{ACCOUNT_ID}\n")
    lock_fd.flush()
    _sync_notif_script()
    _sync_csv_from_icloud()
    retry_pending_notif()
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
        try:
            LOCK_PATH.unlink(missing_ok=True)
        except Exception:
            pass
