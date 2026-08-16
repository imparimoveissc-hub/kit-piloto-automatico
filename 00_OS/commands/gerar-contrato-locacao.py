#!/usr/bin/env python3
"""
Automação de Contratos de Locação - Kit Piloto Automático V30
Gera contrato de locação e termo de vistoria a partir dos modelos padrão.
Uso: python3 gerar-contrato-locacao.py

Nunca altera os arquivos originais de modelo.
"""

import os
import re
import sys
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

# ── Caminhos ──────────────────────────────────────────────────────────────────
DESKTOP = Path.home() / "Desktop"
MODELOS = DESKTOP / "Claude Desktop" / "Modelos de contrato " / "LOCAÇÃO"
MODELO_CONTRATO = MODELOS / "CONTRATO DE LOCAÇÃO - (LOFT) Seguro fiança atualizado - Exemplo - cópia.docx"
MODELO_VISTORIA = MODELOS / "TERMO DE VISTORIA PARA LOCAÇÃO - Exemplo - Padrão .docx"
MODELO_ADMIN = MODELOS / "CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE ADMINISTRAÇÃO IMOBILIÁRIA - IMPAR.docx"

SKILL_DIR = Path("/Users/user/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/1472b09e-7f66-40a4-bbef-ed14367a8b7c/d7f0e942-03a7-42a2-bd25-9013cbe4c3b1/skills/docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# ── Helpers XML ───────────────────────────────────────────────────────────────

def _tag(name):
    return f"{{{W_NS}}}{name}"

def has_yellow(run_elem):
    rpr = run_elem.find(_tag("rPr"))
    if rpr is None:
        return False
    hl = rpr.find(_tag("highlight"))
    return hl is not None and hl.get(_tag("val")) == "yellow"


def replace_yellow_text_in_paragraph(para, new_text):
    """
    Substitui todo o texto amarelo de um parágrafo pelo new_text.
    Coloca o texto no primeiro run amarelo e esvazia os demais.
    Remove o highlight do parágrafo após substituição.
    """
    from lxml import etree

    yellow_runs = [r for r in para.iter(_tag("r")) if has_yellow(r)]
    if not yellow_runs:
        return

    # Coloca o texto no primeiro run amarelo
    first = yellow_runs[0]
    t = first.find(_tag("t"))
    if t is None:
        t = etree.SubElement(first, _tag("t"))
    t.text = new_text
    if new_text and (new_text[0] == " " or new_text[-1] == " "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    # Remove highlight do primeiro run
    rpr = first.find(_tag("rPr"))
    if rpr is not None:
        hl = rpr.find(_tag("highlight"))
        if hl is not None:
            rpr.remove(hl)

    # Esvazia e remove highlight dos runs restantes
    for r in yellow_runs[1:]:
        t = r.find(_tag("t"))
        if t is not None:
            t.text = ""
        rpr = r.find(_tag("rPr"))
        if rpr is not None:
            hl = rpr.find(_tag("highlight"))
            if hl is not None:
                rpr.remove(hl)

    # Remove highlight do pPr também
    ppr = para.find(_tag("pPr"))
    if ppr is not None:
        rpr_p = ppr.find(_tag("rPr"))
        if rpr_p is not None:
            hl = rpr_p.find(_tag("highlight"))
            if hl is not None:
                rpr_p.remove(hl)


def get_paragraph_yellow_text(para):
    """Retorna texto concatenado de todos os runs amarelos do parágrafo."""
    text = ""
    for r in para.iter(_tag("r")):
        if has_yellow(r):
            t = r.find(_tag("t"))
            text += (t.text or "") if t is not None else ""
    return text


def get_paragraph_full_text(para):
    """Retorna texto completo do parágrafo (amarelo ou não)."""
    text = ""
    for r in para.iter(_tag("r")):
        t = r.find(_tag("t"))
        text += (t.text or "") if t is not None else ""
    return text


def edit_docx_xml(docx_path, edit_fn, output_path):
    """Descompacta, edita via edit_fn(tree) e recompacta."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(docx_path, "r") as z:
            z.extractall(tmp)

        doc_xml = tmp / "word" / "document.xml"
        from lxml import etree
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(str(doc_xml), parser)
        edit_fn(tree)

        tree.write(str(doc_xml), xml_declaration=True, encoding="UTF-8", standalone=True)

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for f in tmp.rglob("*"):
                if f.is_file():
                    zout.write(f, f.relative_to(tmp))


# ── Perguntas ─────────────────────────────────────────────────────────────────

def perguntar(label, obrigatorio=True, padrao=None):
    valor = input(f"  {label}: ").strip()
    if not valor and padrao:
        return padrao
    if not valor and obrigatorio:
        print(f"  ⚠️  Campo obrigatório. Digite novamente.")
        return perguntar(label, obrigatorio, padrao)
    return valor


def coletar_dados():
    print("\n" + "="*60)
    print("  DADOS DO CONTRATO DE LOCAÇÃO")
    print("="*60 + "\n")

    d = {}

    print("── LOCADOR / PROPRIETÁRIO ──")
    d["locador_nome"] = perguntar("Nome completo do locador")
    d["locador_nacionalidade"] = perguntar("Nacionalidade", padrao="brasileiro(a)")
    d["locador_profissao"] = perguntar("Profissão")
    d["locador_rg"] = perguntar("RG (ex: 6.776.453 SSP/SC)")
    d["locador_cpf"] = perguntar("CPF (ex: 105.511.869-17)")
    d["locador_endereco"] = perguntar("Endereço completo (rua, nº, bairro, cidade/UF)")
    d["locador_estado_civil"] = perguntar("Estado civil (ex: solteiro(a), casado(a) em regime de comunhão universal de bens)")
    d["locador_2"] = perguntar("2º locador/cônjuge? (deixe em branco se não tiver)", obrigatorio=False)
    if d["locador_2"]:
        d["locador_2_nacionalidade"] = perguntar("Nacionalidade do 2º locador", padrao="brasileiro(a)")
        d["locador_2_profissao"] = perguntar("Profissão do 2º locador")
        d["locador_2_rg"] = perguntar("RG do 2º locador")
        d["locador_2_cpf"] = perguntar("CPF do 2º locador")
        d["locador_2_endereco"] = perguntar("Endereço do 2º locador")

    print("\n── LOCATÁRIO / INQUILINO ──")
    d["locatario_nome"] = perguntar("Nome completo do locatário")
    d["locatario_nacionalidade"] = perguntar("Nacionalidade", padrao="brasileiro(a)")
    d["locatario_profissao"] = perguntar("Profissão (deixe em branco se não tiver)", obrigatorio=False)
    d["locatario_rg"] = perguntar("RG (deixe em branco se não tiver)", obrigatorio=False)
    d["locatario_cpf"] = perguntar("CPF (ex: 028.615.131-60)")
    d["locatario_endereco"] = perguntar("Endereço completo (rua, nº, bairro, cidade/UF)")

    print("\n── IMÓVEL ──")
    d["uso"] = perguntar("Uso (RESIDENCIAL ou COMERCIAL)", padrao="RESIDENCIAL").upper()
    d["imovel_endereco"] = perguntar("Endereço completo do imóvel (Rua, nº, bairro, cidade/UF)")
    d["imovel_denominacao"] = perguntar("Denominação (ex: Apartamento 102, Tipo A, Bloco 01, Residencial Oliveira)")
    d["imovel_area_privativa"] = perguntar("Área privativa (ex: 43,37m²)", obrigatorio=False)
    d["imovel_area_total"] = perguntar("Área total (ex: 77,67m²)", obrigatorio=False)
    d["imovel_matricula"] = perguntar("Matrícula nº")
    d["imovel_inscricao"] = perguntar("Inscrição imobiliária nº")

    print("\n── PRAZOS ──")
    d["prazo_meses"] = perguntar("Prazo em meses (ex: 12)", padrao="12")
    prazo_int = int(d["prazo_meses"])
    d["prazo_extenso"] = perguntar(f"Prazo por extenso (ex: doze)")
    d["inicio"] = perguntar("Data de início (ex: 10/08/2025)")
    d["fim"] = perguntar("Data de encerramento (ex: 09/08/2026)")
    d["primeiro_venc"] = perguntar("Data do 1º vencimento do aluguel (ex: 10/08/2025)")
    d["dia_venc"] = perguntar("Dia de vencimento mensal (ex: 10)")

    print("\n── VALORES ──")
    d["aluguel"] = perguntar("Valor do aluguel (ex: R$ 1.100,00)")
    d["aluguel_extenso"] = perguntar("Valor do aluguel por extenso (ex: mil e cem reais)")
    d["iptu"] = perguntar("Valor do IPTU (ex: R$ 0,00 ou deixe em branco se incluso/isento)", obrigatorio=False)
    d["taxa_lixo"] = perguntar("Valor da taxa de lixo", obrigatorio=False)
    d["condominio"] = perguntar("Valor do condomínio (deixe em branco se não tiver)", obrigatorio=False)
    d["fianca"] = perguntar("Valor da fiança locatícia")
    d["seguro_incendio"] = perguntar("Valor do seguro incêndio")
    d["valor_total"] = perguntar("Valor total (aluguel + IPTU + lixo + fiança + seguro + condomínio)")

    print("\n── DATA E CONDIÇÕES ──")
    d["data_contrato"] = perguntar("Data do contrato (ex: 29 de Maio de 2025)")
    d["condicao_especifica"] = perguntar("Alguma condição específica e única para este contrato? (deixe em branco se não)", obrigatorio=False)

    print("\n── VISTORIA ──")
    d["ar_condicionado"] = perguntar("Ar condicionado (descreva ou 'Não possui ar condicionado')")
    d["demais_acessorios"] = perguntar("Demais acessórios (descreva ou 'Não possui acessórios adicionais')")
    d["chaves"] = perguntar("Chaves entregues (descreva, ex: 2 cópias da chave principal)")
    d["fotos_dir"] = perguntar("Caminho da pasta com as fotos (deixe em branco se não tiver)", obrigatorio=False)

    return d


# ── Geração do texto dos campos ───────────────────────────────────────────────

def montar_locador(d):
    texto = f"LOCADOR(A)(ES): {d['locador_nome']}, {d['locador_nacionalidade']}, {d['locador_profissao']}, portador(a) da carteira de identidade RG nº {d['locador_rg']} e inscrito(a) no CPF nº {d['locador_cpf']}, residente e domiciliado(a) à {d['locador_endereco']}"
    if d.get("locador_2"):
        texto += f"; e {d['locador_2']}, {d['locador_2_nacionalidade']}, {d['locador_2_profissao']}, portador(a) da carteira de identidade RG nº {d['locador_2_rg']} e inscrito(a) no CPF nº {d['locador_2_cpf']}, residente e domiciliado(a) à {d['locador_2_endereco']}"
    texto += "."
    return texto


def montar_locatario(d):
    partes = [d["locatario_nome"], d["locatario_nacionalidade"]]
    if d.get("locatario_profissao"):
        partes.append(d["locatario_profissao"])
    if d.get("locatario_rg"):
        partes.append(f"portador(a) da carteira de identidade RG nº {d['locatario_rg']}")
    partes.append(f"inscrito(a) no CPF nº {d['locatario_cpf']}")
    partes.append(f"residente e domiciliado(a) à {d['locatario_endereco']}")
    return "LOCATÁRIO(A): " + ", ".join(partes) + "."


def montar_imovel_contrato(d):
    texto = f"imóvel situado à {d['imovel_endereco']}, denominado {d['imovel_denominacao']}"
    if d.get("imovel_area_privativa"):
        texto += f", composto por área privativa de {d['imovel_area_privativa']}"
    if d.get("imovel_area_total"):
        texto += f" e área total de {d['imovel_area_total']}"
    texto += f", matrícula nº {d['imovel_matricula']}, inscrição imobiliária nº {d['imovel_inscricao']},"
    return texto


def montar_prazo(d):
    mes_inicio = d["inicio"].split("/")[1] if "/" in d["inicio"] else ""
    ano_inicio = d["inicio"].split("/")[2] if "/" in d["inicio"] else ""
    # Mês seguinte para encargos
    meses_nomes = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
    try:
        mes_idx = int(mes_inicio) - 1
        mes_seguinte = meses_nomes[(mes_idx + 1) % 12]
    except:
        mes_seguinte = "mês seguinte"

    texto = (
        f"O prazo de vigência da presente locação é de {d['prazo_meses']} ({d['prazo_extenso']}) meses, "
        f"iniciando-se em {d['inicio']} e encerrando-se em {d['fim']}. "
        f"O primeiro aluguel vencerá em {d['primeiro_venc']}, e os pagamentos mensais subsequentes vencerão "
        f"todo dia {d['dia_venc']} de cada mês, incluindo o último aluguel e encargos proporcionais referentes "
        f"ao período final da locação. Caso não haja renovação expressa ou prorrogação admitida em lei, "
        f"o(a) LOCATÁRIO(A) deverá restituir o imóvel ao final da vigência, observadas as obrigações de "
        f"vistoria final, quitação de encargos e entrega das chaves. As taxas referentes a condomínio, água, "
        f"luz e gás, de responsabilidade do(a) LOCATÁRIO(A), iniciam-se no mês de {mes_seguinte} de {ano_inicio} "
        f"e permanecem devidas até a efetiva entrega das chaves, salvo renovação do contrato, hipótese em que "
        f"o(a) LOCATÁRIO(A) continuará responsável pelo aluguel e pelos encargos locatícios."
    )
    return texto


def montar_aluguel(d):
    texto = (
        f"O aluguel mensal será de {d['aluguel']} ({d['aluguel_extenso']}), a ser pago ao mandatário do(a) "
        f"LOCADOR(A), mediante Pix ou boleto bancário em nome de Impar Imóveis LTDA, inscrita no CNPJ nº "
        f"50.886.299/0001-00, até o dia {d['dia_venc']} de cada mês, com primeiro vencimento em "
        f"{d['primeiro_venc']} e vencimentos subsequentes no mesmo dia dos meses seguintes."
    )
    return texto


def montar_data_contrato(d):
    return f"Joinville (SC) em {d['data_contrato']}."


# ── Edição do Contrato de Locação ─────────────────────────────────────────────

def editar_contrato(d, input_path, output_path):
    locador_text = montar_locador(d)
    locatario_text = montar_locatario(d)
    imovel_text = montar_imovel_contrato(d)
    prazo_text = montar_prazo(d)
    aluguel_text = montar_aluguel(d)
    data_text = montar_data_contrato(d)

    def edit_fn(tree):
        root = tree.getroot()
        for para in root.iter(_tag("p")):
            yellow = get_paragraph_yellow_text(para).strip()
            if not yellow:
                continue
            if yellow.startswith("LOCADOR(A)(ES):"):
                replace_yellow_text_in_paragraph(para, locador_text)
            elif yellow.startswith("LOCATÁRIO(A):"):
                replace_yellow_text_in_paragraph(para, locatario_text)
            elif "imóvel situado à" in yellow or "imóvel situado a" in yellow.lower():
                replace_yellow_text_in_paragraph(para, imovel_text)
            elif "prazo de vigência" in yellow or "prazo de vigencia" in yellow.lower():
                replace_yellow_text_in_paragraph(para, prazo_text)
            elif "aluguel mensal" in yellow.lower():
                replace_yellow_text_in_paragraph(para, aluguel_text)
            elif yellow.startswith("Joinville"):
                replace_yellow_text_in_paragraph(para, data_text)

    edit_docx_xml(input_path, edit_fn, output_path)
    print(f"  ✅ Contrato salvo: {output_path}")


# ── Edição do Termo de Vistoria ───────────────────────────────────────────────

def montar_locador_vistoria(d):
    texto = f"LOCADOR – {d['locador_nome']}, pessoa física, inscrito(a) no CPF {d['locador_cpf']}"
    if d.get("locador_rg"):
        texto += f" e RG n. {d['locador_rg']}"
    texto += f" residente e domiciliado(a) na {d['locador_endereco']}."
    return texto


def montar_locatario_vistoria(d):
    texto = f"LOCATÁRIA – {d['locatario_nome']}, pessoa física, inscrito(a) no CPF {d['locatario_cpf']}"
    if d.get("locatario_rg"):
        texto += f" e RG n. {d['locatario_rg']}"
    texto += f" residente e domiciliado(a) na {d['locatario_endereco']}."
    return texto


def montar_imovel_vistoria(d):
    uso = "EXCLUSIVAMENTE RESIDENCIAL" if d["uso"] == "RESIDENCIAL" else "EXCLUSIVAMENTE COMERCIAL"
    texto = f"imóvel localizado na {d['imovel_endereco']}, denominado {d['imovel_denominacao']}, para uso {uso}"
    if d.get("imovel_matricula"):
        texto += f", matrícula nº {d['imovel_matricula']}"
    if d.get("imovel_inscricao"):
        texto += f", inscrição imobiliária nº {d['imovel_inscricao']},"
    return texto


def editar_vistoria(d, input_path, output_path):
    locador_v = montar_locador_vistoria(d)
    locatario_v = montar_locatario_vistoria(d)
    imovel_v = montar_imovel_vistoria(d)
    ar_cond = d.get("ar_condicionado", "Não possui ar condicionado.")
    acessorios = d.get("demais_acessorios", "Não possui acessórios adicionais.")
    chaves = "13) CHAVES: " + d.get("chaves", "").lstrip("13) CHAVES: ")
    data_v = f"Joinville {d['data_contrato']}."

    def edit_fn(tree):
        root = tree.getroot()
        for para in root.iter(_tag("p")):
            yellow = get_paragraph_yellow_text(para).strip()
            full = get_paragraph_full_text(para).strip()
            if not yellow:
                continue
            if yellow.startswith("LOCADOR") and "LOCATÁRI" not in yellow and "LOCATARIO" not in yellow:
                replace_yellow_text_in_paragraph(para, locador_v)
            elif yellow.startswith("LOCATÁRIA") or yellow.startswith("LOCATARIO") or yellow.startswith("LOCATÁRIO"):
                replace_yellow_text_in_paragraph(para, locatario_v)
            elif "localizada na" in yellow or "localizado na" in yellow or "imóvel situado" in yellow.lower():
                replace_yellow_text_in_paragraph(para, imovel_v)
            elif "9)" in full and "AR CONDICIONADO" in full.upper():
                replace_yellow_text_in_paragraph(para, ar_cond)
            elif "DEMAIS ACESS" in full.upper():
                replace_yellow_text_in_paragraph(para, f"10) DEMAIS ACESSÓRIOS: {acessorios}")
            elif "13)" in full and "CHAVES" in full.upper():
                replace_yellow_text_in_paragraph(para, chaves)
            elif yellow.startswith("Joinville") and "de 20" in yellow:
                replace_yellow_text_in_paragraph(para, data_v)

    edit_docx_xml(input_path, edit_fn, output_path)
    print(f"  ✅ Termo de vistoria salvo: {output_path}")


# ── Contrato de Administração ─────────────────────────────────────────────────

def editar_contrato_admin(d, input_path, output_path):
    """
    Copia o contrato de administração e preenche CONTRATANTE e IMÓVEL
    com os mesmos dados do contrato de locação.
    """
    estado_civil = d.get("locador_estado_civil", "")
    contratante_bloco = (
        f"{d['locador_nome']}, {d['locador_nacionalidade']}, {estado_civil}, "
        f"{d['locador_profissao']}, RG nº {d['locador_rg']}, "
        f"CPF/CNPJ nº {d['locador_cpf']}, endereço {d['locador_endereco']}."
    )
    assinatura_bloco = f"{d['locador_nome']} | CPF: {d['locador_cpf']}"

    # Monta descrição do imóvel igual ao contrato de locação
    imovel_partes = [d["imovel_endereco"], f"denominado {d['imovel_denominacao']}"]
    if d.get("imovel_area_privativa") and "[A PREENCHER]" not in d.get("imovel_area_privativa",""):
        imovel_partes.append(f"área privativa de {d['imovel_area_privativa']}")
    if d.get("imovel_area_total") and "[A PREENCHER]" not in d.get("imovel_area_total",""):
        imovel_partes.append(f"área total de {d['imovel_area_total']}")
    imovel_partes.append(f"matrícula nº {d['imovel_matricula']}")
    imovel_partes.append(f"inscrição imobiliária nº {d['imovel_inscricao']}")
    imovel_bloco = ", ".join(imovel_partes) + "."

    def edit_fn(tree):
        W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        for r in tree.getroot().iter(f"{{{W}}}r"):
            t = r.find(f"{{{W}}}t")
            if t is None or not t.text:
                continue
            if "[NOME DO(A) PROPRIETÁRIO(A)]" in t.text:
                t.text = contratante_bloco
                if t.text[0] == " " or t.text[-1] == " ":
                    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            elif "[Endereço completo, matrícula" in t.text:
                t.text = imovel_bloco
            elif "[Nome do(a) contratante]" in t.text:
                t.text = t.text.replace(
                    "[Nome do(a) contratante] | CPF/CNPJ: [●]",
                    assinatura_bloco
                )

    edit_docx_xml(input_path, edit_fn, output_path)
    print(f"  ✅ Contrato de administração salvo: {output_path}")


def nome_arquivo_admin(d):
    prop = d["locador_nome"].split()[0] + " " + d["locador_nome"].split()[-1]
    loc = d["locatario_nome"].split()[0] + " " + d["locatario_nome"].split()[-1]
    local = extrair_rua_bairro(d["imovel_endereco"])
    return f"Contrato de Administração - {local} - {prop} x {loc}.docx"


# ── Naming ────────────────────────────────────────────────────────────────────

def extrair_rua_bairro(endereco_imovel):
    """Extrai 'Rua, nº e bairro' do endereço completo do imóvel."""
    # Remove cidade/UF se presente
    partes = endereco_imovel.split(",")
    # Usa as 3 primeiras partes (rua, nº, bairro)
    return ", ".join(p.strip() for p in partes[:3]) if len(partes) >= 3 else endereco_imovel


def nome_pasta(d, tipo="Locação"):
    local = extrair_rua_bairro(d["imovel_endereco"])
    prop = d["locador_nome"].split()[0] + " " + d["locador_nome"].split()[-1]
    loc = d["locatario_nome"].split()[0] + " " + d["locatario_nome"].split()[-1]
    return f"{tipo} - {local} - {prop} x {loc}"


def nome_arquivo_contrato(d):
    local = extrair_rua_bairro(d["imovel_endereco"])
    prop = d["locador_nome"].split()[0] + " " + d["locador_nome"].split()[-1]
    loc = d["locatario_nome"].split()[0] + " " + d["locatario_nome"].split()[-1]
    return f"Contrato de locação - {local} - {prop} x {loc}.docx"


def nome_arquivo_vistoria(d):
    local = extrair_rua_bairro(d["imovel_endereco"])
    prop = d["locador_nome"].split()[0] + " " + d["locador_nome"].split()[-1]
    loc = d["locatario_nome"].split()[0] + " " + d["locatario_nome"].split()[-1]
    return f"TERMO DE VISTORIA - {local} - {prop} x {loc}.docx"


def criar_pasta_destino(d, tipo="Locação"):
    """Cria pasta nova no Desktop para os documentos do contrato."""
    pasta_nome = nome_pasta(d, tipo)
    pasta = DESKTOP / pasta_nome
    # Se já existir, adiciona sufixo numérico para não sobrescrever
    if pasta.exists():
        i = 2
        while (DESKTOP / f"{pasta_nome} ({i})").exists():
            i += 1
        pasta = DESKTOP / f"{pasta_nome} ({i})"
    pasta.mkdir(parents=True, exist_ok=False)
    return pasta


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  GERADOR DE CONTRATO DE LOCAÇÃO - IMPAR IMÓVEIS")
    print("="*60)

    # Verificar modelos
    if not MODELO_CONTRATO.exists():
        print(f"\n❌ Modelo não encontrado: {MODELO_CONTRATO}")
        sys.exit(1)
    if not MODELO_VISTORIA.exists():
        print(f"\n❌ Modelo não encontrado: {MODELO_VISTORIA}")
        sys.exit(1)
    if not MODELO_ADMIN.exists():
        print(f"\n❌ Modelo não encontrado: {MODELO_ADMIN}")
        sys.exit(1)

    d = coletar_dados()

    print("\n── GERANDO DOCUMENTOS ──")

    # Cria pasta no Desktop
    pasta = criar_pasta_destino(d, tipo="Locação")
    print(f"\n  📁 Pasta criada: {pasta.name}")

    contrato_nome = nome_arquivo_contrato(d)
    vistoria_nome = nome_arquivo_vistoria(d)
    admin_nome = nome_arquivo_admin(d)

    contrato_dest = pasta / contrato_nome
    vistoria_dest = pasta / vistoria_nome
    admin_dest = pasta / admin_nome

    # Gera os 3 documentos
    print(f"\n  Gerando contrato de locação...")
    editar_contrato(d, MODELO_CONTRATO, contrato_dest)

    print(f"\n  Gerando termo de vistoria...")
    editar_vistoria(d, MODELO_VISTORIA, vistoria_dest)

    print(f"\n  Gerando contrato de administração...")
    editar_contrato_admin(d, MODELO_ADMIN, admin_dest)

    print("\n" + "="*60)
    print("  DOCUMENTOS GERADOS COM SUCESSO!")
    print("="*60)
    print(f"\n  📁 {pasta.name}/")
    print(f"     📄 {contrato_nome}")
    print(f"     📄 {vistoria_nome}")
    print(f"     📄 {admin_nome}")
    print(f"\n  Pasta salva no Desktop.")
    if d.get("fotos_dir"):
        print(f"\n  ⚠️  Fotos: insira manualmente no Termo de Vistoria")
        print(f"     Pasta informada: {d['fotos_dir']}")
    if d.get("condicao_especifica"):
        print(f"\n  ⚠️  Condição específica a inserir manualmente:")
        print(f"     {d['condicao_especifica']}")
    print()


if __name__ == "__main__":
    main()
