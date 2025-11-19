import flet as ft
from app.theme import title_style, regular_text_style, TERTIARY_COLOR, GREY_COLOR
from app.Modules.GlobalComponents.base_layout import BaseLayout
from app.Modules.GlobalComponents.components import GradientButton
from app.Modules.Identidade.inputs import AppTextField, UserTypeToggle
from app.Modules.Identidade.services import handle_login, EMAIL_RE, _open_snack


def build_login_view(page: ft.Page):
    # --------------------------
    # Inputs
    # --------------------------
    email_field = AppTextField(label="Email")
    password_field = AppTextField(label="Senha", password=True)

    # Estado local (0 = cliente, 1 = prestador)
    selected_user_type = {"value": 0}

    def on_user_type_change(e):
        try:
            v = int(e) if isinstance(e, (int, str)) else int(e.data)
        except:
            v = 0
        selected_user_type["value"] = 0 if v == 0 else 1

    # --------------------------
    # Botão (com referência)
    # --------------------------
    button_height = max(page.height * 0.07, 55)

    def on_login_click(e):
        email = (email_field.value or "").strip()
        password = (password_field.value or "")

        # LIMPA ERROS VISUAIS
        email_field.error_text = None
        password_field.error_text = None
        email_field.update()
        password_field.update()

        # ====== VALIDAÇÕES FRONTEND ======

        if not email:
            email_field.error_text = "Por favor informe o email."
            email_field.update()
            _open_snack(page, "Por favor informe o email.", "#d84315")
            return

        if not EMAIL_RE.match(email):
            email_field.error_text = "Email inválido. Tente novamente."
            email_field.update()
            _open_snack(page, "Email inválido. Tente novamente.", "#d84315")
            return

        if not password:
            password_field.error_text = "Informe sua senha."
            password_field.update()
            _open_snack(page, "Informe sua senha.", "#d84315")
            return

        if len(password) < 8:
            password_field.error_text = "A senha deve ter pelo menos 8 caracteres."
            password_field.update()
            _open_snack(page, "Senha deve ter pelo menos 8 caracteres.", "#d84315")
            return

        # Se passou na validação → chama o serviço
        handle_login(
            page=page,
            email=email,
            password=password,
            user_type_index=selected_user_type["value"],
            submit_button=submit_btn
        )

    submit_btn = GradientButton(
        text="Entrar",
        on_click=on_login_click,
        height=button_height,
        width=page.width * 0.9,
    )

    # --------------------------
    # Layout final
    # --------------------------
    return BaseLayout(
        page,
        ft.Column(
            scroll="auto",
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Icon(ft.Icons.ECO_SHARP, color=TERTIARY_COLOR, size=40),
                ft.Text("Bem-vindo(a) de volta!", style=title_style),

                UserTypeToggle(on_change=on_user_type_change),

                email_field,
                password_field,

                ft.Row(
                    [
                        ft.TextButton(
                            "Esqueci minha senha",
                            style=ft.ButtonStyle(
                                color=TERTIARY_COLOR,
                                overlay_color=ft.Colors.TRANSPARENT,
                                padding=ft.padding.symmetric(horizontal=0, vertical=0),
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            on_click=lambda _: page.go("/forgot-password"),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),

                submit_btn,

                ft.Row(
                    controls=[
                        ft.Text(
                            "Não tem uma conta?",
                            style=regular_text_style,
                            color=GREY_COLOR
                        ),
                        ft.TextButton(
                            "Crie uma aqui",
                            style=ft.ButtonStyle(
                                color=TERTIARY_COLOR,
                                overlay_color=ft.Colors.TRANSPARENT,
                                padding=ft.padding.symmetric(horizontal=0, vertical=0),
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            on_click=lambda _: page.go("/register"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                ),
            ],
        )
    )