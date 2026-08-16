import flet as ft
from gps import GPS
from database import create_sos, get_history
from playsound import playsound
import threading


class StudentPage:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

        self.location_text = ft.Text(
            "Location not shared yet.",
            size=14,
            color=ft.Colors.BLUE_900,
        )

        self.message = ft.Text(
            "",
            size=14,
            color=ft.Colors.RED,
        )

    # =====================================================
    # SIREN
    # =====================================================

    def play_siren(self):
        try:
            playsound("assets/siren.mp3")
        except Exception as error:
            print("Siren Error:", error)

    # =====================================================
    # SOS BUTTON
    # =====================================================

    def sos_clicked(self, e):

        try:
            # Get current GPS location
            location = GPS.get_current_location()

            # Save SOS alert in MongoDB
            alert_id = create_sos(
                student_id=self.user["_id"],
                student_name=self.user["name"],
                latitude=location["latitude"],
                longitude=location["longitude"],
            )

            # Play emergency siren
            threading.Thread(
                target=self.play_siren,
                daemon=True
            ).start()

            self.message.value = (
                "🚨 SOS Alert Sent Successfully!"
            )

            self.message.color = ft.Colors.GREEN

            self.location_text.value = (
                f"Latitude: {location['latitude']}\n"
                f"Longitude: {location['longitude']}"
            )

            print("SOS Alert Created:", alert_id)

        except Exception as error:

            self.message.value = (
                "Unable to send SOS alert."
            )

            self.message.color = ft.Colors.RED

            print("SOS Error:", error)

        self.page.update()

    # =====================================================
    # SHARE LOCATION
    # =====================================================

    def location_clicked(self, e):

        try:

            location = GPS.get_current_location()

            self.location_text.value = (
                f"Latitude: {location['latitude']}\n"
                f"Longitude: {location['longitude']}\n"
                f"Time: {location['timestamp']}"
            )

            self.message.value = "Location shared successfully."
            self.message.color = ft.Colors.GREEN

        except Exception as error:

            self.message.value = "Unable to get location."
            self.message.color = ft.Colors.RED

            print("GPS Error:", error)

        self.page.update()

    # =====================================================
    # EMERGENCY HISTORY
    # =====================================================

    def history_clicked(self, e):

        history = get_history()

        if not history:

            self.message.value = "No emergency history found."
            self.message.color = ft.Colors.BLUE_900
            self.page.update()

            return

        history_text = "Emergency History\n\n"

        for item in history:

            history_text += (
                f"Student: {item.get('student_name', 'Unknown')}\n"
                f"Security: {item.get('security_name', 'Unknown')}\n"
                f"Location: "
                f"{item.get('latitude', '-')}, "
                f"{item.get('longitude', '-')}\n"
                f"Remarks: {item.get('remarks', '-')}\n"
                f"Resolved: {item.get('resolved_at', '-')}\n"
                f"-------------------------\n"
            )

        self.location_text.value = history_text

        self.page.update()

    # =====================================================
    # LOGOUT
    # =====================================================

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

    # =====================================================
    # UI
    # =====================================================

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

                            ft.Text(
                                self.user["email"]
                            ),

                            ft.Text(
                                self.user["role"]
                            ),
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
            "📜 Emergency History",
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

                    self.message,

                    ft.Container(height=10),

                    history_button,

                    ft.Container(height=20),

                    logout_button,
                ],
            ),
        )
