import flet as ft

import app.core.theme.colors as golden_soft

# =========================
# TITLES
# =========================

title_xl = ft.TextStyle(
    font_family="Inter",
    size=32,
    weight=ft.FontWeight.W_900,
    height=1.12,
)

title_lg = ft.TextStyle(
    font_family="Inter",
    size=24,
    weight=ft.FontWeight.W_700,
    height=1.18,
)

title_md = ft.TextStyle(
    font_family="Inter",
    size=20,
    weight=ft.FontWeight.W_500,
    height=1.25,
)

title_sm = ft.TextStyle(
    font_family="Inter",
    size=15,
    weight=ft.FontWeight.W_600,
    height=1.55,
)

# =========================
# BODY
# =========================

body_primary = ft.TextStyle(
    font_family="Inter",
    size=15,
    weight=ft.FontWeight.W_400,
    height=1.55,
)

body_secondary = ft.TextStyle(
    font_family="Inter",
    size=14,
    weight=ft.FontWeight.W_400,
    height=1.5,
)

body_secondary_thin = ft.TextStyle(
    font_family="Inter",
    size=14,
    weight=ft.FontWeight.W_200,
    height=1.5,
)

body_tertiary = ft.TextStyle(
    font_family="Inter",
    size=12,
    weight=ft.FontWeight.W_200,
    height=1.5,
    color=golden_soft,
)