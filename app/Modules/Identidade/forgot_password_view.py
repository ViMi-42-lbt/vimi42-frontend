import flet as ft
import re

from app.theme import title_style, TERTIARY_COLOR, PRIMARY_COLOR
from app.Modules.GlobalComponents.base_layout import BaseLayout
from app.Modules.GlobalComponents.components import GradientButton
from app.Modules.Identidade.inputs import AppTextField
from app.Modules.Identidade.services import (
    handle_forgot_password_request,
    handle_send_token,
    handle_validate_token,
    handle_reset_password,
    CPF_CNPJ_RE,
    _open_snack,
    format_cpf_cnpj, # <--- Corrigido: Apenas importa a função
)


def build_forgot_password_view(page: ft.Page):
    # --------------------------
    # Botão e Variáveis de UI
    # --------------------------
    button_height = max(page.height * 0.07, 55)
    button_width = page.width * 0.9

    # ============================================
    # ESTADOS INTERNOS
    # ============================================
    # Ref para controlar o passo da recuperação (1 a 4)
    step = ft.Ref[int]()
    step.current = 1

    # Ref para armazenar o ID do usuário retornado na Etapa 1
    user_id = ft.Ref[int]()
    # Ref para armazenar o canal escolhido (email ou sms) na Etapa 2
    selected_channel = ft.Ref[str]()

    # --------------------------
    # FUNÇÃO DE MASKING
    # --------------------------
    def on_cpf_cnpj_change(e):
        """Aplica a máscara no campo CPF/CNPJ em tempo real."""
        
        # 1. Formata o valor digitado usando a função importada do services
        new_value = format_cpf_cnpj(e.control.value)
        
        # 2. Atualiza o campo se a formatação alterou o valor
        if new_value != e.control.value:
            e.control.value = new_value
            e.control.update()


    # Inputs (Ajustado com on_change e keyboard_type)
    cpf_field = AppTextField(
        label="CPF ou CNPJ",
        on_change=on_cpf_cnpj_change,
        keyboard_type=ft.KeyboardType.NUMBER,
        # Limita o número de caracteres formatados
        max_length=18, 
    )
    token_field = AppTextField(
        label="Código recebido",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=6 # Máximo de 6 dígitos para o token
    )
    new_password = AppTextField(
        label="Nova senha", 
        password=True, 
        can_reveal_password=True
    )
    confirm_password = AppTextField(
        label="Confirmar senha", 
        password=True, 
        can_reveal_password=True
    )

    # Coluna para as opções de Email/SMS (Etapa 2)
    options = ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --------------------------
    # Navegação entre passos
    # --------------------------
    def go_to_step(n: int):
        """Atualiza a UI para o passo 'n' da recuperação de senha."""
        # Limpa erros visuais ao trocar de passo
        cpf_field.error_text = None
        token_field.error_text = None
        new_password.error_text = None
        confirm_password.error_text = None
        cpf_field.update()
        token_field.update()
        new_password.update()
        confirm_password.update()
        
        step.current = n
        page_content.controls.clear()
        page_content.controls.extend(step_pages[n]())
        page_content.update()


    # ============================================
    # ETAPA 1 — CPF/CNPJ
    # ============================================
    def on_send_cpf(e):
        """Lida com o envio do CPF/CNPJ para identificação."""
        cpf_cnpj_formatted = (cpf_field.value or "").strip()
        
        # LIMPA ERROS VISUAIS
        cpf_field.error_text = None
        cpf_field.update()

        # Limpa o valor para obter APENAS DÍGITOS para validação e envio
        only_digits = re.sub(r"\D", "", cpf_cnpj_formatted)
        
        # ====== VALIDAÇÃO FRONTEND ======
        
        if not cpf_cnpj_formatted:
            cpf_field.error_text = "Por favor, informe o CPF ou CNPJ."
            cpf_field.update()
            _open_snack(page, "Por favor, informe o CPF ou CNPJ.", "#d84315")
            return

        if not CPF_CNPJ_RE.match(only_digits):
            # A validação CPF_CNPJ_RE verifica se o número de DÍGITOS é 11 ou 14
            cpf_field.error_text = "CPF/CNPJ inválido. Verifique o número."
            cpf_field.update()
            _open_snack(page, "CPF/CNPJ inválido. Verifique o número.", "#d84315")
            return

        # Callback de sucesso
        def on_channels_received(data):
            """Prepara a Etapa 2 (escolha de canal) com os dados mascarados."""
            user_id.current = data["user_id"]

            masked_email = data.get("masked_email")
            masked_phone = data.get("masked_phone")

            options.controls.clear()
            options.controls.append(
                ft.Text("Selecione onde deseja receber o código:", 
                        size=16, 
                        weight=ft.FontWeight.BOLD, 
                        text_align=ft.TextAlign.CENTER, 
                        color=TERTIARY_COLOR)
            )

            # Botões de opção de canal (padronizados com altura e largura)
            if masked_email:
                options.controls.append(
                    GradientButton(
                        text=f"E-mail: {masked_email}",
                        height=button_height,
                        width=button_width,
                        on_click=lambda _: choose_method("email", masked_email)
                    )
                )

            if masked_phone:
                options.controls.append(
                    GradientButton(
                        text=f"SMS: {masked_phone}",
                        height=button_height,
                        width=button_width,
                        on_click=lambda _: choose_method("sms", masked_phone)
                    )
                )

            go_to_step(2)

        # Chama o serviço (se passou na validação)
        handle_forgot_password_request(
            page=page,
            cpf_cnpj=only_digits, # <--- Envia a string limpa (apenas dígitos) para o serviço
            submit_button=e.control,
            on_channels_received=on_channels_received,
        )

    # ============================================
    # ETAPA 2 — Canal
    # ============================================
    def choose_method(method: str, masked_info: str):
        """Lida com a escolha do canal e inicia o envio do token."""
        selected_channel.current = method
        
        _open_snack(page, f"Enviando código para {masked_info}...", PRIMARY_COLOR, 50)
        
        # Chama o serviço. O botão é None pois o clique já foi feito.
        handle_send_token(
            page=page,
            user_id=user_id.current,
            channel=method,
            submit_button=None, # Não há um botão de submit nesta etapa (o botão é o canal escolhido)
            on_token_sent=lambda: go_to_step(3)
        )


    # ============================================
    # ETAPA 3 — Validar código
    # ============================================
    def on_validate_token(e):
        """Lida com a validação do token recebido."""
        token = (token_field.value or "").strip()
        
        # LIMPA ERROS VISUAIS
        token_field.error_text = None
        token_field.update()

        # ====== VALIDAÇÃO FRONTEND ======
        if not token:
            token_field.error_text = "Por favor, informe o código."
            token_field.update()
            _open_snack(page, "Por favor, informe o código.", "#d84315")
            return
            
        if not token.isdigit() or len(token) < 4:
            token_field.error_text = "Código inválido. Deve ser numérico e ter 4 a 6 dígitos."
            token_field.update()
            _open_snack(page, "Código inválido.", "#d84315")
            return

        def validated():
            """Callback de sucesso: avança para a Etapa 4."""
            go_to_step(4)

        # Chama o serviço (se passou na validação)
        handle_validate_token(
            page=page,
            user_id=user_id.current,
            token=token,
            submit_button=e.control,
            on_validated=validated,
        )


    # ============================================
    # ETAPA 4 — Resetar senha
    # ============================================
    def on_reset_password(e):
        """Lida com a definição e confirmação da nova senha."""
        p1 = (new_password.value or "").strip()
        p2 = (confirm_password.value or "").strip()

        # LIMPA ERROS VISUAIS
        new_password.error_text = None
        confirm_password.error_text = None
        new_password.update()
        confirm_password.update()

        # ========== VALIDAÇÃO FRONTEND ===========
        if not p1:
            new_password.error_text = "Informe a nova senha."
            new_password.update()
            _open_snack(page, "Informe a nova senha.", "#d84315")
            return
            
        if len(p1) < 8:
            new_password.error_text = "A senha deve ter pelo menos 8 caracteres."
            new_password.update()
            _open_snack(page, "Senha deve ter pelo menos 8 caracteres.", "#d84315")
            return

        if not p2:
            confirm_password.error_text = "Confirme a nova senha."
            confirm_password.update()
            _open_snack(page, "Confirme a nova senha.", "#d84315")
            return

        if p1 != p2:
            confirm_password.error_text = "As senhas não coincidem."
            confirm_password.update()
            _open_snack(page, "As senhas não coincidem.", "#d84315")
            return

        # Chama o serviço (se passou na validação)
        handle_reset_password(
            page=page,
            user_id=user_id.current,
            password=p1,
            submit_button=e.control
        )

    # ============================================
    # TELAS (Content Builders)
    # ============================================
    step_pages = {
        1: lambda: [
            ft.Icon(ft.Icons.LOCK_RESET_SHARP, color=TERTIARY_COLOR, size=40),
            ft.Text("Recuperar Senha", style=title_style, color=TERTIARY_COLOR),
            ft.Text("Digite seu CPF ou CNPJ para identificar sua conta.", text_align=ft.TextAlign.CENTER, color=TERTIARY_COLOR),
            cpf_field,
            GradientButton(
                text="Continuar",
                height=button_height,
                width=button_width,
                on_click=on_send_cpf
            ),
            ft.TextButton(
                "Voltar ao Login", 
                on_click=lambda _: page.go("/login"),
                style=ft.ButtonStyle(color=TERTIARY_COLOR, overlay_color=ft.Colors.TRANSPARENT, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))
            )
        ],

        2: lambda: [
            ft.Icon(ft.Icons.CONTACT_MAIL_SHARP, color=TERTIARY_COLOR, size=40),
            ft.Text("Escolher Método", style=title_style, color=TERTIARY_COLOR),
            options, # options já contém o título "Como deseja receber..."
            ft.TextButton("Trocar CPF/CNPJ", on_click=lambda _: go_to_step(1))
        ],

        3: lambda: [
            ft.Icon(ft.Icons.VERIFIED_USER_SHARP, color=TERTIARY_COLOR, size=40),
            ft.Text("Verificação de Código", style=title_style, color=TERTIARY_COLOR),
            ft.Text("Um código foi enviado. Digite-o abaixo.", color=TERTIARY_COLOR),
            token_field,
            GradientButton(
                text="Validar Código",
                height=button_height,
                width=button_width,
                on_click=on_validate_token
            ),
            # O botão de "Voltar" aqui permite escolher um canal diferente, o que também reenviaria o código.
            ft.TextButton("Voltar e Reenviar Código", on_click=lambda _: go_to_step(2))
        ],

        4: lambda: [
            ft.Icon(ft.Icons.KEY_SHARP, color=TERTIARY_COLOR, size=40),
            ft.Text("Definir Nova Senha", style=title_style, color=TERTIARY_COLOR),
            ft.Text("Sua nova senha deve ter pelo menos 8 caracteres.", color=TERTIARY_COLOR),
            new_password,
            confirm_password,
            GradientButton(
                text="Redefinir Senha",
                height=button_height,
                width=button_width,
                on_click=on_reset_password
            ),
        ],
    }
    
    # Inicializa o container com o conteúdo do passo 1
    page_content = ft.Column(
        controls=step_pages[step.current](),
        scroll="auto",
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
    )

    return BaseLayout(page, page_content)