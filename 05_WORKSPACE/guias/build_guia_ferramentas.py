from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUT = "/Users/user/Downloads/Kit-Piloto-Automatico-V30-DISTRIB/06_OUTPUTS/2026-07-07_guia-ferramentas-codex/Guia_plugins_ferramentas_automacoes_Codex.docx"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_width(cell, width):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = OxmlElement("w:tcW")
    tc_w.set(qn("w:w"), str(width))
    tc_w.set(qn("w:type"), "dxa")
    tc_pr.append(tc_w)


def add_table(doc, rows):
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    headers = ["Nome", "Tipo", "O que faz", "Onde fica / status"]
    widths = [2100, 1500, 3900, 1860]
    for idx, text in enumerate(headers):
        cell = table.rows[0].cells[idx]
        cell.text = text
        set_cell_shading(cell, "E8EEF5")
        set_cell_width(cell, widths[idx])
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(31, 77, 120)
    tr_pr = table.rows[0]._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)

    for row in rows:
        cells = table.add_row().cells
        values = [row["nome"], row["tipo"], row["faz"], row["onde"]]
        for idx, value in enumerate(values):
            cells[idx].text = value
            set_cell_width(cells[idx], widths[idx])
            cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            for p in cells[idx].paragraphs:
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.size = Pt(8.5)
    doc.add_paragraph()


def add_note(doc, title, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, "F4F6F9")
    set_cell_width(cell, 9360)
    p = cell.paragraphs[0]
    run = p.add_run(title + ": ")
    run.bold = True
    run.font.color.rgb = RGBColor(31, 58, 95)
    run.font.size = Pt(10)
    run2 = p.add_run(text)
    run2.font.size = Pt(10)
    doc.add_paragraph()


sections = [
    {
        "title": "Plugins e Capacidades do Codex",
        "intro": "Recursos disponíveis na conversa ou no ambiente Codex para criar, revisar, automatizar e operar arquivos.",
        "rows": [
            {"nome": "Imagegen", "tipo": "Plugin / skill visual", "faz": "Gera ou edita imagens bitmap a partir de descrição ou imagem de referência.", "onde": "Skill disponível no Codex."},
            {"nome": "OpenAI Docs", "tipo": "Skill de documentação", "faz": "Consulta documentação oficial de produtos OpenAI e ajuda a escolher modelos, APIs e padrões atuais.", "onde": "Skill disponível no Codex."},
            {"nome": "Documents", "tipo": "Skill Word / DOCX", "faz": "Cria, edita e valida documentos Word com renderização visual para conferir layout.", "onde": "Skill usada para gerar este guia."},
            {"nome": "PDF", "tipo": "Skill PDF", "faz": "Lê, cria, renderiza e verifica PDFs quando o layout visual importa.", "onde": "Skill disponível no Codex."},
            {"nome": "Presentations", "tipo": "Skill slides", "faz": "Cria e edita apresentações PowerPoint ou materiais destinados ao Google Slides.", "onde": "Skill disponível no Codex."},
            {"nome": "Spreadsheets", "tipo": "Skill planilhas", "faz": "Cria, edita e analisa XLSX, CSV e planilhas com fórmulas, gráficos e tabelas.", "onde": "Skill disponível no Codex."},
            {"nome": "Template Creator", "tipo": "Skill de templates", "faz": "Cria templates reutilizáveis a partir de documentos, apresentações ou planilhas.", "onde": "Skill disponível no Codex."},
            {"nome": "Browser in-app", "tipo": "Plugin navegador", "faz": "Abre, testa, clica e tira screenshots do navegador interno do Codex.", "onde": "Plugin browser."},
            {"nome": "Chrome Control", "tipo": "Plugin navegador externo", "faz": "Controla o Chrome do usuário quando precisa aproveitar sessão logada, abas ou extensões.", "onde": "Plugin chrome."},
            {"nome": "Tool Search", "tipo": "Descoberta de ferramentas", "faz": "Localiza ferramentas e conectores adicionais que podem ser ativados sob demanda.", "onde": "Ferramenta do Codex."},
            {"nome": "Plugin Installer", "tipo": "Instalação de plugin/conector", "faz": "Lista e solicita instalação de plugins ou conectores quando você pede algo específico.", "onde": "Ferramentas list_available_plugins_to_install e request_plugin_install."},
        ],
    },
    {
        "title": "Comandos Principais do Kit",
        "intro": "Comandos operacionais que organizam tarefas, acessos, contexto e revisão de qualidade.",
        "rows": [
            {"nome": "Atualizar imóveis na planta", "tipo": "Comando / automação assistida", "faz": "Compara fonte oficial de construtora com site da Impar e, com aprovação, atualiza imóveis no Imobibrasil.", "onde": "00_OS/commands/atualizar-apartamentos-na-planta.md"},
            {"nome": "Instalar KPA30", "tipo": "Wizard de instalação", "faz": "Instala e configura o Kit V30 em 7 etapas: dependências, .env, MCPs, Meta CLI, onboarding e primeira tarefa.", "onde": "00_OS/commands/instalar-kpa30.md"},
            {"nome": "Start Here", "tipo": "Comando de inicialização", "faz": "Coloca o kit em estado operacional lendo índice, manifesto, contexto e ledger.", "onde": "00_OS/commands/start-here.md"},
            {"nome": "Nova Task", "tipo": "Roteador de trabalho", "faz": "Transforma um pedido novo em task com owner, modelo, gate e registro no ledger.", "onde": "00_OS/commands/nova-task.md"},
            {"nome": "Preflight de acessos", "tipo": "Checklist de segurança", "faz": "Confere cliente, pastas, acessos, permissões e limites antes de operar ferramenta real.", "onde": "00_OS/commands/preflight-acessos.md"},
            {"nome": "Review Gate", "tipo": "Revisão de qualidade", "faz": "Valida uma entrega pelo gate certo e devolve problemas, score e correções.", "onde": "00_OS/commands/review-gate.md"},
            {"nome": "Rodar Pipeline", "tipo": "Pipeline V30", "faz": "Executa demandas com várias fases, bloqueios e gates sequenciais.", "onde": "00_OS/commands/rodar-pipeline.md"},
            {"nome": "Compactar Contexto", "tipo": "Gestão de contexto", "faz": "Reduz o contexto ativo sem perder decisões, premissas, provas, gaps e próxima tarefa.", "onde": "00_OS/commands/compactar-contexto.md"},
            {"nome": "WhatsApp System", "tipo": "Comando WhatsApp", "faz": "Cria ou revisa sistema de WhatsApp com prospecção, SDR, sucesso, follow-up e Cowork.", "onde": "00_OS/commands/whatsapp-system.md"},
            {"nome": "Gerar contrato de locação", "tipo": "Script", "faz": "Script local para gerar contrato de locação conforme modelo operacional do kit.", "onde": "00_OS/commands/gerar-contrato-locacao.py"},
        ],
    },
    {
        "title": "WhatsApp, Atendimento e CRM",
        "intro": "Ferramentas para organizar atendimento, SDR, SAC, follow-up, memória e integração com WhatsApp/Cowork.",
        "rows": [
            {"nome": "WhatsApp Stack", "tipo": "Sistema operacional", "faz": "Estrutura bots, fluxos, handoff humano, contexto, QA e documentos para WhatsApp e Cowork.", "onde": "12_WHATSAPP_STACK/README.md"},
            {"nome": "WhatsApp Orchestrator", "tipo": "Agente", "faz": "Define rota, objetivo da conversa, insumos e handoff entre bots.", "onde": "12_WHATSAPP_STACK/agents/whatsapp-orchestrator.md"},
            {"nome": "Prospecting Bot", "tipo": "Agente", "faz": "Cuida de abordagem fria ou morna, abertura de conversa e permissão para continuar.", "onde": "12_WHATSAPP_STACK/agents/prospecting-bot.md"},
            {"nome": "SDR Attendant", "tipo": "Agente", "faz": "Faz atendimento consultivo, qualificação, objeções, agendamento e handoff comercial.", "onde": "12_WHATSAPP_STACK/agents/sdr-attendant.md"},
            {"nome": "Sales Follow-up Bot", "tipo": "Agente", "faz": "Faz follow-up de oportunidades, recupera no-show e ajuda no fechamento.", "onde": "12_WHATSAPP_STACK/agents/sales-followup-bot.md"},
            {"nome": "Customer Success Bot", "tipo": "Agente", "faz": "Faz onboarding, check-ins, reativação e sinalização de risco de churn.", "onde": "12_WHATSAPP_STACK/agents/customer-success-bot.md"},
            {"nome": "Conversation QA", "tipo": "Agente de revisão", "faz": "Valida tom, clareza, LGPD, risco de automação e limites do bot.", "onde": "12_WHATSAPP_STACK/agents/conversation-qa.md"},
            {"nome": "Cowork Automation Architect", "tipo": "Agente técnico", "faz": "Gera documentos, schemas, estados e regras para rodar no Cowork.", "onde": "12_WHATSAPP_STACK/agents/cowork-automation-architect.md"},
            {"nome": "Dashboard WhatsApp por setores", "tipo": "Dashboard local", "faz": "Mostra leads por SDR, Atendimento, SAC, Jurídico, Financeiro e RH, com resumo e memória por cliente.", "onde": "06_OUTPUTS/2026-07-06_dashboard-whatsapp-setores/index.html | draft seguro"},
            {"nome": "Bridge Webhook do Dashboard", "tipo": "Ponte local", "faz": "Recebe payload de WhatsApp/Cowork/n8n/Make/Zapier e atualiza clientes.json do dashboard.", "onde": "18_AUTOMATION_STACK/impar-dashboard-whatsapp-setores/bridge-server.js | draft"},
            {"nome": "Memória por setor", "tipo": "Schema / Obsidian", "faz": "Define memória grande por cliente, mantendo cada cliente em um único setor.", "onde": "05_WORKSPACE/clientes/impar-imoveis/whatsapp/memoria-setores.yaml"},
            {"nome": "Chatwoot / Oracle", "tipo": "Plano de instalação", "faz": "Documenta plano, cérebro de atendimento e instalação Oracle para central de atendimento.", "onde": "05_WORKSPACE/clientes/impar-imoveis/whatsapp/chatwoot/"},
            {"nome": "Playbook de Atendimento", "tipo": "Documento operacional", "faz": "Padroniza como atender, qualificar e conduzir conversas imobiliárias.", "onde": "05_WORKSPACE/clientes/impar-imoveis/whatsapp/playbook-atendimento.md"},
            {"nome": "Triagem de lead novo", "tipo": "Fluxo WhatsApp", "faz": "Ajuda a classificar lead novo, interesse e próxima ação.", "onde": "05_WORKSPACE/clientes/impar-imoveis/whatsapp/triagem-lead-novo.md"},
            {"nome": "Follow-up WhatsApp", "tipo": "Sequências de mensagem", "faz": "Cria sequências de reengajamento, follow-up e retorno de leads.", "onde": "06_OUTPUTS/2026-06-21_follow-up-whatsapp/"},
            {"nome": "Master Prompt Papo AI", "tipo": "Prompt operacional", "faz": "Centraliza instruções para atendimento imobiliário no Papo AI.", "onde": "05_WORKSPACE/clientes/impar-imoveis/whatsapp/master-prompt-papo-ai.md"},
        ],
    },
    {
        "title": "Automações de Processos",
        "intro": "Automações documentadas ou já testadas no kit. Escrita real em cliente, CRM, WhatsApp ou nota fiscal exige confirmação humana.",
        "rows": [
            {"nome": "Automation Stack", "tipo": "Sistema de automações", "faz": "Transforma processos em blueprint, SOP, gatilhos, handoffs, testes e rollback.", "onde": "18_AUTOMATION_STACK/README.md"},
            {"nome": "Automation Orchestrator", "tipo": "Agente", "faz": "Entry point para processos, SOPs, automações e integrações.", "onde": "18_AUTOMATION_STACK/agents/automation-orchestrator.md"},
            {"nome": "Editor Cinematográfico", "tipo": "Automação de vídeo", "faz": "Converte vídeos para Reels, aplica tratamento visual, áudio, cortes de silêncio e legenda quando fornecida.", "onde": "18_AUTOMATION_STACK/cinematic-video-editor/ | draft funcional"},
            {"nome": "Clarear modelo no vídeo", "tipo": "Entrega de vídeo", "faz": "Clareou o modelo a partir de 3 segundos mantendo características originais do vídeo.", "onde": "06_OUTPUTS/2026-07-07_video-2-clareado/"},
            {"nome": "Vídeo imobiliário cinematográfico", "tipo": "Entrega de vídeo", "faz": "Montou vídeo vertical com cenas selecionadas, voz tratada, pausas cortadas e trilha leve.", "onde": "06_OUTPUTS/2026-07-07_video-imobiliario-cinematico/"},
            {"nome": "Rogga x Impar x Imobibrasil", "tipo": "Automação imobiliária", "faz": "Compara valores oficiais Rogga com site público da Impar e prepara atualização no CRM após aprovação.", "onde": "18_AUTOMATION_STACK/impar-atualizacao-rogga-imobibrasil/ | draft"},
            {"nome": "Grupo JM x Impar x Imobibrasil", "tipo": "Automação imobiliária", "faz": "Compara tabelas/valores do Grupo JM com site da Impar e prepara atualização no CRM após aprovação.", "onde": "18_AUTOMATION_STACK/impar-atualizacao-grupo-jm-imobibrasil/ | draft"},
            {"nome": "Fila de imóveis Rogga", "tipo": "Base CSV", "faz": "Lista imóveis da Impar que dependem de atualização por fonte Rogga.", "onde": "05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-rogga.csv"},
            {"nome": "Fila de imóveis Grupo JM", "tipo": "Base CSV", "faz": "Lista imóveis da Impar que dependem de atualização por fonte Grupo JM.", "onde": "05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-grupo-jm.csv"},
            {"nome": "Fila geral apartamentos na planta", "tipo": "Base CSV", "faz": "Agenda geral para atualização de apartamentos na planta, incluindo construtoras e fontes futuras.", "onde": "05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-apartamentos-na-planta.csv"},
            {"nome": "NF-em Joinville", "tipo": "Automação fiscal", "faz": "Emite notas fiscais de serviço no portal NF-em Joinville após pagamento confirmado no Asaas.", "onde": "18_AUTOMATION_STACK/nfem-joinville/ | dry_run por padrão"},
            {"nome": "Webhook Asaas para NF-em", "tipo": "Servidor webhook", "faz": "Recebe evento de boleto pago, valida assinatura, evita duplicidade e dispara emissão de nota.", "onde": "18_AUTOMATION_STACK/nfem-joinville/src/webhook_server.py"},
            {"nome": "CLI NF-em", "tipo": "Ferramenta de linha de comando", "faz": "Permite simular, emitir nota por pagamento, listar pendentes e emitir mês inteiro.", "onde": "18_AUTOMATION_STACK/nfem-joinville/src/cli.py"},
        ],
    },
    {
        "title": "Conectores MCP e Integrações",
        "intro": "Conectores documentados para ligar o kit a ferramentas externas. Tokens e OAuth devem ficar fora do kit.",
        "rows": [
            {"nome": "Composio Rube", "tipo": "MCP principal", "faz": "Conecta 1000+ apps como Drive, Slack, Notion, Gmail, GitHub, HubSpot, Figma e Microsoft 365.", "onde": "20_MCP_SETUP/connectors/composio-rube.md"},
            {"nome": "WhatsApp MCP", "tipo": "MCP WhatsApp Web", "faz": "Permite ler e enviar mensagens pelo WhatsApp Web quando configurado e autorizado.", "onde": "20_MCP_SETUP/connectors/whatsapp-mcp.md"},
            {"nome": "Google Drive", "tipo": "MCP / conector", "faz": "Acessa arquivos no Drive, importa/exporta documentos e serve como fonte para planilhas e PDFs.", "onde": "20_MCP_SETUP/connectors/google-drive.md"},
            {"nome": "Gmail", "tipo": "MCP / conector", "faz": "Lê e opera e-mails para fluxos de atendimento, códigos, follow-up ou automações.", "onde": "20_MCP_SETUP/connectors/gmail.md"},
            {"nome": "Notion", "tipo": "MCP / conector", "faz": "Integra bases e páginas do Notion, normalmente via Rube.", "onde": "20_MCP_SETUP/connectors/notion.md"},
            {"nome": "Slack", "tipo": "MCP / conector", "faz": "Integra canais, mensagens e notificações de equipe.", "onde": "20_MCP_SETUP/connectors/slack.md"},
            {"nome": "Meta Ads", "tipo": "MCP / CLI", "faz": "Ajuda a operar Facebook/Instagram Ads via Rube ou CLI, com confirmação para alterações reais.", "onde": "20_MCP_SETUP/connectors/meta-ads.md"},
            {"nome": "Playwright", "tipo": "Automação de navegador", "faz": "Automatiza browser, screenshots, auditoria de páginas e testes visuais.", "onde": "20_MCP_SETUP/connectors/playwright.md"},
            {"nome": "Firecrawl", "tipo": "Scraper / pesquisa", "faz": "Coleta páginas e dados externos para pesquisa, concorrentes e auditorias.", "onde": "20_MCP_SETUP/connectors/firecrawl.md"},
            {"nome": "GitHub", "tipo": "MCP versionamento", "faz": "Integra repositórios, issues, PRs e versionamento de projetos.", "onde": "20_MCP_SETUP/connectors/github.md"},
            {"nome": "Filesystem", "tipo": "MCP arquivo local", "faz": "Permite acesso a pastas locais autorizadas sem ficar pedindo permissão repetidamente.", "onde": "20_MCP_SETUP/connectors/filesystem.md"},
        ],
    },
    {
        "title": "Ferramentas e Entregas de Produção",
        "intro": "Apps, vídeos, dashboards e materiais criados no kit para uso direto ou como base de novas versões.",
        "rows": [
            {"nome": "App Finanças iOS MVP", "tipo": "Web app local", "faz": "Registra entradas, saídas, status, filtros, resumo financeiro, PIN local e exportação CSV.", "onde": "06_OUTPUTS/2026-07-03_app-financas-ios-mvp/"},
            {"nome": "Gerador de vídeo imobiliário", "tipo": "Ferramenta local", "faz": "Monta vídeos verticais de empreendimentos com imagens, textos editáveis e exportação WebM.", "onde": "06_OUTPUTS/2026-07-05_gerador-video-empreendimento/"},
            {"nome": "Vídeo empreendimento geminados", "tipo": "Vídeo final", "faz": "Vídeo MP4 pronto para postagem usando fotos reais, localização e simulação visual da obra.", "onde": "06_OUTPUTS/2026-07-05_video-empreendimento-geminados/"},
            {"nome": "Comparação Rogga lote 01", "tipo": "Relatório imobiliário", "faz": "Compara valores Rogga x site público Impar para identificar anúncios que precisam revisão.", "onde": "06_OUTPUTS/2026-07-05_comparacao-rogga-lote-01/"},
            {"nome": "Comparação Grupo JM lote 01", "tipo": "Relatório imobiliário", "faz": "Compara valores Grupo JM x site público Impar e recomenda revisão/atualização.", "onde": "06_OUTPUTS/2026-07-05_comparacao-grupo-jm-lote-01/"},
            {"nome": "Piloto Baviera Rogga", "tipo": "Relatório piloto", "faz": "Testa leitura de fases/tabelas Rogga para definir menor unidade residencial válida.", "onde": "06_OUTPUTS/2026-07-05_piloto-baviera-rogga-impar/"},
            {"nome": "Master Prompt Follow-up Impar", "tipo": "Prompt comercial", "faz": "Centraliza instruções para follow-up imobiliário da Impar.", "onde": "06_OUTPUTS/2026-06-25_master-prompt-followup-impar-imoveis/"},
            {"nome": "Cartões social Jonata Impar", "tipo": "Conteúdo social", "faz": "Cartões e textos de publicação para redes sociais.", "onde": "06_OUTPUTS/social-jonata-impar/"},
        ],
    },
    {
        "title": "Templates, Squads e Builder Kit",
        "intro": "Componentes para padronizar novos clientes, novas tarefas e expansão do kit.",
        "rows": [
            {"nome": "Templates Operacionais", "tipo": "Templates de estado", "faz": "Fornece estrutura para cliente, projeto, output final e task avulsa.", "onde": "10_TEMPLATES_OPERACIONAIS/"},
            {"nome": "Cliente Template", "tipo": "Template de cliente", "faz": "Cria contexto mínimo do cliente: context, state, proofs e outputs.", "onde": "10_TEMPLATES_OPERACIONAIS/cliente-template/"},
            {"nome": "Output Template", "tipo": "Template de entrega", "faz": "Padroniza pacote final e handoff de uma entrega.", "onde": "10_TEMPLATES_OPERACIONAIS/output-template/"},
            {"nome": "Squads Adaptativos", "tipo": "Arquitetura de agentes", "faz": "Monta squads por cliente, fase, canal e gargalo, evitando agentes genéricos.", "onde": "13_ADAPTIVE_SQUADS/"},
            {"nome": "Squad WhatsApp Revenue", "tipo": "Squad base", "faz": "Agrupa CoS, WhatsApp Orchestrator, SDR, Follow-up e QA para vendas/atendimento.", "onde": "13_ADAPTIVE_SQUADS/squad-catalog.md"},
            {"nome": "Squad Process Automation", "tipo": "Squad base", "faz": "Agrupa CoS, Automation Architect e QA para automatizar rotinas de cliente.", "onde": "13_ADAPTIVE_SQUADS/squad-catalog.md"},
            {"nome": "Forge / Builder Kit", "tipo": "Criador de extensões", "faz": "Cria novos agentes, skills, tasks, diretrizes e conectores MCP seguindo o padrão V30.", "onde": "21_BUILDER_KIT/"},
            {"nome": "Create Agent", "tipo": "Task Forge", "faz": "Contrato para criar um novo agente do kit.", "onde": "21_BUILDER_KIT/tasks/create-agent.md"},
            {"nome": "Create Skill", "tipo": "Task Forge", "faz": "Contrato para criar uma nova skill reutilizável.", "onde": "21_BUILDER_KIT/tasks/create-skill.md"},
            {"nome": "Create MCP Connector", "tipo": "Task Forge", "faz": "Contrato para documentar e padronizar um novo conector MCP.", "onde": "21_BUILDER_KIT/tasks/create-mcp-connector.md"},
        ],
    },
]


doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.75)
section.right_margin = Inches(0.75)

styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(10)
styles["Title"].font.name = "Calibri"
styles["Title"].font.size = Pt(24)
styles["Title"].font.color.rgb = RGBColor(11, 37, 69)
styles["Heading 1"].font.name = "Calibri"
styles["Heading 1"].font.size = Pt(16)
styles["Heading 1"].font.color.rgb = RGBColor(46, 116, 181)
styles["Heading 2"].font.name = "Calibri"
styles["Heading 2"].font.size = Pt(13)
styles["Heading 2"].font.color.rgb = RGBColor(46, 116, 181)

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("Guia de Plugins, Ferramentas e Automações")
run.bold = True
run.font.size = Pt(24)
run.font.color.rgb = RGBColor(11, 37, 69)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = subtitle.add_run("Kit Piloto Automático V30 + recursos disponíveis no Codex")
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(85, 85, 85)

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run("Atualizado em 07/07/2026")
r.font.size = Pt(10)
r.font.color.rgb = RGBColor(85, 85, 85)

add_note(
    doc,
    "Como usar este guia",
    "Procure pelo nome da ferramenta ou automação, veja o que ela faz e onde ela está no kit. Itens que mexem com WhatsApp real, CRM, nota fiscal, publicação ou dados sensíveis exigem confirmação humana antes de ativação ou escrita real.",
)

doc.add_heading("Resumo rápido", level=1)
summary = [
    "Comandos do kit: organizam tarefas, contexto, acessos, gates e pipelines.",
    "WhatsApp: fluxos, bots, dashboard por setores, memória de clientes e ponte webhook.",
    "Automações: imóveis na planta, Rogga, Grupo JM, NF-em Joinville e editor de vídeo.",
    "Conectores MCP: Rube, WhatsApp, Drive, Gmail, Notion, Slack, Meta Ads, Playwright, Firecrawl, GitHub e Filesystem.",
    "Produção: apps, vídeos, dashboards e relatórios já entregues em 06_OUTPUTS.",
    "Builder Kit: cria novos agentes, skills, tasks, diretrizes e conectores.",
]
for item in summary:
    p = doc.add_paragraph(style=None)
    p.style = doc.styles["Normal"]
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.add_run("• ").bold = True
    p.add_run(item)

for section_data in sections:
    heading = doc.add_heading(section_data["title"], level=1)
    heading.paragraph_format.keep_with_next = True
    p = doc.add_paragraph(section_data["intro"])
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    add_table(doc, section_data["rows"])

doc.add_heading("Regras de segurança para uso", level=1)
rules = [
    "Nunca pedir ou colar token, senha ou código sensível no chat.",
    "Leitura e comparação podem rodar em modo assistido; escrita real precisa de confirmação.",
    "Envio real de WhatsApp, alteração de CRM, emissão de nota, publicação e exclusão exigem aprovação humana.",
    "Automação nova deve ter trigger, teste, rollback e handoff humano antes de ser considerada pronta.",
    "Quando faltar dado, usar [A PREENCHER] em vez de inventar informação.",
]
for idx, item in enumerate(rules, start=1):
    doc.add_paragraph(f"{idx}. {item}")

doc.add_heading("Próximas melhorias sugeridas", level=1)
next_steps = [
    "Adicionar uma coluna de responsável por ferramenta quando houver equipe usando o kit.",
    "Separar um guia só de WhatsApp e atendimento, com fluxos por setor.",
    "Criar uma versão mensal deste inventário a partir do ledger e das pastas de output.",
    "Adicionar status operacional real: ativo, rascunho, pausado, precisa login, precisa aprovação.",
]
for item in next_steps:
    doc.add_paragraph("• " + item)

doc.save(OUT)
print(OUT)
