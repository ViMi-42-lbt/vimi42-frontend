import flet as ft
from app.core.theme.theme import AppTheme
from app.core.theme.theme_mode import ThemeMode
from app.core.state.app_state import AppState

class ThemeResolver:

    @staticmethod
    def apply(app_state: AppState, page: ft.Page) -> None:
        page.theme = AppTheme.build_light_theme()
        page.dark_theme = AppTheme.build_dark_theme()

        if app_state.theme_mode == ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.LIGHT
        elif app_state.theme_mode == ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.SYSTEM

        effective_scheme = ThemeResolver.get_scheme(page)

        for view in page.views:
            if hasattr(view, "on_theme_change") and callable(view.on_theme_change):
                view.on_theme_change(effective_scheme)

        page.update()

    @staticmethod
    def get_scheme(page: ft.Page) -> ft.ColorScheme:
        if page.theme_mode == ft.ThemeMode.DARK or (
            page.theme_mode == ft.ThemeMode.SYSTEM
            and page.platform_brightness == ft.Brightness.DARK
        ):
            return page.dark_theme.color_scheme
        return page.theme.color_scheme
