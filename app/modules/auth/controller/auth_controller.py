import re
from app.core.errors.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.core.navigation.routes import Routes
from app.modules.auth.domain.auth_validations import AuthValidations
from app.modules.auth.services.auth_service import AuthService
from app.core.errors.error_mapper import map_auth_error
from app.shared.components.dialogs import Dialogs


class AuthController:
    def __init__(self, page):
        self.page = page
        self.service = AuthService()

    # ─────────────────────────────
    # OAUTH GOOGLE
    # ─────────────────────────────



    # ─────────────────────────────
    # REGISTER
    # ─────────────────────────────

    def sanitize_data(self, data: dict) -> dict:
        keys_to_clean = ["cpf", "cnpj", "birth_date"]
        clean_data = data.copy()
        for key in keys_to_clean:
            if key in clean_data and isinstance(clean_data[key], str):
                clean_data[key] = re.sub(r'\D', '', clean_data[key])
        return clean_data

    def register(self, *, data: dict, submit_button, fields: dict) -> None:
        submit_button.set_loading(True)
        for field in fields.values():
            if hasattr(field, "clear_error"):
                field.clear_error()
        self.page.update()

        validation = AuthValidations.validate_register(data)
        if not validation.is_valid:
            submit_button.set_loading(False)
            target_field = fields.get(validation.field)
            if target_field and hasattr(target_field, "set_error"):
                target_field.set_error(validation.message)
                target_field.update()
            
            Dialogs.error(self.page, validation.message)
            return

        try:
            sanitized_payload = self.sanitize_data(data)
            
            self.service.register(payload=sanitized_payload)
            
            Dialogs.success(self.page, "Sua conta foi criada com sucesso.")
            self.page.go(Routes.LOGIN)

        except ConflictError:
            Dialogs.error(self.page, "Estes dados (E-mail, CPF ou CNPJ) já estão em uso por outra conta.\n",
                          "Por favor, verifique e tente novamente.")
        except Exception as exc:
            Dialogs.error(self.page, map_auth_error(exc))
        finally:
            submit_button.set_loading(False)

        # ─────────────────────────────
        # LOGIN
        # ─────────────────────────────
    def login(self, *, email, password, email_field, password_field, submit_button):
        email_field.clear_error()
        password_field.clear_error()

        validation = AuthValidations.validate_login(email, password)
        if not validation.is_valid:
            field = email_field if validation.field == "email" else password_field
            field.set_error(validation.message)
            Dialogs.error(self.page, validation.message)
            return

        submit_button.set_loading(True)
        try:
            self.service.login(email=email, password=password)
            self.page.go(Routes.HOME)
        except Exception as exc:
            Dialogs.error(self.page, map_auth_error(exc))
        finally:
            submit_button.set_loading(False)

    # ─────────────────────────────
    # FORGOT PASSWORD
    # ─────────────────────────────
    def forgot_password(self, *, email, email_field, submit_button):
        email_field.clear_error()

        validation = AuthValidations.validate_forgot_password(email)
        if not validation.is_valid:
            email_field.set_error(validation.message)
            Dialogs.error(self.page, validation.message)
            return

        submit_button.set_loading(True)
        try:
            response = self.service.request_password_reset(email=email)
            if not response or not response.get("success"):
                raise Exception("Resposta inválida do backend")
        except NotFoundError:
            Dialogs.error(self.page, "Email não cadastrado. Por favor, tente novamente.")
            return
        except Exception as exc:
            Dialogs.error(self.page, map_auth_error(exc))
            return
        finally:
            submit_button.set_loading(False)

        Dialogs.success(
            self.page,
            "Enviamos um token para redefinição de senha.\n"
            "Verifique sua caixa de entrada. Caso não encontre, confira também o Spam ou a Lixeira.",
        )
        self.page.go(Routes.RESET_PASSWORD_TOKEN)

    # ─────────────────────────────
    # VALIDATE RESET TOKEN
    # ─────────────────────────────
    def validate_reset_token(self, *, token, token_field, submit_button):
        token_field.clear_error()

        validation = AuthValidations.validate_reset_token(token)
        if not validation.is_valid:
            token_field.set_error(validation.message)
            Dialogs.error(self.page, validation.message)
            return

        attempts = self.page.client_storage.get("reset_token_attempts") or 0
        if attempts >= 3:
            Dialogs.error(
                self.page,
                "Você excedeu o número máximo de tentativas. Solicite um novo token."
            )
            self.page.client_storage.remove("reset_token_attempts")
            self.page.go(Routes.FORGOT_PASSWORD)
            return

        submit_button.set_loading(True)
        try:
            response = self.service.validate_reset_token(token=token)
            reset_session = response.get("reset_session")
            if not reset_session:
                raise Exception("Reset session não retornada pelo backend")

            self.page.client_storage.set("reset_session", reset_session)
            self.page.client_storage.remove("reset_token_attempts")
        except (UnprocessableEntityError, NotFoundError):
            attempts += 1
            self.page.client_storage.set("reset_token_attempts", attempts)
            token_field.set_error("Token inválido.")
            Dialogs.error(self.page, f"Token inválido. Tentativa {attempts}/3.")
            return
        except Exception as exc:
            Dialogs.error(self.page, map_auth_error(exc))
            return
        finally:
            submit_button.set_loading(False)

        self.page.go(Routes.RESET_PASSWORD_NEW)

    # ─────────────────────────────
    # SET NEW PASSWORD
    # ─────────────────────────────
    def set_new_password(
        self,
        *,
        password,
        confirm_password,
        password_field,
        confirm_password_field,
        submit_button,
    ):
        password_field.clear_error()
        confirm_password_field.clear_error()

        validation = AuthValidations.validate_new_password(password, confirm_password)
        if not validation.is_valid:
            field = password_field if validation.field == "password" else confirm_password_field
            field.set_error(validation.message)
            Dialogs.error(self.page, validation.message)
            return

        reset_session = self.page.client_storage.get("reset_session")
        if not reset_session:
            Dialogs.error(self.page, "Sessão expirada. Solicite um novo token.")
            self.page.go(Routes.FORGOT_PASSWORD)
            return

        submit_button.set_loading(True)
        try:
            self.service.reset_password(reset_session=reset_session, password=password)
            self.page.client_storage.remove("reset_session")
            self.page.client_storage.remove("reset_token_attempts")
            password_field.value = ""
            confirm_password_field.value = ""
        except Exception as exc:
            Dialogs.error(self.page, map_auth_error(exc))
            return
        finally:
            submit_button.set_loading(False)

        Dialogs.success(self.page, "Senha redefinida com sucesso.")
        self.page.go(Routes.LOGIN)