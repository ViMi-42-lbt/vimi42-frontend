import flet as ft

# Cores principais
PRIMARY_COLOR = "#e5b701"
SECONDARY_COLOR = "#ca8603"
TERTIARY_COLOR = "#4a2e2a"
PRIMARY_BACKGROUND_COLOR = "#FBF9F6"
SECONDARY_BACKGROUND_COLOR = "#FFFFFF"
SOFT_BLACK_COLOR = "#333333"
GREY_COLOR = "#c0c0c0"
GOLDEN_COLOR = "#e5b701"

# Estilo de texto principal
title_style = ft.TextStyle(
    size=28,
    weight=ft.FontWeight.BOLD,
    color=TERTIARY_COLOR
)

# Estilo para links (Ex: "Crie uma aqui")
link_style = ft.TextStyle(
    size=14,
    weight=ft.FontWeight.BOLD,
    color=TERTIARY_COLOR
)

# Estilo para texto normal (Ex: "Não tem uma conta?")
regular_text_style = ft.TextStyle(
    size=14,
    color=GREY_COLOR
)