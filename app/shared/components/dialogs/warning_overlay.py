import flet as ft
from .base_overlay import show_overlay
from app.core.theme.colors import warning

def show_warning(page: ft.Page, message: str):
    page.dialog_queue.enqueue(
        lambda: show_overlay(
        page=page,
        icon=ft.Icons.WARNING_AMBER_OUTLINED,
        icon_color=warning,
        message=message,
    )
)