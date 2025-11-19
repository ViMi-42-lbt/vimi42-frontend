import flet as ft
import datetime
from typing import Dict, Any, Callable
from app.theme import title_style, TERTIARY_COLOR, PRIMARY_COLOR, GREY_COLOR, PRIMARY_BACKGROUND_COLOR
from app.Modules.GlobalComponents.base_layout import BaseLayout 
from app.Modules.GlobalComponents.components import GradientButton
from app.Modules.Identidade.inputs import AppTextField
# Importando todas as funções de validação e handlers do services.py unificado
from app.Modules.Identidade.services import (
    handle_registration,
    _open_snack,
    format_cpf_cnpj,
    format_cep,
    validate_email,
    validate_password,
    validate_phone,
    validate_zip_code,
    validate_cpf,
    validate_cnpj,
    validate_full_name,
    validate_date,
)

# Constantes de UI
STATE_OPTIONS = [ft.dropdown.Option(s) for s in ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT",
"MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO",
"RR", "SC", "SP", "SE", "TO"]]
BUTTON_HEIGHT = 55
DATE_NOW = datetime.datetime.now()


def build_register_view(page: ft.Page):
    """
    Constrói a View de Registro de Usuário com gerenciamento de passos (PF/PJ)
    e ajustes para garantir o scroll e o funcionamento dos DatePickers.
    """
    # ============================================
    # ESTADOS INTERNOS
    # ============================================
    # 0: Escolha PF/PJ, 1: Form PF, 2: Form PJ
    step = ft.Ref[int]()
    step.current = 0
    
    # Armazena o tipo de usuário escolhido
    user_type = ft.Ref[str]() 
    user_type.current = "PF" 

    # Referências para armazenar os valores de data e os DatePickers
    birth_date_value = ft.Ref[datetime.date | None]()
    opening_date_value = ft.Ref[datetime.date | None]()
    birth_date_value.current = None
    opening_date_value.current = None

    # ============================================
    # INPUTS
    # ============================================
    # Campos comuns
    full_name_field = AppTextField(label="Nome completo") # Inicia com PF
    email_field = AppTextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    phone_field = AppTextField(label="Telefone (DDD + Número)", keyboard_type=ft.KeyboardType.PHONE, max_length=15)
    password_field = AppTextField(label="Senha (mín. 8 caracteres)", password=True, can_reveal_password=True)
    confirm_password_field = AppTextField(label="Confirmar senha", password=True, can_reveal_password=True)

    # Campos de Endereço
    zip_code_field = AppTextField(label="CEP", keyboard_type=ft.KeyboardType.NUMBER, max_length=9)
    street_field = AppTextField(label="Logradouro")
    number_field = AppTextField(label="Número", keyboard_type=ft.KeyboardType.NUMBER, max_length=10)
    neighborhood_field = AppTextField(label="Bairro")
    complement_field = AppTextField(label="Complemento (opcional)")
    city_field = AppTextField(label="Cidade")
    state_unit_field = ft.Dropdown(
        label="Estado (UF)",
        bgcolor=PRIMARY_BACKGROUND_COLOR,
        border_color=GREY_COLOR,
        border_radius=ft.border_radius.all(10),
        border_width=1,
        content_padding=ft.padding.all(14),
        options=STATE_OPTIONS,
        value="SP"
    )

    # Campos PF/PJ específicos
    cpf_field = AppTextField(label="CPF", keyboard_type=ft.KeyboardType.NUMBER, max_length=14)
    cnpj_field = AppTextField(label="CNPJ", keyboard_type=ft.KeyboardType.NUMBER, max_length=18)
    corporate_name_field = AppTextField(label="Nome Fantasia") # PJ only

    # DatePickers Condicionais
    birth_date_button_ref = ft.Ref[ft.ElevatedButton]()
    opening_date_button_ref = ft.Ref[ft.ElevatedButton]()
    
    # ============================================
    # VALIDAÇÕES EM TEMPO REAL (ON_BLUR)
    # ============================================
    
    def validate_full_name_field(e):
        """Valida nome completo quando o campo perde o foco."""
        value = (full_name_field.value or "").strip()
        if not value:
            full_name_field.error_text = "Nome completo é obrigatório."
        elif len(value) < 3:
            full_name_field.error_text = "Nome deve ter pelo menos 3 caracteres."
        else:
            full_name_field.error_text = None
        full_name_field.update()
    
    def validate_email_field(e):
        """Valida email quando o campo perde o foco."""
        value = (email_field.value or "").strip()
        if not value:
            email_field.error_text = "Email é obrigatório."
        else:
            try:
                validate_email(value)
                email_field.error_text = None
            except ValueError as err:
                email_field.error_text = str(err.args[0]) if err.args else "Email inválido."
        email_field.update()
    
    def validate_phone_field(e):
        """Valida telefone quando o campo perde o foco."""
        value = (phone_field.value or "").strip()
        if not value:
            phone_field.error_text = "Telefone é obrigatório."
        elif len(value) < 10:
            phone_field.error_text = "Telefone deve ter DDD + número (mín. 10 dígitos)."
        else:
            phone_field.error_text = None
        phone_field.update()
    
    def validate_password_field(e):
        """Valida senha quando o campo perde o foco."""
        value = (password_field.value or "").strip()
        if not value:
            password_field.error_text = "Senha é obrigatória."
        elif len(value) < 8:
            password_field.error_text = "Senha deve ter pelo menos 8 caracteres."
        else:
            password_field.error_text = None
        password_field.update()
    
    def validate_confirm_password_field(e):
        """Valida confirmação de senha quando o campo perde o foco."""
        value = (confirm_password_field.value or "").strip()
        password_value = (password_field.value or "").strip()
        
        if not value:
            confirm_password_field.error_text = "Confirme sua senha."
        elif value != password_value:
            confirm_password_field.error_text = "As senhas não coincidem."
        else:
            confirm_password_field.error_text = None
        confirm_password_field.update()
    
    def validate_cpf_field(e):
        """Valida CPF quando o campo perde o foco."""
        value = (cpf_field.value or "").strip()
        if not value:
            cpf_field.error_text = "CPF é obrigatório."
        else:
            try:
                validate_cpf(value)
                cpf_field.error_text = None
            except ValueError as err:
                cpf_field.error_text = str(err.args[0]) if err.args else "CPF inválido."
        cpf_field.update()
    
    def validate_cnpj_field(e):
        """Valida CNPJ quando o campo perde o foco."""
        value = (cnpj_field.value or "").strip()
        if not value:
            cnpj_field.error_text = "CNPJ é obrigatório."
        else:
            try:
                validate_cnpj(value)
                cnpj_field.error_text = None
            except ValueError as err:
                cnpj_field.error_text = str(err.args[0]) if err.args else "CNPJ inválido."
        cnpj_field.update()
    
    def validate_zip_code_field(e):
        """Valida CEP quando o campo perde o foco."""
        value = (zip_code_field.value or "").strip()
        if not value:
            zip_code_field.error_text = "CEP é obrigatório."
        else:
            try:
                validate_zip_code(value)
                zip_code_field.error_text = None
            except ValueError as err:
                zip_code_field.error_text = str(err.args[0]) if err.args else "CEP inválido."
        zip_code_field.update()
    
    def validate_street_field(e):
        """Valida logradouro quando o campo perde o foco."""
        value = (street_field.value or "").strip()
        if not value:
            street_field.error_text = "Logradouro é obrigatório."
        else:
            street_field.error_text = None
        street_field.update()
    
    def validate_number_field(e):
        """Valida número quando o campo perde o foco."""
        value = (number_field.value or "").strip()
        if not value:
            number_field.error_text = "Número é obrigatório."
        else:
            number_field.error_text = None
        number_field.update()
    
    def validate_neighborhood_field(e):
        """Valida bairro quando o campo perde o foco."""
        value = (neighborhood_field.value or "").strip()
        if not value:
            neighborhood_field.error_text = "Bairro é obrigatório."
        else:
            neighborhood_field.error_text = None
        neighborhood_field.update()
    
    def validate_city_field(e):
        """Valida cidade quando o campo perde o foco."""
        value = (city_field.value or "").strip()
        if not value:
            city_field.error_text = "Cidade é obrigatória."
        else:
            city_field.error_text = None
        city_field.update()
    
    def validate_corporate_name_field(e):
        """Valida nome fantasia quando o campo perde o foco."""
        value = (corporate_name_field.value or "").strip()
        if not value:
            corporate_name_field.error_text = "Nome Fantasia é obrigatório."
        else:
            corporate_name_field.error_text = None
        corporate_name_field.update()
    
    # Adiciona os validadores on_blur aos campos
    full_name_field.on_blur = validate_full_name_field
    email_field.on_blur = validate_email_field
    phone_field.on_blur = validate_phone_field
    password_field.on_blur = validate_password_field
    confirm_password_field.on_blur = validate_confirm_password_field
    cpf_field.on_blur = validate_cpf_field
    cnpj_field.on_blur = validate_cnpj_field
    zip_code_field.on_blur = validate_zip_code_field
    street_field.on_blur = validate_street_field
    number_field.on_blur = validate_number_field
    neighborhood_field.on_blur = validate_neighborhood_field
    city_field.on_blur = validate_city_field
    corporate_name_field.on_blur = validate_corporate_name_field
    
    # ============================================
    # FUNÇÕES DE UI
    # ============================================
    
    # Referência para o container principal de conteúdo
    page_content_ref = ft.Ref[ft.Column]()

    def go_to_step(n: int, new_user_type: str):
        """Atualiza a UI para o passo 'n' e define o tipo de usuário."""
        
        # 1. Atualiza o tipo de usuário e o label do campo de nome
        user_type.current = new_user_type
        is_pj = new_user_type == "PJ"
        full_name_field.label = "Razão Social" if is_pj else "Nome completo"
        
        # 2. Limpa erros visuais e valores de campo ao trocar (para evitar confusão)
        for control in [full_name_field, email_field, password_field, confirm_password_field,
                         zip_code_field, cpf_field, cnpj_field, corporate_name_field]:
            if hasattr(control, 'error_text') and control.error_text: 
                control.error_text = None
            if hasattr(control, 'value') and control.value:
                 control.value = "" # Limpa campos para evitar que dados PF apareçam em PJ
        
        # 3. Atualiza o passo e o conteúdo
        step.current = n
        page_content_ref.current.controls.clear()
        # step_pages[n]() deve retornar uma lista de ft.Controls — mantemos assim
        page_content_ref.current.controls.extend(step_pages[n]())
        
        # CRUCIAL para o Scroll: Volta o scroll para o topo ao mudar de tela
        try:
            page_content_ref.current.scroll_to(offset=0)
        except Exception:
            # se houver qualquer problema com scroll, evita crash da UI
            pass
        
        page.update() 

    # --------------------------
    # MASKING
    # --------------------------
    def on_cpf_cnpj_change(e):
        """Aplica a máscara no campo CPF/CNPJ em tempo real."""
        new_value = format_cpf_cnpj(e.control.value)
        if new_value != e.control.value:
            e.control.value = new_value
            e.control.update()

    def on_cep_change(e):
        """Aplica a máscara no campo CEP em tempo real."""
        new_value = format_cep(e.control.value)
        if new_value != e.control.value:
            e.control.value = new_value
            e.control.update()
    
    # Adiciona listeners de mask ao inicializar
    cpf_field.on_change = on_cpf_cnpj_change
    cnpj_field.on_change = on_cpf_cnpj_change
    zip_code_field.on_change = on_cep_change

    # --------------------------
    # DATE PICKERS (CORRIGIDOS + MELHORIAS)
    # --------------------------
    
    # REMOVIDO: Não configurar page.locale e page.theme aqui
    # Isso deve ser feito apenas no main.py ou theme.py para evitar conflitos
    
    def on_date_selected(e: ft.ControlEvent, date_ref: ft.Ref[datetime.date | None], button_ref: ft.Ref[ft.ElevatedButton], label: str, picker: ft.DatePicker):
        """Handler genérico para seleção de data."""
        date_ref.current = e.control.value
        # Atualiza a cor para o padrão (caso estivesse vermelha por erro)
        if button_ref.current:
            button_ref.current.style = ft.ButtonStyle(
                bgcolor=PRIMARY_BACKGROUND_COLOR,
                color=TERTIARY_COLOR,
                icon_color=TERTIARY_COLOR,
                overlay_color=PRIMARY_COLOR,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, GREY_COLOR)},
            )
            button_ref.current.text = f"{label}: {date_ref.current.strftime('%d/%m/%Y')}"
            button_ref.current.update()
        # Fecha o picker
        picker.open = False
        page.update()

    def open_date_picker(picker: ft.DatePicker):
        """Abre o DatePicker de forma correta."""
        picker.open = True
        page.update()

    # 1. DatePicker de Pessoa Física (Nascimento)
    birth_date_picker = ft.DatePicker(
        first_date=datetime.datetime(1900, 1, 1),
        last_date=DATE_NOW,
        on_change=lambda e: on_date_selected(e, birth_date_value, birth_date_button_ref, "Data Nasc.", birth_date_picker)
    )
    birth_date_button = ft.ElevatedButton(
        ref=birth_date_button_ref,
        text="Selecionar Data de Nascimento",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: open_date_picker(birth_date_picker),
        style=ft.ButtonStyle(
            bgcolor=PRIMARY_BACKGROUND_COLOR,
            color=TERTIARY_COLOR,
            icon_color=TERTIARY_COLOR,
            overlay_color=PRIMARY_COLOR,
            side={ft.ControlState.DEFAULT: ft.BorderSide(1, GREY_COLOR)},
        ),
    )
    
    # 2. DatePicker de Pessoa Jurídica (Abertura)
    opening_date_picker = ft.DatePicker(
        first_date=datetime.datetime(1900, 1, 1),
        last_date=DATE_NOW,
        on_change=lambda e: on_date_selected(e, opening_date_value, opening_date_button_ref, "Data Abert.", opening_date_picker)
    )
    opening_date_button = ft.ElevatedButton(
        ref=opening_date_button_ref,
        text="Selecionar Data de Abertura",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: open_date_picker(opening_date_picker),
        style=ft.ButtonStyle(
            bgcolor=PRIMARY_BACKGROUND_COLOR,
            color=TERTIARY_COLOR,
            icon_color=TERTIARY_COLOR,
            overlay_color=PRIMARY_COLOR,
            side={ft.ControlState.DEFAULT: ft.BorderSide(1, GREY_COLOR)},
        ),
    )

    # ============================================
    # VALIDAÇÃO E HANDLERS
    # ============================================

    def validate_and_collect_data() -> Dict[str, Any] | None:
        """Valida todos os campos do formulário (PF ou PJ) e coleta os dados limpos."""
        
        data: Dict[str, Any] = {"type": user_type.current}
        
        # Lista para armazenar campos com erro
        fields_with_errors = []
        first_error_control = None
        
        # 1. Limpar erros visuais
        all_controls = [full_name_field, email_field, phone_field, password_field, confirm_password_field,
                         zip_code_field, street_field, number_field, neighborhood_field, city_field,
                         cpf_field, cnpj_field, corporate_name_field, state_unit_field]
        
        for field in all_controls:
            if hasattr(field, 'error_text') and field.error_text: 
                field.error_text = None
                if hasattr(field, 'update'): field.update()
        
        # Resetar estilo de erro nos botões de data
        if birth_date_button_ref.current: 
            birth_date_button_ref.current.style = ft.ButtonStyle(
                bgcolor=PRIMARY_BACKGROUND_COLOR,
                color=TERTIARY_COLOR,
                icon_color=TERTIARY_COLOR,
                overlay_color=PRIMARY_COLOR,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, GREY_COLOR)},
            )
            birth_date_button_ref.current.update()
        if opening_date_button_ref.current: 
            opening_date_button_ref.current.style = ft.ButtonStyle(
                bgcolor=PRIMARY_BACKGROUND_COLOR,
                color=TERTIARY_COLOR,
                icon_color=TERTIARY_COLOR,
                overlay_color=PRIMARY_COLOR,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, GREY_COLOR)},
            )
            opening_date_button_ref.current.update()

        # 2. Executar validações com try/except
        try:
            # Comuns
            try:
                data["full_name"] = validate_full_name(full_name_field.value)
            except ValueError as e:
                fields_with_errors.append(("Nome completo", full_name_field))
                if not first_error_control: first_error_control = full_name_field
                raise
            
            try:
                data["email"] = validate_email(email_field.value)
            except ValueError as e:
                fields_with_errors.append(("Email", email_field))
                if not first_error_control: first_error_control = email_field
                raise
            
            try:
                data["phone_number"] = validate_phone(phone_field.value)
            except ValueError as e:
                fields_with_errors.append(("Telefone", phone_field))
                if not first_error_control: first_error_control = phone_field
                raise
            
            try:
                data["password"] = validate_password(password_field.value, confirm_password_field.value)
            except ValueError as e:
                fields_with_errors.append(("Senha", password_field))
                if not first_error_control: first_error_control = password_field
                raise
            
            # Endereço
            try:
                data["zip_code"] = validate_zip_code(zip_code_field.value)
            except ValueError as e:
                fields_with_errors.append(("CEP", zip_code_field))
                if not first_error_control: first_error_control = zip_code_field
                raise
            
            data["street"] = (street_field.value or "").strip()
            data["number"] = (number_field.value or "").strip()
            data["neighborhood"] = (neighborhood_field.value or "").strip()
            data["complement"] = (complement_field.value or "").strip()
            data["city"] = (city_field.value or "").strip()
            data["federative_unit"] = state_unit_field.value
            
            if not data["street"]: 
                fields_with_errors.append(("Logradouro", street_field))
                if not first_error_control: first_error_control = street_field
                raise ValueError("Logradouro é obrigatório.", street_field)
            if not data["number"]: 
                fields_with_errors.append(("Número", number_field))
                if not first_error_control: first_error_control = number_field
                raise ValueError("Número é obrigatório.", number_field)
            if not data["neighborhood"]: 
                fields_with_errors.append(("Bairro", neighborhood_field))
                if not first_error_control: first_error_control = neighborhood_field
                raise ValueError("Bairro é obrigatório.", neighborhood_field)
            if not data["city"]: 
                fields_with_errors.append(("Cidade", city_field))
                if not first_error_control: first_error_control = city_field
                raise ValueError("Cidade é obrigatória.", city_field)
            if not data["federative_unit"]: 
                fields_with_errors.append(("Estado", state_unit_field))
                if not first_error_control: first_error_control = state_unit_field
                raise ValueError("Estado é obrigatório.", state_unit_field)

            # Específicos PF/PJ
            if user_type.current == "PF":
                try:
                    data["cpf"] = validate_cpf(cpf_field.value)
                except ValueError as e:
                    fields_with_errors.append(("CPF", cpf_field))
                    if not first_error_control: first_error_control = cpf_field
                    raise
                
                try:
                    data["birth_date"] = validate_date(birth_date_value.current, "Data de Nascimento", birth_date_button_ref.current)
                except ValueError as e:
                    fields_with_errors.append(("Data de Nascimento", birth_date_button_ref.current))
                    if not first_error_control: first_error_control = birth_date_button_ref.current
                    raise
                
                data["cnpj"] = None
                data["corporate_name"] = None
                data["opening_date"] = None
            else: # PJ
                try:
                    data["cnpj"] = validate_cnpj(cnpj_field.value)
                except ValueError as e:
                    fields_with_errors.append(("CNPJ", cnpj_field))
                    if not first_error_control: first_error_control = cnpj_field
                    raise
                
                data["corporate_name"] = (corporate_name_field.value or "").strip()
                if not data["corporate_name"]: 
                    fields_with_errors.append(("Nome Fantasia", corporate_name_field))
                    if not first_error_control: first_error_control = corporate_name_field
                    raise ValueError("Nome Fantasia é obrigatório.", corporate_name_field)
                
                try:
                    data["opening_date"] = validate_date(opening_date_value.current, "Data de Abertura", opening_date_button_ref.current)
                except ValueError as e:
                    fields_with_errors.append(("Data de Abertura", opening_date_button_ref.current))
                    if not first_error_control: first_error_control = opening_date_button_ref.current
                    raise
                
                data["cpf"] = None
                data["birth_date"] = None
            
            return data

        except ValueError as e:
            # Lógica de exibição de erro MELHORADA
            msg = str(e)
            control_ref = None

            if len(e.args) > 1 and isinstance(e.args[1], ft.Control):
                msg = e.args[0]
                control_ref = e.args[1]

            # Mostra mensagem de erro mais informativa
            if len(fields_with_errors) > 1:
                error_summary = f"Corrija {len(fields_with_errors)} campos: {fields_with_errors[0][0]}"
                if len(fields_with_errors) > 2:
                    error_summary += f" e mais {len(fields_with_errors) - 1}"
                _open_snack(page, error_summary, ft.Colors.RED_600)
            else:
                _open_snack(page, msg, ft.Colors.RED_600)

            # Marca TODOS os campos com erro visualmente
            for field_name, field_control in fields_with_errors:
                if hasattr(field_control, 'error_text'):
                    field_control.error_text = f"{field_name} inválido ou obrigatório"
                    field_control.update()
                elif field_control in [birth_date_button_ref.current, opening_date_button_ref.current]:
                    field_control.style = ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_50,
                        color=ft.Colors.RED_500,
                        icon_color=ft.Colors.RED_500,
                        side={ft.ControlState.DEFAULT: ft.BorderSide(2, ft.Colors.RED_500)},
                    )
                    field_control.update()

            # SCROLL até o primeiro campo com erro
            if first_error_control and page_content_ref.current:
                try:
                    # Tenta focar no primeiro campo com erro
                    if hasattr(first_error_control, 'focus'):
                        first_error_control.focus()
                    # Faz scroll suave até o topo para mostrar o erro
                    page_content_ref.current.scroll_to(offset=0, duration=300)
                except Exception:
                    pass
            
            return None

    def on_register_click(e):
        """Lida com o clique no botão de registro após validação."""
        user_data = validate_and_collect_data()
        if user_data:
            handle_registration(page, user_data, e.control)

    # --------------------------
    # HANDLERS DE SELEÇÃO DE TIPO
    # --------------------------
    
    def select_pf(e): go_to_step(1, "PF")
    def select_pj(e): go_to_step(2, "PJ")


    # ============================================
    # TELAS (Content Builders)
    # ============================================

    def UserTypeCard(
        icon,
        title: str,
        description: str,
        on_click: Callable[[ft.ControlEvent], None]
    ) -> ft.Container:
        """Cria o card de seleção PF/PJ no estilo da imagem."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Icon(icon, size=30, color=PRIMARY_COLOR),
                            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text(
                                description,
                                size=12,
                                color=ft.Colors.BLACK54,
                                max_lines=2,
                                text_align=ft.TextAlign.START,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True
                    ),
                    ft.Icon(ft.Icons.ARROW_FORWARD, color=PRIMARY_COLOR),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            width=300, 
            padding=ft.padding.all(15),
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=ft.border_radius.all(12),
            on_click=on_click,
            ink=True, 
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 1),
            ),
        )

    def step_zero():
        """Etapa 0: Escolha PF ou PJ - Novo design de cards."""
        return [
            ft.Text("Crie sua conta", style=title_style, color=TERTIARY_COLOR),
            ft.Text(
                "Escolha o tipo de cadastro e tenha acesso aos serviços disponíveis para você.",
                color=TERTIARY_COLOR,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            
            # Layout dos cards lado a lado (Row)
            ft.Column(
                controls=[
                    UserTypeCard(
                        icon=ft.Icons.PERSON_OUTLINED,
                        title="Pessoa Física",
                        description="Para cidadãos que desejam acessar serviços ou clientes individuais.",
                        on_click=select_pf,
                    ),
                    UserTypeCard(
                        icon=ft.Icons.BUSINESS_OUTLINED,
                        title="Pessoa Jurídica",
                        description="Para empresas que precisam acessar serviços ou clientes específicos.",
                        on_click=select_pj,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            ),
            
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

            # Já possui conta? Fazer login
            ft.Row(
                spacing=2,
                controls=[
                    ft.Text("Já possui conta?", color=GREY_COLOR),
                    ft.TextButton(
                        "Fazer login",
                        on_click=lambda _: page.go("/login"),
                        style=ft.ButtonStyle(
                            color=TERTIARY_COLOR,
                            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            overlay_color=ft.Colors.TRANSPARENT
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
                
            )
        ]

    # Campos de endereço padrão para reuso
    address_fields = [
        zip_code_field,
        street_field,
        ft.Row(
            controls=[
                ft.Container(number_field, expand=2),
                ft.Container(neighborhood_field, expand=3),
            ],
            spacing=10
        ),
        complement_field,
        ft.Row(
            controls=[
                ft.Container(city_field, expand=2),
                ft.Container(state_unit_field, expand=1),
            ],
            spacing=10
        ),
    ]

    def step_one_pf():
        """Etapa 1: Formulário de Pessoa Física."""

        finalizar_btn = GradientButton(
            text="Finalizar Cadastro",
            on_click=on_register_click,
            height=button_height,
            width=page.width * 0.9,
        )

        return [
            ft.Icon(ft.Icons.PERSON_SHARP, color=TERTIARY_COLOR, size=40),
            ft.Text("Cadastro de Pessoa Física", style=title_style, text_align=ft.TextAlign.CENTER, color=TERTIARY_COLOR),
            ft.Text("Preencha seus dados pessoais para continuar.", text_align=ft.TextAlign.CENTER, color=TERTIARY_COLOR),
            
            full_name_field, email_field, phone_field,
            password_field, confirm_password_field,
            ft.Row(
                controls=[
                    ft.Container(cpf_field, expand=2),
                    ft.Container(birth_date_button, expand=3),
                ],
                spacing=10
            ),

            *address_fields,
            
            ft.Container(height=20), # Espaçamento extra antes do botão final

            # adiciona o botão diretamente — NÃO chamar métodos internos
            finalizar_btn,

            ft.TextButton(
                "Voltar",
                on_click=lambda _: go_to_step(0, user_type.current),
                height=button_height,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    color=TERTIARY_COLOR
                )
            )
        ]

    button_height = max(page.height * 0.07, 55)

    def step_two_pj():
        """Etapa 2: Formulário de Pessoa Jurídica."""

        finalizar_btn = GradientButton(
            text="Finalizar Cadastro",
            on_click=on_register_click,
            height=button_height,
            width=page.width * 0.9,
        )
        
        return [
            ft.Icon(ft.Icons.BUSINESS_SHARP, color=TERTIARY_COLOR, size=40),
            ft.Text("Cadastro de Pessoa Jurídica", style=title_style, text_align=ft.TextAlign.CENTER, color=TERTIARY_COLOR),
            ft.Text("Preencha os dados da sua empresa para continuar.", text_align=ft.TextAlign.CENTER, color=TERTIARY_COLOR),
            
            full_name_field, # Razão Social
            corporate_name_field, # Nome Fantasia
            email_field, phone_field,
            password_field, confirm_password_field,
            ft.Row(
                controls=[
                    ft.Container(cnpj_field, expand=2),
                    ft.Container(opening_date_button, expand=3),
                ],
                spacing=10
            ),
            
            *address_fields,
            
            ft.Container(height=20), # Espaçamento extra antes do botão final
            
            # adiciona o botão diretamente — NÃO chamar métodos internos
            finalizar_btn,

            ft.TextButton(
                "Voltar",
                on_click=lambda _: go_to_step(0, user_type.current),
                height=button_height,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    color=TERTIARY_COLOR
                )
            )
        ]


    step_pages = {
        0: step_zero,
        1: step_one_pf,
        2: step_two_pj,
    }
    
    # 1. DEFINE O CONTEÚDO PRINCIPAL (ft.Column)
    page_content = ft.Column(
        ref=page_content_ref, 
        controls=step_pages[step.current](), # Inicia com o conteúdo do passo 0
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
    )
    
    # 2. GARANTE QUE OS DATE PICKERS ESTEJAM NO OVERLAY DA PÁGINA (Antes do retorno)
    page.overlay.append(birth_date_picker)
    page.overlay.append(opening_date_picker)
    
    # 3. RETORNA O BASELAYOUT ENVOLVENDO DIRETAMENTE O page_content
    return BaseLayout(page, page_content)