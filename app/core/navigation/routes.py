class Routes:

    # ─────────────────────────────
    # AUTH
    # ─────────────────────────────

    LOGIN = "/login"
    REGISTER = "/register"
    REGISTER_COMPLEMENTARY = "/register/complementary" # Débito Técnico (Autenticação google)
    FORGOT_PASSWORD = "/forgot-password"
    RESET_PASSWORD_TOKEN = "/reset-password/token"
    RESET_PASSWORD_NEW = "/reset-password/new"

    # ─────────────────────────────
    # DEFAULT
    # ─────────────────────────────

    DEFAULT = LOGIN

    # ─────────────────────────────
    # HOME
    # ─────────────────────────────

    HOME = "/home"

    # ─────────────────────────────
    # BOTTOM NAVIBAR
    # ─────────────────────────────

    MAIN_NAV_ROUTES = [HOME]