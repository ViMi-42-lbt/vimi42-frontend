import flet as ft

from flet.auth.providers.google_oauth_provider import GoogleOAuthProvider
from app.shared.services.http_client import HttpClient


class AuthService:
    def __init__(self):
        self.http = HttpClient()

    # ─────────────────────────────
    # OAUTH GOOGLE
    # ─────────────────────────────

    

    # ─────────────────────────────
    # CADASTRO
    # ─────────────────────────────

    def register(self, *, payload: dict) -> None:
        self.http.post("/auth/register", json=payload)

    # ─────────────────────────────
    # LOGIN
    # ─────────────────────────────

    def login(self, *, email: str, password: str) -> None:
        self.http.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

    # ─────────────────────────────
    # FORGOT PASSWORD
    # ─────────────────────────────

    def request_password_reset(self, *, email: str) -> dict:
        return self.http.post(
            "/auth/forgot-password",
            json={"email": email},
        )

    # ─────────────────────────────
    # VALIDATE RESET TOKEN
    # ─────────────────────────────

    def validate_reset_token(self, *, token: str) -> dict:
        return self.http.post(
            "/auth/validate-reset-token",
            json={"token": token},
        )

    # ─────────────────────────────
    # RESET PASSWORD
    # ─────────────────────────────

    def reset_password(self, *, reset_session: str, password: str) -> None:
        self.http.post(
            "/auth/reset-password",
            json={
                "reset_session": reset_session,
                "new_password": password,
            },
        )