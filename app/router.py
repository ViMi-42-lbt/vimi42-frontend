import flet as ft
from app.Modules.Identidade.routes import get_identidade_routes


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {view.route: view for view in get_identidade_routes(page)}

    def route_change(self, e: ft.RouteChangeEvent):
        """Chamado sempre que page.go() é invocado."""
        route = e.route
        view = self.routes.get(route)

        if view:
            # Empilha a view atual
            self.page.views.clear()
            self.page.views.append(view)
        else:
            # Fallback caso a rota não exista
            self.page.views.clear()
            self.page.views.append(self.routes["/login"])

        self.page.update()

    def view_pop(self, e: ft.ViewPopEvent):
        """Chamado ao clicar no botão de voltar."""
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        else:
            self.page.go("/login")