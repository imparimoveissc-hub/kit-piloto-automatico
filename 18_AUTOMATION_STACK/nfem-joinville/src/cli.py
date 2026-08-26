"""
CLI para operações manuais: testar, reprocessar, listar erros.

Uso:
  python -m src.cli emitir <payment_id>
  python -m src.cli simular
  python -m src.cli listar-erros
  python -m src.cli reprocessar <payment_id>
  python -m src.cli servidor
  python -m src.cli pendentes              # lista pagamentos do mês atual prontos para emitir
  python -m src.cli emitir-mes             # busca, mostra a lista, pede confirmação e emite tudo
  python -m src.cli emitir-manual --tipo venda|aluguel --cpf-cnpj <cpf/cnpj> --descricao "<texto>" --valor <valor>
                                           # emite uma nota avulsa (item 1005 venda / 1712 aluguel), fora do Asaas
                                           #   +flag --usar-sessao : roda headless com a sessão salva (uso remoto/desassistido)
                                           #   com certificado digital A1 configurado, roda headless sem captcha
  python -m src.cli login-manual           # abre o navegador para login manual e salva a sessão "quente" (pula o captcha depois)
"""

import asyncio
import calendar
import json
import sys
from datetime import date


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "emitir":
        if len(sys.argv) < 3:
            print("Uso: python -m src.cli emitir <payment_id>")
            sys.exit(1)
        from src.pipeline import processar_pagamento
        resultado = asyncio.run(processar_pagamento(sys.argv[2]))
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    elif cmd == "simular":
        _simular()

    elif cmd == "listar-erros":
        from src.idempotency import listar_erros
        erros = listar_erros()
        if not erros:
            print("Nenhum erro registrado.")
        else:
            print(json.dumps(erros, ensure_ascii=False, indent=2))

    elif cmd == "reprocessar":
        if len(sys.argv) < 3:
            print("Uso: python -m src.cli reprocessar <payment_id>")
            sys.exit(1)
        from src.idempotency import resetar_para_reprocessamento
        from src.pipeline import processar_pagamento
        resetar_para_reprocessamento(sys.argv[2])
        resultado = asyncio.run(processar_pagamento(sys.argv[2]))
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    elif cmd == "servidor":
        import uvicorn
        from src.config import WEBHOOK_HOST, WEBHOOK_PORT
        uvicorn.run("src.webhook_server:app", host=WEBHOOK_HOST, port=WEBHOOK_PORT, reload=False)

    elif cmd == "pendentes":
        pendentes = _buscar_pendentes_mes_atual()
        _imprimir_pendentes(pendentes)

    elif cmd == "emitir-mes":
        pendentes = _buscar_pendentes_mes_atual()
        _imprimir_pendentes(pendentes)
        if not pendentes:
            sys.exit(0)
        resposta = input(f"\nConfirma a emissão real dessas {len(pendentes)} notas? (digite SIM para confirmar): ")
        if resposta.strip().upper() != "SIM":
            print("Cancelado — nenhuma nota foi emitida.")
            sys.exit(0)
        _emitir_pendentes(pendentes)

    elif cmd == "emitir-manual":
        args = _parse_flags(sys.argv[2:])
        _emitir_manual(args)

    elif cmd == "login-manual":
        _login_manual()

    else:
        print(f"Comando desconhecido: {cmd}")
        print(__doc__)
        sys.exit(1)


def _buscar_pendentes_mes_atual() -> list[dict]:
    """
    Busca no Asaas todos os pagamentos RECEIVED/CONFIRMED do mês atual e
    cruza com clientes.json para achar quais já têm tudo pronto para emitir
    (e ainda não foram emitidos).
    """
    import httpx
    from src.config import ASAAS_API_KEY, ASAAS_BASE_URL
    from src.pipeline import _encontrar_config_cliente
    from src.idempotency import ja_emitida

    hoje = date.today()
    primeiro_dia = hoje.replace(day=1)
    ultimo_dia = hoje.replace(day=calendar.monthrange(hoje.year, hoje.month)[1])

    pagamentos = []
    with httpx.Client(timeout=30) as client:
        for status in ("RECEIVED", "CONFIRMED"):
            offset = 0
            while True:
                r = client.get(
                    f"{ASAAS_BASE_URL}/payments",
                    headers={"access_token": ASAAS_API_KEY},
                    params={
                        "status": status,
                        "paymentDate[ge]": primeiro_dia.isoformat(),
                        "paymentDate[le]": ultimo_dia.isoformat(),
                        "limit": 100,
                        "offset": offset,
                    },
                )
                r.raise_for_status()
                data = r.json()
                pagamentos.extend(data["data"])
                if not data["hasMore"]:
                    break
                offset += 100

        prontos = []
        for p in pagamentos:
            if ja_emitida(p["id"]):
                continue
            customer_id = p.get("customer", "")
            if not customer_id:
                continue
            r = client.get(f"{ASAAS_BASE_URL}/customers/{customer_id}", headers={"access_token": ASAAS_API_KEY})
            r.raise_for_status()
            cust = r.json()
            cfg = _encontrar_config_cliente(customer_id, cust.get("cpfCnpj", ""), cust.get("name", ""))
            if cfg:
                prontos.append({
                    "payment_id": p["id"],
                    "inquilino": cust.get("name", ""),
                    "proprietario": cfg["nome_tomador"],
                    "valor_comissao": cfg["valor_referencia"],
                })

    return prontos


def _imprimir_pendentes(pendentes: list[dict]) -> None:
    if not pendentes:
        print("Nenhum pagamento pendente de nota fiscal este mês.")
        return
    print(f"\n{len(pendentes)} pagamento(s) pronto(s) para emitir nota:\n")
    total = 0.0
    for p in pendentes:
        print(f"  {p['payment_id']} | {p['proprietario']:<35} | inquilino={p['inquilino']:<30} | R$ {p['valor_comissao']:.2f}")
        total += p["valor_comissao"]
    print(f"\nTotal em comissões: R$ {total:.2f}")


def _recarregar_dry_run() -> None:
    """
    Re-executa src.config, src.nfem_automation e src.pipeline nessa ordem.

    Necessário porque `pendentes`/`emitir-mes` já importam esses módulos (via
    _buscar_pendentes_mes_atual) antes de _emitir_pendentes trocar DRY_RUN no
    ambiente — e o valor de DRY_RUN é lido só uma vez, no import, tanto em
    src.config quanto no default do __init__ de NfemAutomation. Sem o reload,
    a troca do env var não tem efeito nenhum e a emissão "real" continua em
    modo simulação.
    """
    import importlib
    import sys

    for nome in ("src.config", "src.nfse_nacional_automation", "src.pipeline"):
        if nome in sys.modules:
            importlib.reload(sys.modules[nome])
        else:
            importlib.import_module(nome)


def _emitir_pendentes(pendentes: list[dict]) -> None:
    """Ativa DRY_RUN=false, emite em lote, e sempre volta DRY_RUN=true ao final."""
    import os
    from pathlib import Path

    env_path = Path(__file__).parent.parent / ".env"
    conteudo_original = env_path.read_text(encoding="utf-8")

    try:
        env_path.write_text(
            conteudo_original.replace("DRY_RUN=true", "DRY_RUN=false"), encoding="utf-8"
        )
        os.environ["DRY_RUN"] = "false"
        _recarregar_dry_run()

        from src.pipeline import processar_lote
        payment_ids = [p["payment_id"] for p in pendentes]
        resultados = asyncio.run(processar_lote(payment_ids))
        print(json.dumps(resultados, ensure_ascii=False, indent=2))

        sucesso = sum(1 for r in resultados if r["status"] == "sucesso")
        erro = sum(1 for r in resultados if r["status"] == "erro")
        print(f"\nCONCLUÍDO: {sucesso} sucesso, {erro} erro, {len(resultados)} total")
        if erro:
            print("Notas com erro ficam registradas em /erros — rode 'python -m src.cli listar-erros' para ver detalhes.")
    finally:
        env_path.write_text(conteudo_original, encoding="utf-8")
        os.environ["DRY_RUN"] = "true"
        _recarregar_dry_run()


def _parse_flags(argv: list[str]) -> dict:
    """Parser simples de flags '--chave valor' para os comandos manuais."""
    flags: dict[str, str] = {}
    i = 0
    while i < len(argv):
        token = argv[i]
        if token.startswith("--"):
            chave = token[2:]
            valor = argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else ""
            flags[chave] = valor
            i += 2
        else:
            i += 1
    return flags


def _emitir_manual(args: dict) -> None:
    """
    Emite uma nota avulsa (fora do fluxo do Asaas) a partir dos dados passados.

    Regras fixas: natureza da operação 107; item da lista de serviço 1005 para
    VENDA e 1712 para ALUGUEL; alíquota ISS e demais campos seguem as constantes
    de config. O tomador precisa já estar cadastrado no NF-em pelo CPF/CNPJ — a
    automação só informa o documento e o site preenche nome/endereço.

    Emite de verdade (dry_run=False explícito) e abre o navegador para o captcha
    do login (headless=False), independente do que estiver no .env.
    """
    from datetime import datetime

    tipo = (args.get("tipo") or "").strip().lower()
    cpf_cnpj = (args.get("cpf-cnpj") or args.get("cpf_cnpj") or "").strip()
    nome_tomador = (args.get("nome-tomador") or args.get("nome_tomador") or cpf_cnpj).strip()
    descricao = (args.get("descricao") or "").strip()
    valor_raw = (args.get("valor") or "").strip()

    if tipo not in ("venda", "aluguel"):
        print("Erro: --tipo deve ser 'venda' ou 'aluguel'.")
        sys.exit(1)
    if not cpf_cnpj:
        print("Erro: --cpf-cnpj é obrigatório.")
        sys.exit(1)
    if not descricao:
        print("Erro: --descricao é obrigatória.")
        sys.exit(1)
    try:
        valor = float(valor_raw.replace(".", "").replace(",", ".")) if "," in valor_raw else float(valor_raw)
    except ValueError:
        print(f"Erro: --valor inválido: {valor_raw!r}")
        sys.exit(1)

    codigo_servico = "1005" if tipo == "venda" else "1712"

    dados = {
        "nome_tomador": nome_tomador,
        "cpf_cnpj": cpf_cnpj,
        "descricao_servico": descricao,
        "valor_servico": valor,
        "natureza_operacao": "107",
        "codigo_servico": codigo_servico,
    }

    # Portal Nacional (exclusivo a partir de 20/07/2026)
    from src.config import (
        NFSE_NACIONAL_USER,
        NFSE_NACIONAL_PASSWORD,
        NFSE_NACIONAL_SESSION_STATE,
        certificado_digital_configurado,
    )
    from src.config import (
        NATUREZA_OPERACAO, ITEM_LISTA_SERVICO, CODIGO_SERVICO,
        ALIQUOTA_ISS, MUNICIPIO_INCIDENCIA, ISS_RETIDO
    )
    from src.nfse_nacional_automation import NfseNacionalAutomation as NfemAutomation
    from src.pdf_manager import salvar_pdf
    from src.idempotency import registrar_emissao, registrar_erro

    portal_user = NFSE_NACIONAL_USER
    portal_password = NFSE_NACIONAL_PASSWORD
    portal_session = NFSE_NACIONAL_SESSION_STATE
    usa_certificado = certificado_digital_configurado()

    payment_id = f"manual_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # --usar-sessao: modo remoto/desassistido — roda headless com a sessão salva
    # e aborta (SessaoExpirada) se a sessão não valer mais, em vez de travar
    # esperando um captcha que ninguém vai digitar. Sem a flag (uso local no
    # Mac), abre o navegador para o captcha quando a sessão não estiver quente.
    usar_sessao = "usar-sessao" in args or "usar_sessao" in args
    headless = usar_sessao or usa_certificado
    unattended = usar_sessao or usa_certificado

    async def _run():
        # Portal Nacional: precisa das credenciais
        async with NfemAutomation(
            user=portal_user,
            password=portal_password,
            natureza_operacao=NATUREZA_OPERACAO,
            codigo_servico=dados.get("codigo_servico", CODIGO_SERVICO),
            item_lista_servico=ITEM_LISTA_SERVICO,
            aliquota_iss=ALIQUOTA_ISS,
            municipio_incidencia=MUNICIPIO_INCIDENCIA,
            iss_retido=ISS_RETIDO,
            headless=headless,
            dry_run=False,
            storage_state=str(portal_session),
            unattended=unattended,
        ) as nfem:
            return await nfem.emitir(dados)

    try:
        pdf_bytes, numero = asyncio.run(_run())
    except Exception as e:
        registrar_erro(payment_id, dados.get("nome_tomador", cpf_cnpj), valor, str(e))
        print(json.dumps(
            {"status": "erro", "erro_tipo": type(e).__name__, "erro": str(e)},
            ensure_ascii=False, indent=2,
        ))
        sys.exit(1)

    nome_final = dados.get("nome_tomador") or cpf_cnpj
    agora = datetime.now()
    caminho = salvar_pdf(pdf_bytes, nome_final, payment_id, agora)
    registrar_emissao(payment_id, nome_final, valor, agora.date().isoformat(), numero, str(caminho))

    print(json.dumps({
        "status": "sucesso",
        "tipo": tipo,
        "numero_nota": numero,
        "tomador": nome_final,
        "cpf_cnpj": cpf_cnpj,
        "valor": valor,
        "descricao": descricao,
        "codigo_servico": codigo_servico,
        "pdf_path": str(caminho),
    }, ensure_ascii=False, indent=2))


def _login_manual() -> None:
    """
    Abre o navegador, faz o login manual (com captcha) e salva a sessão "quente"
    em NFSE_NACIONAL_SESSION_STATE. Depois disso, `emitir-manual --usar-sessao` e o listener
    do WhatsApp emitem sem precisar de captcha enquanto a sessão do portal valer.

    Portal Nacional exclusivo a partir de 20/07/2026.
    """
    from src.config import NFSE_NACIONAL_USER, NFSE_NACIONAL_PASSWORD, NFSE_NACIONAL_SESSION_STATE
    from src.config import (
        NATUREZA_OPERACAO, ITEM_LISTA_SERVICO, CODIGO_SERVICO,
        ALIQUOTA_ISS, MUNICIPIO_INCIDENCIA, ISS_RETIDO
    )
    from src.nfse_nacional_automation import NfseNacionalAutomation as NfemAutomation

    async def _run():
        async with NfemAutomation(
            user=NFSE_NACIONAL_USER,
            password=NFSE_NACIONAL_PASSWORD,
            natureza_operacao=NATUREZA_OPERACAO,
            codigo_servico=CODIGO_SERVICO,
            item_lista_servico=ITEM_LISTA_SERVICO,
            aliquota_iss=ALIQUOTA_ISS,
            municipio_incidencia=MUNICIPIO_INCIDENCIA,
            iss_retido=ISS_RETIDO,
            headless=False,
            dry_run=True,
            storage_state=str(NFSE_NACIONAL_SESSION_STATE),
            unattended=False,
        ) as nfem:
            await nfem.login()
            # Garante o arquivo salvo mesmo se a sessão já estava quente (login
            # retornou cedo sem passar pelo _salvar_sessao do fluxo de captcha).
            await nfem._salvar_sessao()

    print("Abrindo o navegador para login... digite o captcha e clique em Login.")
    asyncio.run(_run())
    print(f"\nSessão salva em: {NFSE_NACIONAL_SESSION_STATE}")
    print("Agora o disparo remoto (WhatsApp) emite sem captcha enquanto a sessão valer.")


def _simular():
    """Testa o pipeline com dados fictícios (sem chamar Asaas nem NF-em)."""
    import os
    os.environ.setdefault("DRY_RUN", "true")

    from src.config import DRY_RUN
    from src.asaas_client import montar_dados_nota
    from src.logger import log

    log.info("=== SIMULAÇÃO (dry_run=%s) ===", DRY_RUN)

    pagamento_fake = {
        "id": "pay_SIMULACAO_001",
        "customer": "cus_000000000002",
        "status": "CONFIRMED",
        "value": 3610.46,
        "billingType": "BOLETO",
        "description": "Aluguel sala comercial",
        "paymentDate": "2026-06-25",
        "confirmedDate": "2026-06-25",
    }

    cliente_fake = {
        "id": "cus_000000000002",
        "name": "ERIC RUBSON DA SILVA ROCHA",
        "cpfCnpj": "00952750104",
        "address": "Rua Elizabeth Rech",
        "addressNumber": "417",
        "province": "Paranaguamirim",
        "city": "Joinville",
        "state": "SC",
        "postalCode": "89220490",
    }

    from src.config import carregar_clientes
    clientes = carregar_clientes()
    cliente_config = next(
        (c for c in clientes if c.get("asaas_customer_id") == pagamento_fake["customer"]),
        None,
    )

    dados = montar_dados_nota(pagamento_fake, cliente_fake, cliente_config)
    log.info("Dados montados: %s", json.dumps(dados, ensure_ascii=False, indent=2))

    # Testa cenário duplicado
    from src.idempotency import ja_emitida, registrar_emissao, registrar_erro
    pid = pagamento_fake["id"]

    print("\n--- Teste: pagamento novo ---")
    print("Já emitida?", ja_emitida(pid))

    print("\n--- Teste: registrar emissão ---")
    registrar_emissao(pid, dados["nome_tomador"], dados["valor_servico"], "2026-06-25", "DRY-001", "/tmp/teste.pdf")
    print("Após registrar, já emitida?", ja_emitida(pid))

    print("\n--- Teste: tentativa duplicada ---")
    print("Já emitida (deve ser True)?", ja_emitida(pid))

    print("\n--- Teste: PDF manager ---")
    from src.pdf_manager import salvar_pdf
    from datetime import datetime
    caminho = salvar_pdf(b"%PDF-1.4 FAKE", dados["nome_tomador"], pid, datetime(2026, 6, 25))
    print("PDF salvo em:", caminho)

    print("\nSimulação concluída com sucesso!")


if __name__ == "__main__":
    main()
