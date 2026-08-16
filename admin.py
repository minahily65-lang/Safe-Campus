import flet as ft


class AdminPage:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

    # --------------------------
    # Button Functions
    # --------------------------

    def manage_users(self, e):
        print("Manage Users")

    def view_alerts(self, e):
        print("View SOS Alerts")

    def emergency_history(self, e):
        print("Emergency History")

    def system_status(self, e):
        print("System Status")

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

    # --------------------------
    # UI
    # --------------------------

    def build(self):

        profile = ft.Container(
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=15,
            content=ft.Row(
                controls=[
                    ft.Image(
                        src="assets/admin.png",
                        width=80,
                        height=80,
                    ),

                    ft.Column(
                        controls=[
                            ft.Text(
                                self.user["name"],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(self.user["email"]),

                            ft.Text(
                                "Administrator",
                                color=ft.Colors.BLUE_900,
                            ),
                        ]
                    ),
                ]
            ),
        )

        return ft.Container(

            expand=True,
            padding=20,

            content=ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Text(
                        "Admin Dashboard",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),

                    ft.Container(height=15),

                    profile,

                    ft.Container(height=25),

                    ft.ElevatedButton(
                        "👥 Manage Users",
                        width=320,
                        height=50,
                        on_click=self.manage_users,
                    ),

                    ft.Container(height=10),

                    ft.ElevatedButton(
                        "🚨 View SOS Alerts",
                        width=320,
                        height=50,
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE,
                        on_click=self.view_alerts,
                    ),

                    ft.Container(height=10),

                    ft.ElevatedButton(
                        "📜 Emergency History",
                        width=320,
                        height=50,
                        on_click=self.emergency_history,
                    ),

                    ft.Container(height=10),

                    ft.ElevatedButton(
                        "🖥 System Status",
                        width=320,
                        height=50,
                        on_click=self.system_status,
                    ),

                    ft.Container(height=25),

                    ft.OutlinedButton(
                        "Logout",
                        width=320,
                        on_click=self.logout,
                    ),
                ],
            ),
        )