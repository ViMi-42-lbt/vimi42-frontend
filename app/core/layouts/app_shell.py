import flet as ft
from app.shared.components.navigation.bottom_navbar import CustomBottomNavbar

class AppShell(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        
        self.scroll_area = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.navbar = CustomBottomNavbar(page)
        self.navbar.visible = False

        self.scroll_container = ft.Container(
            content=self.scroll_area,
            expand=True,
            alignment=ft.alignment.top_center
        )

        self.content = ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.scroll_container,
                self.navbar
            ]
        )

    def set_content(self, control: ft.Control, show_nav: bool = False, centered: bool = False):
        self.scroll_area.controls.clear()
        self.scroll_area.controls.append(control)
        
        if centered:
            self.scroll_area.alignment = ft.MainAxisAlignment.CENTER
            self.scroll_container.alignment = ft.alignment.center
        else:
            self.scroll_area.alignment = ft.MainAxisAlignment.START
            self.scroll_container.alignment = ft.alignment.top_center
        
        try:
            self.scroll_area.scroll_to(offset=0, duration=100)
        except Exception:
            pass
            
        self.navbar.visible = show_nav
        if show_nav:
            self.navbar.update_state()

        self.update()
        
    def refresh(self) -> None:
        if not self.page or not self.page.views:
            return

        self.scroll_area.controls.clear()
        current_view = self.page.views[-1]
        for control in current_view.controls:
            self.scroll_area.controls.append(control)

        self.update()

    def fade_out(self):
        self.opacity = 0.0
        self.update()

    def fade_in(self):
        self.opacity = 1.0
        self.update()