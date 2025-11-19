import flet as ft
from app.theme import PRIMARY_COLOR, PRIMARY_COLOR, SECONDARY_BACKGROUND_COLOR, SECONDARY_COLOR

def PrimaryButton(
    text: str,
    on_click: callable,
    page: ft.Page = None,
    width: float = None,
    height: float = None,
    **kwargs
) -> ft.Container:
    button_height = height or (max(page.height * 0.07, 55) if page else 55)
    button_width = width or (page.width * 0.9 if page else 250)

    return ft.Container(
        content=ft.Text(
            text,
            color=SECONDARY_BACKGROUND_COLOR,
            size=16,
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        width=button_width,
        height=button_height,
        bgcolor=PRIMARY_COLOR,
        border_radius=ft.border_radius.all(12),
        on_click=on_click,
        **kwargs
    )

def GradientButton(
    text: str,
    on_click: callable,
    width: float | int = None,
    height: float | int = 55,
    border_radius: int = 12,
    text_size: int = 16,
    **kwargs
) -> ft.Container:
    container = ft.Container(
        content=ft.Text(
            text,
            color=SECONDARY_BACKGROUND_COLOR,
            size=text_size,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        width=width,
        height=height,
        border_radius=border_radius,
        on_click=on_click,
        ink=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[PRIMARY_COLOR, SECONDARY_COLOR],
        ),
        scale=1,
        animate=ft.Animation(200, "easeInOut"),
        **kwargs,
    )

    def hover(e):
        container.scale = 1.04 if e.data == "true" else 1.0
        container.update()

    container.on_hover = hover

    return container