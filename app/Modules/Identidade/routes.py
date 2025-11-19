import flet as ft
from app.theme import PRIMARY_BACKGROUND_COLOR
from .login_view import build_login_view
from .register_view import build_register_view
from .forgot_password_view import build_forgot_password_view

def get_identidade_routes(page: ft.Page) -> list[ft.View]:
    """Retorna todas as views (telas) deste módulo."""
    
    return [
        ft.View(
            route="/login",
            controls=[build_login_view(page)],
            bgcolor=PRIMARY_BACKGROUND_COLOR,
            padding=0,
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        ft.View(
            route="/register",
            controls=[build_register_view(page)],
            bgcolor=PRIMARY_BACKGROUND_COLOR,
            padding=0,
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        ft.View(
            route="/forgot-password",
            controls=[build_forgot_password_view(page)],
            bgcolor=PRIMARY_BACKGROUND_COLOR,
            padding=0,
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    ]