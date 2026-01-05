from app.core.navigation.routes import Routes

from app.modules.auth.ui.login_page import build_login_page
from app.modules.auth.ui.forgot_password_page import build_forgot_password_page
from app.modules.auth.ui.register_page import build_register_page
from app.modules.auth.ui.reset_password_token_page import build_reset_password_token_page
from app.modules.auth.ui.reset_password_new_page import build_reset_password_new_page
from app.modules.home.ui.home_page import build_home_page
# from app.modules.auth.ui.register_complementary_page import build_register_complementary_page


def get_app_routes() -> dict[str, callable]:
    return {

        # ─────────────────────────────
        # AUTH
        # ─────────────────────────────

        Routes.REGISTER: build_register_page,
        # Routes.REGISTER_COMPLEMENTARY: build_register_complementary_page,
        Routes.LOGIN: build_login_page,
        Routes.FORGOT_PASSWORD: build_forgot_password_page,
        Routes.RESET_PASSWORD_TOKEN: build_reset_password_token_page,
        Routes.RESET_PASSWORD_NEW: build_reset_password_new_page,

        # ─────────────────────────────
        # HOME
        # ─────────────────────────────

        Routes.HOME: build_home_page,
    }
