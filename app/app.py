import flet as ft

from app.core.navigation.router import Router
from app.core.navigation.routes import Routes
from app.core.navigation.routes_factory import get_app_routes
from app.core.state.app_state import AppState
from app.core.theme.theme_resolver import ThemeResolver
from app.core.layouts.app_shell import AppShell
from app.modules.auth.controller.auth_controller import AuthController
from app.shared.components.dialogs.dialog_dispatcher import Dialogs
from app.shared.components.dialogs.dialog_queue import DialogQueue


def create_app(page: ft.Page) -> None:
    # ─────────────────────────────
    # Page base
    # ─────────────────────────────
    page.title = "ViMi42"
    page.locale = "pt_BR"
    page.scroll = None 
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.padding = 0

    page.on_login = None

    # ─────────────────────────────
    # Estado global
    # ─────────────────────────────
    app_state = AppState()

    # ─────────────────────────────
    # Tema
    # ─────────────────────────────
    def on_theme_change():
        ThemeResolver.apply(app_state, page)
        page.bgcolor = page.theme.color_scheme.background
        page.update()

    app_state.subscribe(on_theme_change)
    ThemeResolver.apply(app_state, page)

    # ─────────────────────────────
    # Dialog Queue (GLOBAL)
    # ─────────────────────────────
    page.dialog_queue = DialogQueue(page)

    # ─────────────────────────────
    # Shell
    # ─────────────────────────────
    shell = AppShell(page)
    page.add(shell)

    # ─────────────────────────────
    # Rotas / Views
    # ─────────────────────────────
    routes = get_app_routes()
    Router(page, routes, shell)

    # ─────────────────────────────
    # Rota inicial
    # ─────────────────────────────
    page.go(page.route or Routes.DEFAULT)