#!/usr/bin/env python3
"""
Gerenciador de Sessão Autenticada do Facebook para Playwright.

Kernel IMPAR: Contexto persistente com autenticação reutilizável.

Fluxo:
  1. AUTH_SETUP → Abrir navegador, permitir login manual, persistir
  2. AUTH_CHECK → Validar sessão existente
  3. AUTH_REUSE → Usar contexto autenticado no Publisher

Não captura credenciais. Não exibe cookies. Não versiona sessão.
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright


class FacebookSessionManager:
    """Gerencia sessão autenticada do Facebook no Playwright."""

    def __init__(self, profile_dir: Path):
        """
        Inicializar gerenciador.

        Args:
            profile_dir: Diretório de perfil persistente do Playwright
        """
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(parents=True, exist_ok=True)

        self.status_file = self.profile_dir / "session-status.json"
        self.marketplace_url = "https://www.facebook.com/marketplace/create/rental"

    def _load_status(self) -> dict:
        """Carregar status da última sessão."""
        if self.status_file.exists():
            return json.loads(self.status_file.read_text(encoding="utf-8"))
        return {"status": "NOT_INITIALIZED"}

    def _save_status(self, status: str, details: dict = None):
        """Salvar status da sessão."""
        data = {
            "status": status,
            "timestamp": "2026-07-24T11:00:00Z",
            "details": details or {}
        }
        self.status_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def auth_setup(self, headless: bool = False):
        """
        Modo AUTH_SETUP: Capturar autenticação manualmente.

        Procedimento:
          1. Abrir navegador em modo headed
          2. Permitir que usuário faça login no Facebook
          3. Aguardar confirmação
          4. Persistir sessão
          5. Retornar: FACEBOOK_SESSION_SAVED

        Args:
            headless: Se False, abre navegador visível (padrão para AUTH_SETUP)
        """

        print("\n" + "="*70)
        print("🔐 FACEBOOK AUTH_SETUP — CAPTURA DE SESSÃO AUTENTICADA")
        print("="*70 + "\n")

        print("📋 Procedimento:")
        print("  1. O navegador será aberto")
        print("  2. Faça login na sua conta do Facebook")
        print("  3. Após fazer login, volte aqui e pressione ENTER")
        print("  4. A sessão será persistida para uso futuro\n")

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=False,  # AUTH_SETUP sempre em modo headed
                viewport={"width": 1280, "height": 900},
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            try:
                print("🌐 Abrindo Facebook...")
                page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
                print("   ✅ Facebook aberto\n")

                print("⏳ Aguardando login manual...")
                print("   Quando terminar de fazer login, pressione ENTER aqui:\n")
                input("➜ ")

                # Verificar autenticação
                print("\n🔍 Verificando autenticação...")
                is_authenticated = self._verify_authentication(page)

                if is_authenticated:
                    print("   ✅ Autenticação confirmada\n")
                    print("💾 Persistindo sessão...")
                    self._save_status("AUTHENTICATED", {
                        "profile_dir": str(self.profile_dir),
                        "authenticated_at": "2026-07-24T11:00:00Z"
                    })
                    print("   ✅ Sessão persistida\n")

                    print("="*70)
                    print("✅ FACEBOOK_SESSION_SAVED")
                    print("="*70 + "\n")
                    print("Próxima execução:")
                    print("  python3 publish_marketplace_playwright.py --auth-check\n")
                    return True
                else:
                    print("   ❌ Autenticação não confirmada")
                    print("   Verifique se fez login corretamente.\n")
                    return False

            except Exception as e:
                print(f"   ❌ Erro: {e}\n")
                return False
            finally:
                print("📖 Navegador permanecerá aberto para revisão.")
                print("   Feche manualmente quando terminar.\n")

    def auth_check(self):
        """
        Modo AUTH_CHECK: Validar sessão existente.

        Retorna:
          • FACEBOOK_SESSION_VALID: Sessão autenticada e pronta
          • FACEBOOK_SESSION_EXPIRED: Perfil existe mas não autenticado
          • AUTH_SETUP_REQUIRED: Nenhuma sessão anterior
        """

        print("\n" + "="*70)
        print("🔍 FACEBOOK AUTH_CHECK — VALIDAÇÃO DE SESSÃO")
        print("="*70 + "\n")

        # Verificar se perfil existe
        if not list(self.profile_dir.glob("*")):
            print("❌ Nenhuma sessão anterior encontrada")
            print("   Execução requerida: --auth-setup\n")
            self._save_status("NOT_INITIALIZED", {"reason": "no_profile_found"})
            return "AUTH_SETUP_REQUIRED"

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=True,  # AUTH_CHECK em modo headless
                viewport={"width": 1280, "height": 900},
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            try:
                print("🌐 Abrindo Marketplace...")
                page.goto(self.marketplace_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)

                is_authenticated = self._verify_authentication(page)

                if is_authenticated:
                    print("   ✅ Autenticação confirmada")
                    print("   ✅ Marketplace acessível\n")
                    self._save_status("AUTHENTICATED", {
                        "validated_at": "2026-07-24T11:00:00Z",
                        "marketplace_accessible": True
                    })

                    print("="*70)
                    print("✅ FACEBOOK_SESSION_VALID")
                    print("="*70 + "\n")
                    return "FACEBOOK_SESSION_VALID"

                else:
                    print("   ❌ Autenticação inválida ou expirada")
                    print("   Marketplace não acessível\n")
                    self._save_status("EXPIRED", {
                        "validated_at": "2026-07-24T11:00:00Z",
                        "reason": "authentication_failed"
                    })

                    print("="*70)
                    print("❌ FACEBOOK_SESSION_EXPIRED")
                    print("="*70 + "\n")
                    print("Próxima execução: --auth-setup\n")
                    return "FACEBOOK_SESSION_EXPIRED"

            except Exception as e:
                print(f"   ❌ Erro: {e}\n")
                self._save_status("ERROR", {"error": str(e)})
                return "FACEBOOK_SESSION_EXPIRED"

            finally:
                browser.close()

    def get_authenticated_context(self):
        """
        Obter contexto autenticado para uso no Publisher.

        Retorna:
          • browser: Contexto Playwright autenticado
          • page: Página para usar
          • status: Status da autenticação

        Levanta:
          • RuntimeError: Se sessão não estiver autenticada
        """

        status = self._load_status()
        if status.get("status") != "AUTHENTICATED":
            raise RuntimeError(
                f"Sessão não autenticada: {status.get('status')}. "
                "Execute: --auth-setup"
            )

        browser = None
        try:
            p = sync_playwright().__enter__()
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=False,
                viewport={"width": 1280, "height": 900},
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Verificar autenticação
            page.goto(self.marketplace_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)

            if not self._verify_authentication(page):
                raise RuntimeError("Sessão autenticada não acessível ao Marketplace")

            return browser, page, "AUTHENTICATED"

        except Exception as e:
            if browser:
                browser.close()
            raise RuntimeError(f"Erro ao obter contexto autenticado: {e}")

    def _verify_authentication(self, page) -> bool:
        """
        Verificar autenticação por múltiplos sinais.

        Validações:
          • Ausência de tela de login
          • Presença de elemento de conta
          • Acesso ao Marketplace
          • Sem redirecionamento para login
        """

        try:
            # Verificar 1: Não está na tela de login
            login_screen = page.query_selector('button:has-text("Entrar")')
            if login_screen:
                return False

            # Verificar 2: Página carregou (qualquer conteúdo além de login)
            current_url = page.url
            if "login.php" in current_url or "/auth/" in current_url:
                return False

            # Verificar 3: Elemento de conta visível (nome de usuário ou dropdown conta)
            profile_menu = page.query_selector('[aria-label*="seu perfil"], [aria-label*="Seu Perfil"]')
            if profile_menu:
                return True

            # Verificar 4: Se não tem menu, mas também não tem login, é provável autenticado
            # (Marketplace pode ter layout diferente)
            if current_url.startswith("https://www.facebook.com/marketplace"):
                return True

            # Fallback: Se não encontrou indicadores, assume não autenticado
            return False

        except Exception:
            return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Facebook Session Manager")
    parser.add_argument("command", choices=["auth-setup", "auth-check"])
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path(".impar/runtime/facebook-profile"),
        help="Diretório do perfil"
    )

    args = parser.parse_args()

    manager = FacebookSessionManager(args.profile)

    if args.command == "auth-setup":
        success = manager.auth_setup()
        exit(0 if success else 1)

    elif args.command == "auth-check":
        result = manager.auth_check()
        exit(0 if result == "FACEBOOK_SESSION_VALID" else 1)
