import flet as ft
import threading
import requests
import re
import datetime
from typing import Callable, Dict, Any, Optional

from app.theme import SOFT_BLACK_COLOR, PRIMARY_COLOR
# NOTA: O API_BASE_URL é importado de app.Modules.GlobalComponents.services,
# assumindo que você possui esse arquivo com a URL base definida.
from app.Modules.GlobalComponents.services import API_BASE_URL 

# ===============================================================
# ====================== REGEX E CONSTANTES =====================
# ===============================================================

# Regex geral para validação de formato
CPF_CNPJ_RE = re.compile(r"^(\d{11}|\d{14})$")
CPF_RE = re.compile(r"^\d{11}$")
CNPJ_RE = re.compile(r"^\d{14}$")
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PHONE_RE = re.compile(r"^\d{10,11}$") # 10 digitos (sem 9º) ou 11 digitos (com 9º)
ZIP_CODE_RE = re.compile(r"^\d{8}$")
PASSWORD_MIN_LENGTH = 8

# ===============================================================
# ====================== UTILITIES (Geral) ======================
# ===============================================================

def _open_snack(page: ft.Page, text: str, color=SOFT_BLACK_COLOR, seconds: int = 4):
    """Exibe um SnackBar (notificação) na parte inferior da tela."""
    page.snack_bar = ft.SnackBar(
        content=ft.Text(text),
        bgcolor=color,
        open=True,
        duration=seconds * 1000, # Flet usa milissegundos
    )
    page.update()


def _enable(control: ft.Control, enabled: bool):
    """Auxiliar para habilitar/desabilitar controle (e.g., botão)."""
    if control:
        control.disabled = not enabled
        control.update()

# ===============================================================
# ====================== FORMATTERS E VALIDATORS ================
# ===============================================================

def format_cpf_cnpj(text: str) -> str:
    """Aplica a máscara de CPF (11 dígitos) ou CNPJ (14 dígitos)."""
    digits = re.sub(r'\D', '', text)
    length = len(digits)
    
    if length <= 11: # CPF
        formatted = ''
        if length > 0: formatted += digits[:3]
        if length > 3: formatted += '.' + digits[3:6]
        if length > 6: formatted += '.' + digits[6:9]
        if length > 9: formatted += '-' + digits[9:11]
        return formatted[:14] if length <= 11 else digits
    else: # CNPJ
        formatted = ''
        if length > 0: formatted += digits[:2]
        if length > 2: formatted += '.' + digits[2:5]
        if length > 5: formatted += '.' + digits[5:8]
        if length > 8: formatted += '/' + digits[8:12]
        if length > 12: formatted += '-' + digits[12:14]
        return formatted[:18] if length <= 14 else digits

def format_cep(text: str) -> str:
    """Aplica a máscara de CEP (5 dígitos + hífen + 3 dígitos)."""
    digits = re.sub(r'\D', '', text)
    length = len(digits)
    
    formatted = ''
    if length > 0: formatted += digits[:5]
    if length > 5: formatted += '-' + digits[5:8]
    
    return formatted[:9] if length <= 8 else digits

def _clean_and_validate_field(value: Optional[str], pattern: re.Pattern, error_message: str, clean_digits: bool = False) -> str:
    """Limpa o valor do campo e verifica o padrão regex."""
    value = (value or "").strip()
    
    if clean_digits:
        cleaned = re.sub(r"\D", "", value)
    else:
        cleaned = value
        
    if not cleaned:
        raise ValueError("O campo é obrigatório.")
    
    if not pattern.match(cleaned):
        raise ValueError(error_message)
    
    return cleaned

# Funções específicas de validação (retorna o valor limpo ou lança ValueError)
def validate_full_name(name: Optional[str]) -> str:
    if not (name or "").strip():
        raise ValueError("O nome/razão social é obrigatório.")
    return (name or "").strip()

def validate_email(email: Optional[str]) -> str:
    return _clean_and_validate_field(email, EMAIL_RE, "Email inválido.")

def validate_password(password: Optional[str], confirm: Optional[str]) -> str:
    p = (password or "").strip()
    c = (confirm or "").strip()
    
    if len(p) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"A senha deve ter no mínimo {PASSWORD_MIN_LENGTH} caracteres.")
    if p != c:
        raise ValueError("As senhas não coincidem.")
    return p

def validate_phone(phone: Optional[str]) -> str:
    cleaned = re.sub(r"\D", "", phone or "")
    return _clean_and_validate_field(cleaned, PHONE_RE, "Telefone inválido (inclua o DDD).", clean_digits=True)

def validate_zip_code(zip_code: Optional[str]) -> str:
    cleaned = re.sub(r"\D", "", zip_code or "")
    return _clean_and_validate_field(cleaned, ZIP_CODE_RE, "CEP inválido (8 dígitos).", clean_digits=True)

def validate_cpf(cpf: Optional[str]) -> str:
    cleaned = re.sub(r"\D", "", cpf or "")
    return _clean_and_validate_field(cleaned, CPF_RE, "CPF inválido (11 dígitos).", clean_digits=True)

def validate_cnpj(cnpj: Optional[str]) -> str:
    cleaned = re.sub(r"\D", "", cnpj or "")
    return _clean_and_validate_field(cleaned, CNPJ_RE, "CNPJ inválido (14 dígitos).", clean_digits=True)

def validate_date(date_value: Optional[datetime.date], field_name: str) -> datetime.date:
    """Valida se a data foi selecionada."""
    if not date_value:
        raise ValueError(f"A {field_name} é obrigatória.")
    return date_value

# ===============================================================
# ========================== LOGIN ===============================
# ===============================================================

def handle_login(
    page: ft.Page,
    email: str,
    password: str,
    user_type_index: int,
    submit_button: ft.Control = None
):
    """
    Função principal para lidar com a solicitação de login
    e roteamento para a página inicial do usuário.
    """

    user_type = 0 if user_type_index in (0, "0") else 1

    if submit_button:
        _enable(submit_button, False)

    _open_snack(page, "Conectando...", PRIMARY_COLOR, 60)

    def _request():
        try:
            # --- SIMULAÇÃO DE REQUESTS INÍCIO ---
            # resp = requests.post(
            #     f"{API_BASE_URL}/auth/login",
            #     json={"email": email, "password": password, "user_type": user_type},
            #     headers={"Content-Type": "application/json"},
            #     timeout=10
            # )
            
            # SIMULAÇÃO: 
            resp_status_code = 200
            data = {"user_type": ["CLIENTE"], "id_user": 1}
            # FIM DA SIMULAÇÃO

            page.snack_bar.open = False
            page.update()

            if resp_status_code == 200:
                backend_user_types = data.get("user_type", [])
                user_id = data.get("id_user")

                # Cliente
                if user_type == 0:
                    _open_snack(page, "Login realizado!", PRIMARY_COLOR)
                    page.go("/inicio-cliente")
                    return

                # Prestador já ativado
                if "PRESTADOR" in backend_user_types:
                    _open_snack(page, "Bem-vindo(a) prestador!", PRIMARY_COLOR)
                    page.go("/inicio-prestador")
                    return

                # Pergunta sobre ativar prestador
                _ask_activate_prestador(page, user_id)
                return

            # Erros conhecidos
            if resp_status_code == 401: # Simulação de resp.status_code
                _open_snack(page, "Credenciais inválidas.", "#d84315")

            elif resp_status_code == 404:
                _open_snack(page, "Usuário não encontrado.", "#d84315")

            elif resp_status_code == 422:
                # msg = resp.json().get("detail", "Dados inválidos.")
                msg = "Dados inválidos (simulação)."
                _open_snack(page, f"Validação: {msg}", "#d84315")

            else:
                _open_snack(page, f"Erro inesperado ({resp_status_code}).", "#d84315")

        except Exception as ex:
            _open_snack(page, f"Erro de conexão/inesperado: {ex}", "#d84315")

        finally:
            if submit_button:
                _enable(submit_button, True)

    threading.Thread(target=_request, daemon=True).start()


def _ask_activate_prestador(page: ft.Page, user_id: int):
    """Exibe um diálogo para perguntar se o usuário deseja ativar a conta de prestador."""
    def activate_prestador():
        """Chama a API para ativar a conta de prestador."""
        try:
            # Fechando o diálogo antes da requisição para melhorar a UX
            setattr(dialog, "open", False)
            page.update() 
            
            # --- SIMULAÇÃO DE REQUESTS INÍCIO ---
            # resp = requests.post(f"{API_BASE_URL}/users/{user_id}/activate-prestador", timeout=10)
            # if resp.status_code == 200:
            
            # SIMULAÇÃO:
            success = True
            # FIM DA SIMULAÇÃO
            
            if success:
                _open_snack(page, "Prestador ativado!", PRIMARY_COLOR)
                page.go("/inicio-prestador")
            else:
                 _open_snack(page, f"Erro ao ativar prestador.", "#d84315")
                 
        except:
            _open_snack(page, "Erro de conexão ao ativar prestador.", "#d84315")

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Ativar conta prestador?"),
        content=ft.Text(
            "Sua conta ainda não está habilitada como prestador.\nDeseja ativar agora?"
        ),
        actions=[
            ft.TextButton(
                "Não",
                on_click=lambda e: (
                    setattr(dialog, "open", False),
                    page.update(),
                    page.go("/inicio-cliente")
                )
            ),
            ft.TextButton(
                "Sim",
                on_click=lambda e: activate_prestador()
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = dialog
    dialog.open = True
    page.update()


# ===============================================================
# ======================== REGISTRO ==============================
# ===============================================================

def handle_registration(page: ft.Page, user_data: Dict[str, Any], submit_button: ft.Control):
    """
    Função principal para lidar com a solicitação de registro.
    Recebe dados *já validados e limpos* da View.
    """
    if submit_button:
        _enable(submit_button, False)
        
    _open_snack(page, "Processando seu cadastro...", PRIMARY_COLOR, 60)

    def _request():
        try:
            # Prepara o payload, formatando as datas de datetime.date para string (ISO)
            payload = {
                "type": user_data["type"],
                "full_name": user_data["full_name"],
                "email": user_data["email"],
                "password": user_data["password"], 
                "phone_number": user_data["phone_number"],
                "zip_code": user_data["zip_code"],
                "street": user_data["street"],
                "number": user_data["number"],
                "neighborhood": user_data["neighborhood"],
                "complement": user_data["complement"],
                "city": user_data["city"],
                "federative_unit": user_data["federative_unit"],
                
                # Campos condicionais
                "cpf": user_data.get("cpf"),
                "cnpj": user_data.get("cnpj"),
                "corporate_name": user_data.get("corporate_name"),
                
                # Datas (Formatadas para YYYY-MM-DD)
                "birth_date": user_data.get("birth_date").strftime("%Y-%m-%d") if user_data.get("birth_date") else None,
                "opening_date": user_data.get("opening_date").strftime("%Y-%m-%d") if user_data.get("opening_date") else None,
            }
            
            # --- AQUI ENTRARIA A CHAMADA REQUESTS.POST REAL PARA O BACKEND ---
            # resp = requests.post(f"{API_BASE_URL}/auth/register", json=payload, timeout=10)

            # Simulação de sucesso (Assumindo que a requisição real foi um sucesso 201 ou 200)
            print("Dados de registro enviados:", payload)
            
            page.snack_bar.open = False
            page.update()
            
            _open_snack(page, "Cadastro realizado com sucesso! Redirecionando para o Login.", PRIMARY_COLOR)
            
            # Redirecionamento 
            page.go("/login")
            
        except Exception as e:
            page.snack_bar.open = False
            page.update()
            error_message = f"Erro no cadastro: {str(e)}"
            _open_snack(page, error_message, "#d84315")
            
        finally:
            if submit_button:
                _enable(submit_button, True)
    
    threading.Thread(target=_request, daemon=True).start()


# ===============================================================
# ==================== RECUPERAÇÃO DE SENHA =====================
# ===============================================================

# As funções de recuperação de senha usam a lógica requests/threading do seu arquivo original.
# O `format_cpf_cnpj` foi movido para a seção de formatters.

def handle_forgot_password_request(
    page: ft.Page,
    cpf_cnpj: str,
    submit_button: ft.Control, 
    on_channels_received: callable,
):
    """
    Etapa 1 — Recebe o CPF/CNPJ (apenas dígitos), consulta na API e
    retorna os canais disponíveis (email / sms).
    """
    
    # Nota: cpf_cnpj é esperado APENAS COM DÍGITOS, pois a View faz a limpeza.

    _enable(submit_button, False)
    _open_snack(page, "Consultando usuário...", PRIMARY_COLOR, 50)

    def _request():
        # Lógica de requests e threading mantida do seu código original
        try:
            # --- SIMULAÇÃO DE REQUESTS INÍCIO ---
            # resp = requests.post(f"{API_BASE_URL}/auth/password/identify", json={"cpf_cnpj": cpf_cnpj}, timeout=10)
            
            # SIMULAÇÃO (SUCESSO):
            data = {"user_id": 123, "masked_email": "u***@exemplo.com", "masked_phone": "(11) 9****-1234"}
            resp_status_code = 200
            # FIM DA SIMULAÇÃO

            # Fecha snack
            page.snack_bar.open = False
            page.update()

            if resp_status_code == 404:
                _open_snack(page, "Usuário não encontrado.", "#d84315")
                return

            if resp_status_code != 200:
                _open_snack(page, f"Erro ao consultar usuário ({resp_status_code}).", "#d84315")
                return

            # Sucesso
            on_channels_received(data)
            return 

        except Exception:
            _open_snack(page, "Erro de conexão inesperado.", "#d84315")

        finally:
            _enable(submit_button, True) 

    threading.Thread(target=_request, daemon=True).start()

def handle_send_token(
    page: ft.Page,
    user_id: int,
    channel: str,
    submit_button: ft.Control,
    on_token_sent: callable,
):
    """
    Etapa 2 — Envia o token de verificação por email ou SMS.
    (Lógica mantida do seu código original)
    """

    _enable(submit_button, False)
    _open_snack(page, "Enviando código...", PRIMARY_COLOR, 50)

    def _request():
        try:
            # --- SIMULAÇÃO DE REQUESTS INÍCIO ---
            # resp = requests.post(f"{API_BASE_URL}/auth/password/send-token", json={"user_id": user_id, "channel": channel}, timeout=10)
            
            # SIMULAÇÃO (SUCESSO):
            resp_status_code = 200
            # FIM DA SIMULAÇÃO

            page.snack_bar.open = False
            page.update()

            if resp_status_code != 200:
                _open_snack(page, "Falha ao enviar token. Tente novamente.", "#d84315")
                return

            _open_snack(page, "Código de verificação enviado! Prossiga para a validação.", PRIMARY_COLOR)
            on_token_sent()

        except Exception:
            _open_snack(page, "Erro de conexão ou ao enviar token.", "#d84315")

        finally:
            _enable(submit_button, True) 

    threading.Thread(target=_request, daemon=True).start()

def handle_validate_token(
    page: ft.Page,
    user_id: int,
    token: str,
    submit_button: ft.Control,
    on_validated: callable,
):
    """
    Etapa 3 — Validação do token enviado para email/sms.
    (Lógica mantida do seu código original)
    """

    _enable(submit_button, False)
    _open_snack(page, "Validando token...", PRIMARY_COLOR, 50)

    def _request():
        try:
            # --- SIMULAÇÃO DE REQUESTS INÍCIO ---
            # resp = requests.post(f"{API_BASE_URL}/auth/password/validate", json={"user_id": user_id, "token": token}, timeout=10)
            
            # SIMULAÇÃO (SUCESSO):
            if token == "123456": # Token de simulação de sucesso
                resp_status_code = 200
            else:
                resp_status_code = 400
            # FIM DA SIMULAÇÃO

            page.snack_bar.open = False
            page.update()

            if resp_status_code != 200:
                _open_snack(page, "Token incorreto ou expirado.", "#d84315")
                return

            _open_snack(page, "Token validado!", PRIMARY_COLOR)
            on_validated()
            
            return 

        except Exception:
            _open_snack(page, "Erro de conexão ou ao validar token.", "#d84315")

        finally:
            _enable(submit_button, True)

    threading.Thread(target=_request, daemon=True).start()

def handle_reset_password(
    page: ft.Page,
    user_id: int,
    password: str,
    submit_button: ft.Control,
):
    """
    Etapa 4 — Finaliza a recuperação alterando a senha.
    (Lógica mantida do seu código original)
    """

    _enable(submit_button, False)
    _open_snack(page, "Alterando senha...", PRIMARY_COLOR, 50)

    def _request():
        try:
            # --- SIMULAÇÃO DE REQUESTS INÍCIO ---
            # resp = requests.post(f"{API_BASE_URL}/auth/password/reset", json={"user_id": user_id, "password": password}, timeout=10)
            
            # SIMULAÇÃO (SUCESSO):
            resp_status_code = 200
            # FIM DA SIMULAÇÃO

            page.snack_bar.open = False
            page.update()

            if resp_status_code != 200:
                _open_snack(page, "Erro ao alterar senha. Tente novamente.", "#d84315")
                return

            _open_snack(page, "Senha alterada com sucesso! Redirecionando para o login.", PRIMARY_COLOR)
            page.go("/login")

        except Exception:
            _open_snack(page, "Erro de conexão inesperado.", "#d84315")

        finally:
            _enable(submit_button, True)

    threading.Thread(target=_request, daemon=True).start()