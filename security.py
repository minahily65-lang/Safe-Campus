import flet as ft
from database import (
    get_all_alerts,
    get_active_alerts,
    update_alert_status,
    save_history,
)


class SecurityPage:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

        self.message = ft.Text(
            "",
            size=14,
            color=ft.Colors.BLUE_900,
        )

        self.alert_list = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

    # =====================================================
    # VIEW ALL SOS ALERTS
    # =====================================================

    def view_alerts(self, e):

        self.alert_list.controls.clear()

        alerts = get_all_alerts()

        if not alerts:

            self.alert_list.controls.append(
                ft.Text(
                    "No SOS alerts found.",
                    size=16,
                )
            )

        else:

            for alert in alerts:

                alert_id = str(alert["_id"])

                alert_card = ft.Container(
                    width=360,
                    padding=15,
                    border_radius=12,
                    bgcolor=ft.Colors.RED_50,

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                "🚨 SOS ALERT",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED_900,
                            ),

                            ft.Text(
                                f"Student: "
                                f"{alert.get('student_name', 'Unknown')}"
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
                                f"Status: "
                                f"{alert.get('status', 'Unknown')}"
                            ),

                            ft.Text(
                                f"Created: "
                                f"{alert.get('created_at', '-')}"
                            ),

                            ft.Row(
                                controls=[

                                    ft.ElevatedButton(
                                        "Resolve",
                                        on_click=lambda e,
                                        aid=alert_id:
                                        self.resolve_alert(
                                            aid
                                        ),
                                    ),

                                    ft.OutlinedButton(
                                        "Delete",
                                        on_click=lambda e,
                                        aid=alert_id:
                                        self.delete_alert(
                                            aid
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    ),
                )

                self.alert_list.controls.append(
                    alert_card
                )

        self.message.value = (
            f"{len(alerts)} SOS alert(s) found."
        )

        self.page.update()

    # =====================================================
    # ACTIVE EMERGENCIES
    # =====================================================

    def active_emergencies(self, e):

        self.alert_list.controls.clear()

        alerts = get_active_alerts()

        if not alerts:

            self.alert_list.controls.append(
                ft.Text(
                    "No active emergencies.",
                    size=16,
                )
            )

        else:

            for alert in alerts:

                alert_id = str(alert["_id"])

                card = ft.Container(
                    width=360,
                    padding=15,
                    border_radius=12,
                    bgcolor=ft.Colors.ORANGE_50,

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                "⚠️ ACTIVE EMERGENCY",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                f"Student: "
                                f"{alert.get('student_name', 'Unknown')}"
                            ),

                            ft.Text(
                                f"Location: "
                                f"{alert.get('latitude', '-')}, "
                                f"{alert.get('longitude', '-')}"
                            ),

                            ft.Text(
                                f"Status: "
                                f"{alert.get('status', 'Unknown')}"
                            ),

                            ft.ElevatedButton(
                                "Resolve Emergency",
                                on_click=lambda e,
                                aid=alert_id:
                                self.resolve_alert(aid),
                            ),
                        ]
                    ),
                )

                self.alert_list.controls.append(card)

        self.message.value = (
            f"{len(alerts)} active emergency(s)."
        )

        self.page.update()

    # =====================================================
    # RESOLVE ALERT
    # =====================================================

    def resolve_alert(self, alert_id):

        try:

            # Find the alert
            alerts = get_all_alerts()

            alert = None

            for item in alerts:

                if str(item["_id"]) == alert_id:
                    alert = item
                    break

            if alert is None:

                self.message.value = (
                    "Alert not found."
                )

                self.page.update()
                return

            # Update status
            update_alert_status(
                alert_id,
                "Resolved"
            )

            # Save emergency history
            save_history(
                alert_id=alert_id,
                student_name=alert.get(
                    "student_name",
                    "Unknown"
                ),
                security_name=self.user["name"],
                latitude=alert.get(
                    "latitude",
                    0
                ),
                longitude=alert.get(
                    "longitude",
                    0
                ),
                remarks="Emergency resolved by security."
            )

            self.message.value = (
                "Emergency resolved successfully."
            )

            self.message.color = ft.Colors.GREEN

            # Refresh alerts
            self.alert_list.controls.clear()

            self.page.update()

        except Exception as error:

            self.message.value = (
                "Unable to resolve emergency."
            )

            self.message.color = ft.Colors.RED

            print(
                "Resolve Alert Error:",
                error
            )

        self.page.update()

    # =====================================================
    # DELETE ALERT
    # =====================================================

    def delete_alert(self, alert_id):

        try:

            from database import delete_alert

            delete_alert(alert_id)

            self.message.value = (
                "Alert deleted successfully."
            )

            self.message.color = ft.Colors.GREEN

            self.alert_list.controls.clear()

            self.page.update()

        except Exception as error:

            self.message.value = (
                "Unable to delete alert."
            )

            self.message.color = ft.Colors.RED

            print(
                "Delete Alert Error:",
                error
            )

            self.page.update()

    # =====================================================
    # EMERGENCY HISTORY
    # =====================================================

    def emergency_history(self, e):

        from database import get_history

        self.alert_list.controls.clear()

        history = get_history()

        if not history:

            self.alert_list.controls.append(
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
                                f"{item.get('student_name', 'Unknown')}"
                            ),

                            ft.Text(
                                f"Security: "
                                f"{item.get('security_name', 'Unknown')}"
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

                self.alert_list.controls.append(card)

        self.message.value = (
            f"{len(history)} history record(s) found."
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

                    ft.Container(height=10),

                    ft.Image(
                        src="assets/security.png",
                        width=100,
                        height=100,
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

                    ft.Container(height=10),

                    self.message,

                    ft.Container(height=10),

                    self.alert_list,

                    ft.Container(height=20),

                    ft.OutlinedButton(
                        "Logout",
                        width=320,
                        on_click=self.logout,
                    ),
                ]
            )
        )
