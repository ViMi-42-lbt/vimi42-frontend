import flet as ft


class StorageService:
    def __init__(self, page: ft.Page):
        self._storage = page.client_storage

    def set_token(self, token: str) -> None:
        self._storage.set("auth_token", token)

    def get_token(self) -> str | None:
        return self._storage.get("auth_token")

    def clear(self) -> None:
        self._storage.remove("auth_token")