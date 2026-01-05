import flet as ft

from app.core.theme.theme_resolver import ThemeResolver
from app.core.theme.typography import title_md
from app.modules.auth.controller.auth_controller import AuthController


def build_home_page(page: ft.Page) -> ft.Control:
    controller = AuthController(page)
    scheme = ThemeResolver.get_scheme(page)
    
    return ft.Container(
        padding=ft.padding.only(left=16, right=16, top=62, bottom=62),
        content=ft.Column(
            spacing=20,
            width=360,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("ViMi42", style=title_md, color=scheme.primary, text_align=ft.TextAlign.CENTER),
                    ],
                )
            ],
        ),
    )