import flet as ft
from app.core.navigation.routes import Routes
from app.core.theme.theme_resolver import ThemeResolver
from app.core.theme.typography import title_lg, body_primary, body_secondary
from app.core.utils.validators import InputFormatters
from app.modules.auth.controller.auth_controller import AuthController
from app.shared.components.buttons.google_auth_button import GoogleAuthButton
from app.shared.components.buttons.link_button import LinkButton
from app.shared.components.buttons.primary_button import PrimaryButton
from app.shared.components.inputs.password_rules_card import PasswordRulesCard
from app.shared.components.inputs.text_field import AppTextField

def build_register_page(page: ft.Page) -> ft.Control:
    controller = AuthController(page)
    scheme = ThemeResolver.get_scheme(page)
    rules_card = PasswordRulesCard(page=page)

    # --- UI Helpers ---
    def section_title(title: str):
        return ft.Text(title, style=body_primary, color=scheme.primary)

    # --- Campos de Entrada ---
    fields = {
        "email": AppTextField(page=page, label="E-mail"),
        "password": AppTextField(page=page, label="Senha", password=True),
        "confirm_password": AppTextField(page=page, label="Confirmar Senha", password=True),
        "display_name": AppTextField(page=page, label="Como gostaria de ser chamado (a)?"),
        "full_name": AppTextField(page=page, label="Nome completo"),
        "cpf": AppTextField(
            page=page, label="CPF", on_change=InputFormatters.format_input, 
            keyboard_type=ft.KeyboardType.NUMBER, max_length=14
        ),
        "birth_date": AppTextField(
            page=page, label="Data de nascimento", on_change=InputFormatters.format_input, 
            keyboard_type=ft.KeyboardType.NUMBER, max_length=10
        ),
        "corporate_name": AppTextField(page=page, label="Razão social"),
        "cnpj": AppTextField(
            page=page, label="CNPJ", on_change=InputFormatters.format_input, 
            keyboard_type=ft.KeyboardType.NUMBER, max_length=18
        ),
        "is_mei": ft.Checkbox(label="Sou MEI", visible=False),
    }

    # Listeners de UI
    fields["password"].on_change = lambda e: rules_card.update_password(e.control.value)

    # --- Seleção de Tipo de Pessoa ---
    person_type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="PF", label="Pessoa Física"),
            ft.Radio(value="PJ", label="Pessoa Jurídica"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        value="PF",
    )

    # --- Grupos de Campos (Containers Dinâmicos) ---
    display_name_group = ft.Column([
        fields["display_name"],
        ft.Text("Aparecerá em seu perfil, anúncios e chats", style=body_secondary, size=12, color=scheme.outline)
    ], spacing=2)

    pf_container = ft.Column([
        fields["full_name"], display_name_group, fields["cpf"], fields["birth_date"]
    ], visible=True, spacing=20)

    pj_container = ft.Column([
        fields["corporate_name"], display_name_group, fields["cnpj"], fields["is_mei"]
    ], visible=False, spacing=20)

    def toggle_fields(_):
        is_pf = person_type_radio.value == "PF"
        pf_container.visible = is_pf
        pj_container.visible = not is_pf
        fields["is_mei"].visible = not is_pf
        page.update()

    person_type_radio.on_change = toggle_fields

    # --- Ações ---
    google_btn = GoogleAuthButton(on_click=lambda _: controller.login_with_google(button=google_btn))
    
    submit_button = PrimaryButton(
        text="Criar conta",
        on_click=lambda _: controller.register(
            data={
                "person_type": person_type_radio.value,
                "is_mei": fields["is_mei"].value,
                **{k: f.value for k, f in fields.items() if hasattr(f, 'value')},
            },
            submit_button=submit_button,
            fields=fields,
        ),
    )

    return ft.Container(
        padding=ft.padding.symmetric(vertical=62, horizontal=16),
        alignment=ft.alignment.top_center,
        content=ft.Column(
            spacing=20, width=360, scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Column([
                    ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=48, color=scheme.primary),
                    ft.Text("Crie sua conta. É grátis!", style=title_lg, color=scheme.primary),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                ft.Row([google_btn], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("______________ ou ______________", style=body_secondary, color=scheme.outline, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "Cadastre-se em poucos passos para comprar e vender serviços com mais facilidade e segurança.", 
                    style=body_primary, color=scheme.outline, text_align=ft.TextAlign.CENTER
                ),

                section_title("Tipo de conta"),
                person_type_radio,
                pf_container,
                pj_container,

                section_title("Informações de Acesso"),
                fields["email"],
                fields["password"],
                fields["confirm_password"],
                rules_card,

                ft.Container(height=10),
                submit_button,
                
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Já possui uma conta?", style=body_secondary, color=scheme.outline),
                        LinkButton(text="Entre aqui", on_click=lambda _: page.go(Routes.LOGIN)),
                    ],
                ),
            ],
        ),
    )