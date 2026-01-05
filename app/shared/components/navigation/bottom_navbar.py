import flet as ft
from app.core.navigation.routes import Routes
from app.core.theme.theme_resolver import ThemeResolver

class NavButton(ft.Container):
    def __init__(self, icon: str, active_icon: str, label: str, route: str, page: ft.Page):
        super().__init__(
            expand=True,
            height=64,
            on_click=lambda _: page.go(route),
            bgcolor=ft.Colors.TRANSPARENT,
            ink=False,
            padding=ft.padding.symmetric(vertical=4, horizontal=4),
        )
        self.page = page
        self.route = route
        self.active_icon = active_icon
        self.inactive_icon = icon
        
        self.indicator = ft.Container(
            width=56,
            height=32,
            border_radius=16,
            bgcolor=ft.Colors.TRANSPARENT,
            content=ft.Icon(
                name=icon, 
                size=24,
                animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE)
            ),
            animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
        )
        
        self.text_control = ft.Text(
            value=label,
            size=12,
            weight=ft.FontWeight.W_200,
            animate_opacity=300,
        )
        
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
            controls=[
                self.indicator,
                self.text_control
            ]
        )

    def update_style(self, current_route: str, scheme: ft.ColorScheme):
        is_active = current_route == self.route
        
        active_color = scheme.primary
        inactive_color = scheme.outline
        indicator_bg = scheme.secondary_container if is_active else ft.Colors.TRANSPARENT
        
        self.indicator.bgcolor = indicator_bg
        self.indicator.content.name = self.active_icon if is_active else self.inactive_icon
        self.indicator.content.color = scheme.on_secondary_container if is_active else inactive_color
        self.indicator.content.scale = 1.1 if is_active else 1.0
        
        self.text_control.color = active_color if is_active else inactive_color
        self.text_control.weight = ft.FontWeight.W_200 if is_active else ft.FontWeight.W_200
        self.text_control.opacity = 1.0 if is_active else 0.8
        
        self.update()

class CustomBottomNavbar(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        scheme = ThemeResolver.get_scheme(page)
        
        self.buttons = [
            NavButton(ft.Icons.HOME_OUTLINED, ft.Icons.HOME_ROUNDED, "Início", Routes.HOME, page),
            NavButton(ft.Icons.HOME_OUTLINED, ft.Icons.HOME_ROUNDED, "Agendamentos", Routes.LOGIN, page),
            NavButton(ft.Icons.HOME_OUTLINED, ft.Icons.HOME_ROUNDED, "Mensagens", Routes.LOGIN, page),
            NavButton(ft.Icons.HOME_OUTLINED, ft.Icons.HOME_ROUNDED, "Perfil", Routes.LOGIN, page),
        ]

        super().__init__(
            content=ft.Row(
                controls=self.buttons,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=0,
            ),
            bgcolor=scheme.surface,
            height=85,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                offset=ft.Offset(0, -2)
            ),
            padding=ft.padding.only(bottom=15, left=10, right=10),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(600, ft.AnimationCurve.DECELERATE),
        )

    def update_state(self):
        scheme = ThemeResolver.get_scheme(self.page)
        self.bgcolor = scheme.surface
            
        for btn in self.buttons:
            btn.update_style(self.page.route, scheme)
        self.update()