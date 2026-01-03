import flet as ft


class AppShell(ft.Container):
    def __init__(self, page: ft.Page):
        
        super().__init__(expand=True)
        self.page = page
        self.scroll_area = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.alignment = ft.alignment.center 
        self.content = self.scroll_area

    def set_content(self, control: ft.Control):
        self.scroll_area.controls.clear()
        self.scroll_area.controls.append(control)
        self.scroll_area.scroll_to(offset=0, duration=100)
        self.update()
        
    def refresh(self) -> None:
        if not self.page or not self.page.views:
            return

        self.content_area.controls.clear()
        current_view = self.page.views[-1]
        for control in current_view.controls:
            self.content_area.controls.append(control)

        self.update()

    def fade_out(self):
        self.opacity = 0.0
        self.update()

    def fade_in(self):
        self.opacity = 1.0
        self.update()
