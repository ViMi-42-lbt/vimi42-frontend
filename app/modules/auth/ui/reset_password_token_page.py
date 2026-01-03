import flet as ft

from app.core.navigation.routes import Routes
from app.core.theme.theme_resolver import ThemeResolver
from app.core.theme.typography import title_lg, body_primary
from app.modules.auth.controller.auth_controller import AuthController
from app.shared.components.inputs.text_field import AppTextField
from app.shared.components.buttons.primary_button import PrimaryButton
from app.shared.components.buttons.link_button import LinkButton


def build_reset_password_token_page(page: ft.Page) -> ft.Control:
    controller = AuthController(page)
    scheme = ThemeResolver.get_scheme(page)

    token_input = AppTextField(
        page=page,
        label="Token recebido",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def on_submit(e):
        controller.validate_reset_token(
            token=token_input.value,
            token_field=token_input,
            submit_button=submit_button,
        )

    submit_button = PrimaryButton(
        text="Enviar",
        on_click=on_submit,
    )

    return ft.Container(
        padding=ft.padding.only(left=16, right=16, top=62, bottom=62),
        content=ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=360,
            controls=[
                ft.Icon(
                    ft.Icons.KEY_SHARP,
                    size=42,
                    color=scheme.primary,
                ),
                ft.Text(
                    "Validar token",
                    style=title_lg,
                    color=scheme.primary,
                ),
                ft.Text(
                    "Informe o token que enviamos para seu email.",
                    style=body_primary,
                    color=scheme.outline,
                    text_align=ft.TextAlign.CENTER,
                ),
                token_input,
                submit_button,
                LinkButton(
                    text="Voltar ao login",
                    on_click=lambda _: page.go(Routes.LOGIN),
                ),
            ],
        ),
    )