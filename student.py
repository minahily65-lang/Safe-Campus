import flet as ft
from gps import GPS
from playsound import playsound
import threading


class StudentPage:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

        # Text to display the student's location
        self.location_text = ft.Text(
            "Location not shared yet.",
            size=14,
            color=ft.Colors.BLUE_900,
        )

    # -----------------------------
    # SOS Button
    # -----------------------------
    from playsound import playsound
import threading


def play_siren():
    playsound("assets/siren.mp3")


def sos_clicked(self, e):
    threading.Thread(
        target=play_siren,
        daemon=True
    ).start()

    print("SOS Pressed")

    # -----------------------------
    # Share Location Button
    # -----------------------------
    def location_clicked(self, e):

        location = GPS.get_current_location()

        self.location_text.value = (
            f"Latitude: {location['latitude']}\n"
            f"Longitude: {location['longitude']}"
        )

        self.page.update()

    # -----------------------------
    # Emergency History Button
    # -----------------------------
    def history_clicked(self, e):
        print("Emergency History")

    # -----------------------------
    # Logout Button
    # -----------------------------
    def logout_clicked(self, e):

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

    # -----------------------------
    # UI
    # -----------------------------
    def build(self):

        title = ft.Text(
            "Student Dashboard",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
        )

        welcome = ft.Text(
            f"Welcome, {self.user['name']}",
            size=18,
            weight=ft.FontWeight.W_500,
        )

        profile = ft.Container(
            width=360,
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.BLUE_50,
            content=ft.Row(
                controls=[
                    ft.Image(
                        src="assets/student.png",
                        width=80,
                        height=80,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                self.user["name"],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(self.user["email"]),
                            ft.Text(self.user["role"]),
                        ]
                    ),
                ]
            ),
        )

        sos_button = ft.ElevatedButton(
            "🚨 SOS Emergency",
            width=320,
            height=55,
            bgcolor=ft.Colors.RED,
            color=ft.Colors.WHITE,
            on_click=self.sos_clicked,
        )

        location_button = ft.ElevatedButton(
            "📍 Share Location",
            width=320,
            height=50,
            on_click=self.location_clicked,
        )

        history_button = ft.ElevatedButton(
            "Emergency History",
            width=320,
            height=50,
            on_click=self.history_clicked,
        )

        logout_button = ft.OutlinedButton(
            "Logout",
            width=320,
            on_click=self.logout_clicked,
        )

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    title,
                    welcome,

                    ft.Divider(),

                    profile,

                    ft.Container(height=20),

                    sos_button,

                    ft.Container(height=10),

                    location_button,

                    ft.Container(height=10),

                    self.location_text,

                    ft.Container(height=10),

                    history_button,

                    ft.Container(height=20),

                    logout_button,
                ],
            ),
        )