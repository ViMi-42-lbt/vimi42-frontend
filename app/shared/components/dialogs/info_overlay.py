import flet as ft
from .base_overlay import show_overlay
from app.core.theme.colors import info

def show_info(page: ft.Page, message: str):
    page.dialog_queue.enqueue(
        lambda: show_overlay(
        page=page,
        icon=ft.Icons.INFO_OUTLINE,
        icon_color=info,
        message=message,
    )    
)