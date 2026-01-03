import flet as ft
from .base_overlay import show_overlay
from app.core.theme.colors import success


def show_success(page: ft.Page, message: str):
    page.dialog_queue.enqueue(
        lambda: show_overlay(
        page=page,
        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        icon_color=success,
        message=message,
    )
)