import flet as ft

from .error_overlay import show_error
from .warning_overlay import show_warning
from .info_overlay import show_info
from .success_overlay import show_success


class Dialogs:
    @staticmethod
    def error(page: ft.Page, message: str) -> None:
        show_error(page, message)

    @staticmethod
    def warning(page: ft.Page, message: str) -> None:
        show_warning(page, message)

    @staticmethod
    def info(page: ft.Page, message: str) -> None:
        show_info(page, message)

    @staticmethod
    def success(page: ft.Page, message: str) -> None:
        show_success(page, message)