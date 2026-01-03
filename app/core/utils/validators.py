import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 20


PASSWORD_REGEX = re.compile(
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$"
)


def is_required(value: str | None) -> bool:
    return bool(value and value.strip())


def is_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value))

class InputFormatters:
    @staticmethod
    def format_input(e):
        """Lógica centralizada de máscaras dinâmicas para componentes Flet."""
        v = re.sub(r'\D', '', e.control.value)
        label = e.control.label
        formatted = ""

        if label == "CPF":
            v = v[:11]
            if len(v) <= 3: formatted = v
            elif len(v) <= 6: formatted = f"{v[:3]}.{v[3:]}"
            elif len(v) <= 9: formatted = f"{v[:3]}.{v[3:6]}.{v[6:]}"
            else: formatted = f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}"

        elif label == "CNPJ":
            v = v[:14]
            if len(v) <= 2: formatted = v
            elif len(v) <= 5: formatted = f"{v[:2]}.{v[2:]}"
            elif len(v) <= 8: formatted = f"{v[:2]}.{v[2:5]}.{v[5:]}"
            elif len(v) <= 12: formatted = f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:]}"
            else: formatted = f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"

        elif label == "Data de nascimento":
            v = v[:8]
            if len(v) <= 2: formatted = v
            elif len(v) <= 4: formatted = f"{v[:2]}/{v[2:]}"
            else: formatted = f"{v[:2]}/{v[2:4]}/{v[4:]}"
        
        else:
            formatted = e.control.value

        e.control.value = formatted
        e.control.update()