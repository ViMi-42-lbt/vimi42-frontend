import flet as ft
from app.app import create_app

def main(page: ft.Page):
    create_app(page)

if __name__ == "__main__":
    ft.app(
        target=main,
        port=8550,
        view=ft.AppView.WEB_BROWSER
    )