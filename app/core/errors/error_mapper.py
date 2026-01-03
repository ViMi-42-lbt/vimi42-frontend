from app.core.errors.exceptions import (
    NetworkError,
    UnauthorizedError,
    AccessDeniedError,
    NotFoundError,
    UnprocessableEntityError,
    ServerError,
    ValidationError,
    ConflictError,
)

def map_auth_error(exc: Exception) -> str:
    if isinstance(exc, UnauthorizedError):
        return "Email ou senha inválidos."

    if isinstance(exc, ConflictError):
        return "Estes dados (E-mail, CPF ou CNPJ) já estão em uso por outra conta."

    if isinstance(exc, AccessDeniedError):
        return "Você não tem permissão para acessar esta área."

    if isinstance(exc, NotFoundError):
        return "Não encontramos o recurso solicitado."

    if isinstance(exc, UnprocessableEntityError):
        return "Os dados enviados são inválidos. Verifique e tente novamente."

    if isinstance(exc, NetworkError):
        return "Erro de conexão. Verifique sua internet."

    if isinstance(exc, ServerError):
        return "O sistema está temporariamente indisponível."

    if isinstance(exc, ValidationError):
        return str(exc)

    return (
        "Ocorreu um erro inesperado, mas já estamos trabalhando nisso. "
        "Tente novamente mais tarde."
    )