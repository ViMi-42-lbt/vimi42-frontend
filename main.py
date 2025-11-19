import flet as ft
from app.theme import PRIMARY_BACKGROUND_COLOR
from app.router import Router

def main(page: ft.Page):
    page.title = "ViMi42"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = PRIMARY_BACKGROUND_COLOR
    page.locale = "pt_BR"

    # Inicializa o roteador
    app_router = Router(page)
    page.on_route_change = app_router.route_change
    page.on_view_pop = app_router.view_pop

    # Vai para a rota inicial (login)
    page.go("/login")

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")