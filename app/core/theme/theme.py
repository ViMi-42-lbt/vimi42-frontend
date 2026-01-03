import flet as ft
from app.core.theme import colors


class AppTheme:

    @staticmethod
    def build_light_theme() -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                # BRAND / IDENTIDADE
                primary=colors.golden_primary,
                secondary=colors.golden_action,
                tertiary=colors.golden_soft,

                # SURFACES
                background=colors.background_primary,
                surface=colors.background_secondary,
                surface_variant=colors.background_elevated,

                # TEXT
                on_background=colors.text_primary,
                on_surface=colors.text_primary,
                on_surface_variant=colors.text_secondary,

                # STATES
                error=colors.error,
                outline=colors.text_tertiary,
            ),
            font_family="Inter",
        )

    @staticmethod
    def build_dark_theme() -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                # BRAND / IDENTIDADE
                primary=colors.golden_primary,
                secondary=colors.golden_action,
                tertiary=colors.golden_soft,

                # SURFACES
                background=colors.background_primary_dark,
                surface=colors.background_secondary_dark,
                surface_variant=colors.background_elevated_dark,

                # TEXT
                on_background=colors.text_primary_dark,
                on_surface=colors.text_primary_dark,
                on_surface_variant=colors.text_secondary_dark,

                # STATES
                error=colors.error,
                outline=colors.text_tertiary_dark,
            ),
            font_family="Inter",
        )