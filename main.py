import flet as ft
from login import LoginPage


def main(page: ft.Page):
    # -----------------------------
    # Window Settings
    # -----------------------------
    page.title = "Safe Campus"
    page.window.width = 420
    page.window.height = 780
    page.window.resizable = False
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE

    # -----------------------------
    # Function to switch screens
    # -----------------------------
    def show_screen(screen):
        page.clean()
        page.add(screen)
        page.update()

    # -----------------------------
    # Open Login Screen
    # -----------------------------
    login = LoginPage(page, show_screen)
    show_screen(login.build())


# Run Application
ft.run(main)