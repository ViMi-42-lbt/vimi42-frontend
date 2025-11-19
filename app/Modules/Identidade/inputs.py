import flet as ft
from app.theme import PRIMARY_COLOR, TERTIARY_COLOR, PRIMARY_COLOR, GREY_COLOR, PRIMARY_BACKGROUND_COLOR

def AppTextField(label: str, password: bool = False, **kwargs) -> ft.TextField:
    field = ft.TextField(
        label=label,
        password=password,
        border_color=GREY_COLOR,
        border_radius=ft.border_radius.all(12),
        border_width=1,
        content_padding=ft.padding.symmetric(vertical=14, horizontal=16),
        label_style=ft.TextStyle(color=GREY_COLOR, size=13),
        cursor_color=PRIMARY_COLOR,
        focused_border_color=PRIMARY_COLOR,
        text_style=ft.TextStyle(size=14),
        **kwargs
    )

    if password:
        def toggle_password(e):
            field.password = not field.password
            # muda a cor do ícone de acordo com o estado
            field.suffix_icon.icon_color = GREY_COLOR if field.password else PRIMARY_COLOR
            field.update()

        field.suffix_icon = ft.IconButton(
            icon=ft.Icons.REMOVE_RED_EYE,
            icon_color=GREY_COLOR,
            on_click=toggle_password,
            bgcolor=None,
            hover_color=PRIMARY_BACKGROUND_COLOR,
            style=ft.ButtonStyle(
                padding=ft.padding.only(left=4, right=4)  # afasta o ícone da borda
            )
        )

    return field

def UserTypeToggle(on_change: callable) -> ft.Container:
    """
    Seletor de tipo de usuário: Cliente / Prestador
    """
    def build_controls(selected_index: int):
        return [
            ft.Text(
                "Sou Cliente",
                color=PRIMARY_BACKGROUND_COLOR if selected_index == 0 else TERTIARY_COLOR,
                weight=ft.FontWeight.NORMAL,
            ),
            ft.Text(
                "Sou Prestador",
                color=PRIMARY_BACKGROUND_COLOR if selected_index == 1 else TERTIARY_COLOR,
                weight=ft.FontWeight.NORMAL,
            ),
        ]

    # Armazena o estado do índice selecionado
    selected_index = 0

    # Container principal
    container = ft.Container(
        padding=ft.padding.all(2),
        bgcolor=None,
        border=ft.border.all(1, GREY_COLOR),
        border_radius=ft.border_radius.all(12),
    )

    # Cria o toggle
    toggle = ft.CupertinoSlidingSegmentedButton(
        selected_index=selected_index,
        thumb_color=TERTIARY_COLOR,
        bgcolor=PRIMARY_BACKGROUND_COLOR,
        padding=ft.padding.all(0),
        controls=build_controls(selected_index),
        on_change=lambda e: _on_change(e),
    )

    # Atualiza cores quando muda a seleção
    def _on_change(e):
        nonlocal selected_index
        selected_index = e.control.selected_index
        toggle.controls = build_controls(selected_index)
        toggle.update()
        on_change(e)  # chama callback externo

    container.content = toggle
    return container

