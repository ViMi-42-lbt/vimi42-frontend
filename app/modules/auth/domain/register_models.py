from dataclasses import dataclass
from typing import Optional, Literal

PersonType = Literal["PF", "PJ"]

@dataclass
class RegisterPF:
    email: str
    display_name: str # Nome social
    full_name: str
    cpf: str
    birth_date: Optional[str] = None # Obrigatório via Validador no cadastro manual
    person_type: str = "PF"
    password: Optional[str] = None

@dataclass
class RegisterPJ:
    email: str
    display_name: str
    corporate_name: str
    cnpj: str
    is_mei: bool = False
    person_type: str = "PJ"
    password: Optional[str] = None