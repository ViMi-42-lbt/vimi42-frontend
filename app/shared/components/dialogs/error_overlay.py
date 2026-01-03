import flet as ft
from .base_overlay import show_overlay
from app.core.theme.colors import error

def show_error(page: ft.Page, message: str):
    page.dialog_queue.enqueue(
        lambda: show_overlay(
            page=page,
            icon=ft.Icons.ERROR_OUTLINE,
            icon_color=error,
            message=message,
        )
    )