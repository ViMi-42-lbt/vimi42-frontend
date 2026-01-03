import flet as ft

class GoogleAuthButton(ft.Container):
    def __init__(self, on_click=None, disabled=True):
        super().__init__()
        self.on_click = None 
        self.disabled = True
        self.opacity = 0.4
        
        self.width = 50
        self.height = 50
        self.border_radius = 24
        self.alignment = ft.alignment.center
        self.bgcolor = ft.Colors.WHITE
        self.tooltip = "Login com Google temporariamente indisponível"
        
        self.content = ft.Image(
            src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg",
            width=24,
            height=24,
        )

    def set_loading(self, loading: bool):
        """No-op para evitar quebras no controller se ainda houver referências"""
        pass