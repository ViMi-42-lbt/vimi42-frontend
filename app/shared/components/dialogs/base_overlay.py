import flet as ft

from app.core.theme.theme_resolver import ThemeResolver
from app.shared.components.buttons.primary_button import PrimaryButton


def show_overlay(page: ft.Page, *, icon, icon_color, message: str):
    if page is None or not page.views:
        return
    
    def close_overlay(_=None):
        page.overlay.clear()
        page.update()

        if hasattr(page, "dialog_queue"):
            page.dialog_queue.notify_closed()

        if hasattr(page, "_active_overlay"):
            delattr(page, "_active_overlay")

    def render_overlay():
        scheme = ThemeResolver.get_scheme(page)

        scrim = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            on_click=close_overlay,
        )

        sheet = ft.Container(
            bgcolor=scheme.surface,
            border_radius=ft.border_radius.vertical(top=20),
            padding=ft.padding.symmetric(horizontal=24, vertical=48),
            bottom=0,
            left=0,
            right=0,
            content=ft.Column(
                spacing=24,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Icon(icon, color=icon_color, size=48),
                    ft.Text(message, color=scheme.on_surface, text_align=ft.TextAlign.CENTER),
                    PrimaryButton(text="OK", on_click=close_overlay),
                ],
            ),
        )

        page.overlay.clear()
        page.overlay.extend([scrim, sheet])

    page._active_overlay = {
        "icon": icon,
        "icon_color": icon_color,
        "message": message,
    }

    render_overlay()
    page.update()
