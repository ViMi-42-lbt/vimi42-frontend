from dataclasses import dataclass
import re
from app.core.utils.validators import PASSWORD_MAX_LEN, PASSWORD_MIN_LEN, is_required, is_email


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    message: str | None = None
    field: str | None = None


class AuthValidations:
    @staticmethod
    def validate_register(data: dict) -> ValidationResult:
        if not is_email(data.get("email", "")):
            return ValidationResult(False, "E-mail inválido", "email")
        
        pw_res = AuthValidations.validate_password_strength(data.get("password", ""))
        if not pw_res.is_valid: return pw_res
        
        if data.get("password") != data.get("confirm_password"):
            return ValidationResult(False, "As senhas não coincidem", "confirm_password")

        if not data.get("display_name"):
            return ValidationResult(False, "Nome social é obrigatório", "display_name")
        
        if data.get("person_type") == "PF":
            if not data.get("full_name"):
                return ValidationResult(False, "Nome completo é obrigatório", "full_name")
            if not data.get("birth_date") or len(re.sub(r'\D', '', data.get("birth_date"))) < 8:
                return ValidationResult(False, "Data de nascimento obrigatória (DD/MM/AAAA)", "birth_date")
            if not AuthValidations.validate_cpf(data.get("cpf", "")):
                return ValidationResult(False, "CPF inválido", "cpf")
        else:
            if not data.get("corporate_name"):
                return ValidationResult(False, "Razão social é obrigatória", "corporate_name")
            if not AuthValidations.validate_cnpj(data.get("cnpj", "")):
                return ValidationResult(False, "CNPJ inválido", "cnpj")
        
        return ValidationResult(True)

    @staticmethod
    def validate_password_strength(password: str) -> ValidationResult:
        if not is_required(password):
            return ValidationResult(False, "Informe sua senha.", "password")
    
        if not AuthValidations.has_valid_length(password):
            return ValidationResult(
                False,
                f"A senha deve ter entre {PASSWORD_MIN_LEN} e {PASSWORD_MAX_LEN} caracteres.",
                "password",
            )
    
        if not AuthValidations.has_upper_and_lower(password):
            return ValidationResult(
                False,
                "A senha deve conter letras maiúsculas e minúsculas.",
                "password",
            )
    
        if not AuthValidations.has_number(password):
            return ValidationResult(
                False,
                "A senha deve conter pelo menos um número.",
                "password",
            )
    
        if not AuthValidations.has_symbol(password):
            return ValidationResult(
                False,
                "A senha deve conter pelo menos um símbolo.",
                "password",
            )
    
        return ValidationResult(True)

    @staticmethod
    def validate_login(email: str, password: str) -> ValidationResult:
        email = (email or "").strip()
        password = password or ""

        if not is_required(email):
            return ValidationResult(False, "Informe seu email.", "email")

        if not is_email(email):
            return ValidationResult(False, "Email inválido.", "email")

        return AuthValidations.validate_password_strength(password)
    
    @staticmethod
    def validate_forgot_password(email: str) -> ValidationResult:
        email = (email or "").strip()

        if not is_required(email):
            return ValidationResult(False, "Informe seu email.", "email")

        if not is_email(email):
            return ValidationResult(False, "Email inválido.", "email")

        return ValidationResult(True)

    @staticmethod
    def validate_reset_token(token: str) -> ValidationResult:
        token = (token or "").strip()
    
        if not is_required(token):
            return ValidationResult(False, "Informe o token.", "token")
    
        if len(token) < 4:
            return ValidationResult(False, "Token inválido.", "token")
    
        return ValidationResult(True)
    
    
    @staticmethod
    def validate_new_password(password: str, confirm_password: str) -> ValidationResult:
        result = AuthValidations.validate_password_strength(password)
        if not result.is_valid:
            return result

        if password != confirm_password:
            return ValidationResult(False, "As senhas não coincidem.", "confirm_password")

        return ValidationResult(True)
    
    @staticmethod
    def has_valid_length(password: str) -> bool:
        return PASSWORD_MIN_LEN <= len(password) <= PASSWORD_MAX_LEN

    @staticmethod
    def has_upper_and_lower(password: str) -> bool:
        return bool(re.search(r"[A-Z]", password)) and bool(re.search(r"[a-z]", password))

    @staticmethod
    def has_number(password: str) -> bool:
        return bool(re.search(r"\d", password))

    @staticmethod
    def has_symbol(password: str) -> bool:
        return bool(re.search(r"[^\w\s]", password))
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11: return False
        for i in range(9, 11):
            val = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
            val = ((val * 10) % 11) % 10
            if val != int(cpf[i]): return False
        return True

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14: return False
        
        def check_digit(s, weights):
            digit = sum(int(a) * b for a, b in zip(s, weights)) % 11
            return 0 if digit < 2 else 11 - digit

        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        if check_digit(cnpj[:12], w1) != int(cnpj[12]): return False
        if check_digit(cnpj[:13], w2) != int(cnpj[13]): return False
        return True