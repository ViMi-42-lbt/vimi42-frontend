class AppException(Exception):
    """Erro base da aplicação"""


class NetworkError(AppException):
    pass


class UnauthorizedError(AppException):
    pass


class AccessDeniedError(AppException):
    pass


class NotFoundError(AppException):
    pass


class UnprocessableEntityError(AppException):
    pass


class ServerError(AppException):
    pass


class ValidationError(AppException):
    pass


class ConflictError(AppException):
    pass


class UnknownError(AppException):
    pass