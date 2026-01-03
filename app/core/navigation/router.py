import flet as ft
from typing import Dict, Callable
from app.core.layouts.app_shell import AppShell
from app.core.navigation.routes import Routes


class Router:
    def __init__(self, page: ft.Page, routes: Dict[str, Callable], shell: AppShell):
        self.page = page
        self.routes = routes
        self.shell = shell
        
        self.page.on_route_change = self._on_route_change

    def _on_route_change(self, e: ft.RouteChangeEvent) -> None:
        view_factory = self.routes.get(e.route) or self.routes.get(Routes.DEFAULT)
        content = view_factory(self.page)
        self.shell.set_content(content)
        
        for control in self.page.controls:
            if isinstance(control, AppShell):
                control.set_content(content)
                break
        
        self.page.update()

    def _notify_shells(self):
        for control in self.page.controls:
            if callable(getattr(control, "refresh", None)):
                control.refresh()
