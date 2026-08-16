import flet as ft

from database import (
    get_all_users,
    delete_user,
    get_all_alerts,
    get_history,
)


class AdminPage:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

        self.message = ft.Text(
            "",
            size=14,
            color=ft.Colors.BLUE_900,
        )

        self.content_area = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

    # =====================================================
    # MANAGE USERS
    # =====================================================

    def manage_users(self, e):

        self.content_area.controls.clear()

        users = get_all_users()

        if not users:

            self.content_area.controls.append(
                ft.Text(
                    "No users found.",
                    size=16,
                )
            )

        else:

            for user in users:

                user_id = str(user["_id"])

                user_card = ft.Container(
                    width=360,
                    padding=15,
                    border_radius=12,
                    bgcolor=ft.Colors.BLUE_50,

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                user.get(
                                    "name",
                                    "Unknown"
                                ),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                f"Email: "
                                f"{user.get('email', '-')}"
                            ),

                            ft.Text(
                                f"Phone: "
                                f"{user.get('phone', '-')}"
                            ),

                            ft.Text(
                                f"Role: "
                                f"{user.get('role', '-')}"
                            ),

                            ft.Text(
                                f"ID: {user_id}",
                                size=11,
                                color=ft.Colors.GREY_700,
                            ),

                            ft.OutlinedButton(
                                "Delete User",
                                on_click=lambda e,
                                uid=user_id:
                                self.delete_user_clicked(uid),
                            ),
                        ]
                    ),
                )

                self.content_area.controls.append(
                    user_card
                )

        self.message.value = (
            f"{len(users)} user(s) found."
        )

        self.page.update()

    # =====================================================
    # DELETE USER
    # =====================================================

    def delete_user_clicked(self, user_id):

        try:

            # Prevent admin from deleting himself
            if str(self.user["_id"]) == user_id:

                self.message.value = (
                    "You cannot delete your own account."
                )

                self.message.color = ft.Colors.RED

                self.page.update()
                return

            deleted = delete_user(user_id)

            if deleted:

                self.message.value = (
                    "User deleted successfully."
                )

                self.message.color = ft.Colors.GREEN

            else:

                self.message.value = (
                    "User could not be deleted."
                )

                self.message.color = ft.Colors.RED

            self.manage_users(None)

        except Exception as error:

            self.message.value = (
                "Error deleting user."
            )

            self.message.color = ft.Colors.RED

            print(
                "Delete User Error:",
                error
            )

            self.page.update()

    # =====================================================
    # VIEW SOS ALERTS
    # =====================================================

    def view_alerts(self, e):

        self.content_area.controls.clear()

        alerts = get_all_alerts()

        if not alerts:

            self.content_area.controls.append(
                ft.Text(
                    "No SOS alerts found.",
                    size=16,
                )
            )

        else:

            for alert in alerts:

                status = alert.get(
                    "status",
                    "Unknown"
                )

                card = ft.Container(
                    width=360,
                    padding=15,
                    border_radius=12,
                    bgcolor=(
                        ft.Colors.RED_50
                        if status == "Pending"
                        else ft.Colors.GREEN_50
                    ),

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                "🚨 SOS Alert",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                f"Student: "
                                f"{alert.get('student_name', '-')}"
                            ),

                            ft.Text(
                                f"Latitude: "
                                f"{alert.get('latitude', '-')}"
                            ),

                            ft.Text(
                                f"Longitude: "
                                f"{alert.get('longitude', '-')}"
                            ),

                            ft.Text(
                                f"Status: {status}"
                            ),

                            ft.Text(
                                f"Created: "
                                f"{alert.get('created_at', '-')}"
                            ),
                        ]
                    ),
                )

                self.content_area.controls.append(
                    card
                )

        self.message.value = (
            f"{len(alerts)} SOS alert(s) found."
        )

        self.page.update()

    # =====================================================
    # EMERGENCY HISTORY
    # =====================================================

    def emergency_history(self, e):

        self.content_area.controls.clear()

        history = get_history()

        if not history:

            self.content_area.controls.append(
                ft.Text(
                    "No emergency history found.",
                    size=16,
                )
            )

        else:

            for item in history:

                card = ft.Container(
                    width=360,
                    padding=15,
                    border_radius=12,
                    bgcolor=ft.Colors.BLUE_50,

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                "📜 Emergency Record",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                f"Student: "
                                f"{item.get('student_name', '-')}"
                            ),

                            ft.Text(
                                f"Security: "
                                f"{item.get('security_name', '-')}"
                            ),

                            ft.Text(
                                f"Location: "
                                f"{item.get('latitude', '-')}, "
                                f"{item.get('longitude', '-')}"
                            ),

                            ft.Text(
                                f"Remarks: "
                                f"{item.get('remarks', '-')}"
                            ),

                            ft.Text(
                                f"Resolved: "
                                f"{item.get('resolved_at', '-')}"
                            ),
                        ]
                    ),
                )

                self.content_area.controls.append(
                    card
                )

        self.message.value = (
            f"{len(history)} history record(s) found."
        )

        self.page.update()

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    def system_status(self, e):

        self.content_area.controls.clear()

        try:

            users = get_all_users()
            alerts = get_all_alerts()
            history = get_history()

            pending = len([
                alert
                for alert in alerts
                if alert.get("status") == "Pending"
            ])

            resolved = len([
                alert
                for alert in alerts
                if alert.get("status") == "Resolved"
            ])

            self.content_area.controls.extend([

                ft.Container(
                    width=360,
                    padding=20,
                    border_radius=15,
                    bgcolor=ft.Colors.GREEN_50,

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                "🟢 System Status",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                "Database: Connected"
                            ),

                            ft.Text(
                                "Application: Running"
                            ),
                        ]
                    ),
                ),

                ft.Text(
                    f"👥 Total Users: {len(users)}",
                    size=16,
                ),

                ft.Text(
                    f"🚨 Total SOS Alerts: {len(alerts)}",
                    size=16,
                ),

                ft.Text(
                    f"⚠️ Pending Emergencies: {pending}",
                    size=16,
                ),

                ft.Text(
                    f"✅ Resolved Alerts: {resolved}",
                    size=16,
                ),

                ft.Text(
                    f"📜 History Records: {len(history)}",
                    size=16,
                ),
            ])

            self.message.value = (
                "System status loaded successfully."
            )

            self.message.color = ft.Colors.GREEN

        except Exception as error:

            self.content_area.controls.append(
                ft.Text(
                    "Database connection error.",
                    color=ft.Colors.RED,
                    size=16,
                )
            )

            self.message.value = (
                "Unable to load system status."
            )

            self.message.color = ft.Colors.RED

            print(
                "System Status Error:",
                error
            )

        self.page.update()

    # =====================================================
    # LOGOUT
    # =====================================================

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

    # =====================================================
    # UI
    # =====================================================

    def build(self):

        profile = ft.Container(
            width=360,
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

                            ft.Text(
                                self.user["email"]
                            ),

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

                    ft.Container(height=20),

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

                    ft.Container(height=15),

                    self.message,

                    ft.Container(height=10),

                    self.content_area,

                    ft.Container(height=20),

                    ft.OutlinedButton(
                        "Logout",
                        width=320,
                        on_click=self.logout,
                    ),
                ],
            ),
        )
