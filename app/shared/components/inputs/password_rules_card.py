import flet as ft

from app.modules.auth.domain.auth_validations import AuthValidations
from app.core.utils.validators import PASSWORD_MIN_LEN, PASSWORD_MAX_LEN
from app.core.theme import spacing
from app.core.theme.typography import body_secondary, body_primary
from app.core.theme.theme_resolver import ThemeResolver


class PasswordRulesCard(ft.Container):
    def __init__(
        self,
        *,
        page: ft.Page | None = None,
        color_scheme: ft.ColorScheme | None = None,
        password: str = "",
    ):
        if color_scheme is None and page is not None:
            self._scheme = ThemeResolver.get_scheme(page)
        else:
            self._scheme = color_scheme

        self._password = password or ""

        super().__init__(
            padding=spacing.md,
            border_radius=16,
            bgcolor=self._scheme.surface_variant,
        )

        self._build()

    def _build(self):
        pwd = self._password
        self.bgcolor = self._scheme.surface_variant

        self.content = ft.Column(
            spacing=spacing.sm,
            controls=[
                ft.Text(
                    "Sua senha deve conter:",
                    style=body_primary,
                    color=self._scheme.on_surface,
                ),
                self._rule_row(
                    f"Entre {PASSWORD_MIN_LEN} e {PASSWORD_MAX_LEN} caracteres",
                    AuthValidations.has_valid_length(pwd),
                ),
                self._rule_row("Letra maiúscula", any(c.isupper() for c in pwd)),
                self._rule_row("Letra minúscula", any(c.islower() for c in pwd)),
                self._rule_row("Pelo menos um número", AuthValidations.has_number(pwd)),
                self._rule_row("Pelo menos um caractere especial\n""(exemplo: @ ! $ & #)", AuthValidations.has_symbol(pwd)),
            ],
        )

    def _rule_row(self, label: str, valid: bool) -> ft.Row:
        return ft.Row(
            spacing=spacing.sm,
            controls=[
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if valid else ft.Icons.CANCEL,
                    size=18,
                    color=self._scheme.secondary if valid else self._scheme.outline,
                ),
                ft.Text(label, style=body_secondary, color=self._scheme.on_surface_variant),
            ],
        )

    def update_password(self, password: str):
        self._password = password or ""
        self._build()
        self.update()

    def update_color_scheme(self, scheme: ft.ColorScheme):
        self._scheme = scheme
        self.bgcolor = scheme.surface_variant
        self._build()
        self.update()
