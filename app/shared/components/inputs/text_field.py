import flet as ft
from app.core.theme.theme_resolver import ThemeResolver


class AppTextField(ft.TextField):
    def __init__(
        self,
        page: ft.Page | None = None,
        label: str = "",
        password: bool = False,
        color_scheme: ft.ColorScheme | None = None,
        **kwargs,
    ):
        self._is_password = password
        self._page = page

        self._scheme = (
            color_scheme
            if color_scheme
            else ThemeResolver.get_scheme(page) if page else None
        )

        super().__init__(
            label=label,
            password=password,
            border_radius=12,
            border_width=0.5,
            content_padding=ft.padding.symmetric(14, 16),
            **kwargs,
        )

        if self._scheme:
            self._apply_theme()

        if password:
            self.suffix_icon = ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF,
                icon_color=self._scheme.on_surface_variant,
                on_click=self._toggle_password,
            )

        if page is not None:
            if not hasattr(page, "_textfields"):
                page._textfields = []
            page._textfields.append(self)

    def _apply_theme(self):
        scheme = self._scheme

        self.border_color = scheme.outline + "88"
        self.focused_border_color = scheme.primary
        self.cursor_color = scheme.primary

        self.text_style = ft.TextStyle(color=scheme.on_surface_variant)
        self.label_style = ft.TextStyle(color=scheme.on_surface_variant)
        self.floating_label_style = ft.TextStyle(color=scheme.primary)
        self.hint_style = ft.TextStyle(color=scheme.on_surface_variant + "AA")

        self.prefix_icon_color = scheme.on_surface_variant
        self.suffix_icon_color = scheme.on_surface_variant
        self.error_style = ft.TextStyle(color=scheme.error)

    def _toggle_password(self, e: ft.ControlEvent):
        self._is_password = not self._is_password
        self.password = self._is_password
        self.suffix_icon.icon = (
            ft.Icons.VISIBILITY_OFF if self._is_password else ft.Icons.VISIBILITY
        )
        e.page.update()

    def set_error(self, message: str):
        self.error_text = message

    def clear_error(self):
        self.error_text = None

    def update_theme(self, scheme: ft.ColorScheme):
        self._scheme = scheme
        self._apply_theme()
        self.update()
