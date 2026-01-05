import flet as ft


class PrimaryButton(ft.Container):
    def __init__(
        self,
        text: str,
        on_click: callable,
    ):
        self._on_click = on_click
        self._loading = False

        self.label = ft.Text(
            text,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.WHITE,
        )

        super().__init__(
            alignment=ft.alignment.center,
            width=400,
            height=48,
            border_radius=12,
            bgcolor=ft.Colors.PRIMARY,
            on_click=self._handle_click,
            animate_opacity=120,
            content=self.label,
        )

    def _handle_click(self, e):
        if not self._loading:
            self._on_click(e)

    def set_loading(self, value: bool):
        self._loading = value
        self.content = (
            ft.ProgressRing(width=22, height=22, stroke_width=2)
            if value
            else self.label
        )
        self.opacity = 0.7 if value else 1
        self.update()
