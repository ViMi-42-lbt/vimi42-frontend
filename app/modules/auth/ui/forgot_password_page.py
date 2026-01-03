import flet as ft

from app.core.navigation.routes import Routes
from app.core.theme.theme_resolver import ThemeResolver
from app.modules.auth.controller.auth_controller import AuthController
from app.shared.components.buttons.link_button import LinkButton
from app.shared.components.buttons.primary_button import PrimaryButton
from app.shared.components.inputs.text_field import AppTextField
from app.core.theme.typography import title_lg, body_primary


def build_forgot_password_page(page: ft.Page) -> ft.Control:
    controller = AuthController(page)
    scheme = ThemeResolver.get_scheme(page)

    email_input = AppTextField(page=page, label="E-mail")

    def on_submit(e):
        controller.forgot_password(
            email=email_input.value,
            email_field=email_input,
            submit_button=submit_button,
        )

    submit_button = PrimaryButton(
        text="Receber instruções",
        on_click=on_submit,
    )

    return ft.Container(
        padding=ft.padding.only(left=16, right=16, top=62, bottom=62),
        content=ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=360,
            controls=[
                ft.Icon(ft.Icons.LOCK_RESET, size=42, color=scheme.primary),
                ft.Text("Recuperar conta", style=title_lg, color=scheme.primary),
                ft.Text(
                    "Digite seu email cadastrado para recuperar sua conta:",
                    style=body_primary,
                    color=scheme.outline,
                    text_align=ft.TextAlign.CENTER,
                ),
                email_input,
                submit_button,
                LinkButton(
                    text="Voltar ao login",
                    on_click=lambda _: page.go(Routes.LOGIN),
                ),
            ],
        ),
    )