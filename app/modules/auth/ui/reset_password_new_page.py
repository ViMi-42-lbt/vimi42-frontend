import flet as ft

from app.core.navigation.routes import Routes
from app.core.theme.theme_resolver import ThemeResolver
from app.core.theme.typography import title_lg, body_primary
from app.modules.auth.controller.auth_controller import AuthController
from app.shared.components.inputs.text_field import AppTextField
from app.shared.components.buttons.primary_button import PrimaryButton
from app.shared.components.buttons.link_button import LinkButton
from app.shared.components.inputs.password_rules_card import PasswordRulesCard


def build_reset_password_new_page(page: ft.Page) -> ft.Control:
    controller = AuthController(page)
    scheme = ThemeResolver.get_scheme(page)

    password_rules_card = PasswordRulesCard(page=page, password="")

    password_input = AppTextField(
        page=page,
        label="Nova senha",
        password=True,
        can_reveal_password=True,
    )

    confirm_password_input = AppTextField(
        page=page,
        label="Confirmar nova senha",
        password=True,
        can_reveal_password=True,
    )

    def on_password_change(e):
        password_rules_card.update_password(password_input.value)

    password_input.on_change = on_password_change

    def on_submit(e):
        controller.set_new_password(
            password=password_input.value,
            confirm_password=confirm_password_input.value,
            password_field=password_input,
            confirm_password_field=confirm_password_input,
            submit_button=submit_button,
        )

    submit_button = PrimaryButton(
        text="Redefinir senha",
        on_click=on_submit,
    )

    return ft.Container(
        padding=ft.padding.only(left=16, right=16, top=62, bottom=80),
        content=ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=360,
            controls=[
                ft.Icon(
                    ft.Icons.LOCK_RESET,
                    size=42,
                    color=scheme.primary,
                ),
                ft.Text(
                    "Nova senha",
                    style=title_lg,
                    color=scheme.primary,
                ),
                ft.Text(
                    "Crie uma nova senha para sua conta.",
                    style=body_primary,
                    color=scheme.outline,
                    text_align=ft.TextAlign.CENTER,
                ),
                password_input,
                confirm_password_input,
                password_rules_card,
                submit_button,
                LinkButton(
                    text="Cancelar",
                    on_click=lambda _: page.go(Routes.LOGIN),
                ),
            ],
        ),
    )