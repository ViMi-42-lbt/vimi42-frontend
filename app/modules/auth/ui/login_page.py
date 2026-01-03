import flet as ft

from app.core.navigation.routes import Routes
from app.core.theme.theme_resolver import ThemeResolver
from app.core.theme.typography import title_lg, body_secondary, body_primary
from app.modules.auth.controller.auth_controller import AuthController
from app.shared.components.inputs.text_field import AppTextField
from app.shared.components.buttons.primary_button import PrimaryButton
from app.shared.components.buttons.link_button import LinkButton
from app.shared.components.buttons.google_auth_button import GoogleAuthButton


def build_login_page(page: ft.Page) -> ft.Control:
    controller = AuthController(page)
    scheme = ThemeResolver.get_scheme(page)

    email_input = AppTextField(page=page, label="E-mail")
    password_input = AppTextField(page=page, label="Senha", password=True)

    email_input.value = ""
    password_input.value = ""

    def on_submit(e):
        controller.login(
            email=email_input.value,
            password=password_input.value,
            email_field=email_input,
            password_field=password_input,
            submit_button=submit_button,
        )

    google_btn = GoogleAuthButton(
        on_click=lambda _: controller.login_with_google(button=google_btn)
    )

    submit_button = PrimaryButton(text="Entrar", on_click=on_submit)

    return ft.Container(
        padding=ft.padding.only(left=16, right=16, top=62, bottom=62),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            width=360,
            controls=[
                ft.Icon(ft.Icons.ECO_SHARP, size=42, color=scheme.primary),
                ft.Text("Entre agora e negocie com segurança!", style=title_lg, color=scheme.primary, text_align=ft.TextAlign.CENTER),

                google_btn,
                ft.Text("______________ ou ______________", style=body_secondary, color=scheme.outline, text_align=ft.TextAlign.CENTER),
                ft.Text("Conecte-se com:", style=body_primary, color=scheme.outline, text_align=ft.TextAlign.CENTER),

                email_input,
                password_input,
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        LinkButton(
                            text="Esqueci minha senha",
                            on_click=lambda _: page.go(Routes.FORGOT_PASSWORD),
                        )
                    ],
                ),
                submit_button,
                ft.Row(
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Não tem uma conta?", style=body_secondary, color=scheme.outline),
                        LinkButton(
                            text="Crie uma aqui",
                            on_click=lambda _: page.go(Routes.REGISTER),
                        ),
                    ],
                ),
            ],
        ),
    )