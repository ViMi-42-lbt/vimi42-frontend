import flet as ft
from app.theme import PRIMARY_BACKGROUND_COLOR

def BaseLayout(page: ft.Page, content: ft.Control) -> ft.SafeArea:
    page.scrollbar_theme = ft.ScrollbarTheme(
        thickness=4,
        main_axis_margin=0,
        cross_axis_margin=0,
        radius=4,
    )

    return ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            bgcolor=PRIMARY_BACKGROUND_COLOR,  # Usa a constante diretamente
            alignment=ft.alignment.center,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Container(
                        expand=True,
                        padding=ft.padding.all(16),
                        content=content,
                    )
                ],
            ),
        )
    )