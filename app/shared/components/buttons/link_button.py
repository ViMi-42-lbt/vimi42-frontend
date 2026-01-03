import flet as ft

class LinkButton(ft.TextButton):
    def __init__(
        self,
        text: str,
        on_click: callable,
    ):
        super().__init__(
            text,
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.TRANSPARENT,
                shadow_color=ft.Colors.TRANSPARENT,
                surface_tint_color=ft.Colors.TRANSPARENT,
                color=ft.Colors.SECONDARY,
            ),
        )
