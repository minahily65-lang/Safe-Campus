import flet as ft


class SecurityPage:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

    def view_alerts(self, e):
        print("View Alerts")

    def active_emergencies(self, e):
        print("Active Emergencies")

    def emergency_history(self, e):
        print("Emergency History")

    def logout(self, e):
        from login import LoginPage

        login = LoginPage(
            self.page,
            lambda screen: (
                self.page.clean(),
                self.page.add(screen),
                self.page.update()
            )
        )

        self.page.clean()
        self.page.add(login.build())
        self.page.update()

    def build(self):

        return ft.Container(
            expand=True,
            padding=20,

            content=ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Text(
                        "Security Dashboard",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),

                    ft.Container(height=15),

                    ft.Image(
                        src="assets/security.png",
                        width=120,
                        height=120,
                    ),

                    ft.Text(
                        f"Welcome {self.user['name']}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        self.user["email"],
                        size=15,
                    ),

                    ft.Divider(),

                    ft.ElevatedButton(
                        "🚨 View SOS Alerts",
                        width=320,
                        height=55,
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE,
                        on_click=self.view_alerts,
                    ),

                    ft.Container(height=10),

                    ft.ElevatedButton(
                        "📍 Active Emergencies",
                        width=320,
                        height=50,
                        on_click=self.active_emergencies,
                    ),

                    ft.Container(height=10),

                    ft.ElevatedButton(
                        "📜 Emergency History",
                        width=320,
                        height=50,
                        on_click=self.emergency_history,
                    ),

                    ft.Container(height=20),

                    ft.OutlinedButton(
                        "Logout",
                        width=320,
                        on_click=self.logout,
                    ),

                ]

            )
        )