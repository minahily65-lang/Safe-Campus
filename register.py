import flet as ft
from database import register_user, get_user_by_email


class RegisterPage:

    def __init__(self, page: ft.Page, show_screen):
        self.page = page
        self.show_screen = show_screen

        self.name = ft.TextField(
            label="Full Name",
            width=320,
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
        )

        self.email = ft.TextField(
            label="Email",
            width=320,
            prefix_icon=ft.Icons.EMAIL,
            border_radius=10,
        )

        self.phone = ft.TextField(
            label="Phone Number",
            width=320,
            prefix_icon=ft.Icons.PHONE,
            border_radius=10,
        )

        self.password = ft.TextField(
            label="Password",
            width=320,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=10,
        )

        self.message = ft.Text(
            "",
            color=ft.Colors.RED,
            size=14,
        )

    # =====================================================
    # REGISTER
    # =====================================================

    def register_clicked(self, e):

        name = self.name.value.strip()
        email = self.email.value.strip().lower()
        phone = self.phone.value.strip()
        password = self.password.value.strip()

        # -------------------------
        # Validation
        # -------------------------

        if not name or not email or not phone or not password:

            self.message.value = (
                "Please fill all fields."
            )

            self.message.color = ft.Colors.RED

            self.page.update()

            return

        # -------------------------
        # Password length
        # -------------------------

        if len(password) < 6:

            self.message.value = (
                "Password must be at least 6 characters."
            )

            self.message.color = ft.Colors.RED

            self.page.update()

            return

        # -------------------------
        # Duplicate email
        # -------------------------

        if get_user_by_email(email):

            self.message.value = (
                "Email already exists."
            )

            self.message.color = ft.Colors.RED

            self.page.update()

            return

        # -------------------------
        # Public registration
        # -------------------------
        # Users can only register
        # as Student.

        success = register_user(
            name=name,
            email=email,
            phone=phone,
            password=password,
            role="Student",
        )

        if not success:

            self.message.value = (
                "Registration failed."
            )

            self.message.color = ft.Colors.RED

            self.page.update()

            return

        # -------------------------
        # Success
        # -------------------------

        self.message.value = (
            "Registration Successful! "
            "You can now login."
        )

        self.message.color = ft.Colors.GREEN

        # Clear fields

        self.name.value = ""
        self.email.value = ""
        self.phone.value = ""
        self.password.value = ""

        self.page.update()

    # =====================================================
    # BACK
    # =====================================================

    def back_clicked(self, e):

        from login import LoginPage

        login = LoginPage(
            self.page,
            self.show_screen
        )

        self.show_screen(
            login.build()
        )

    # =====================================================
    # UI
    # =====================================================

    def build(self):

        logo = ft.Image(
            src="assets/logo.png",
            width=110,
            height=110,
        )

        title = ft.Text(
            "Create Student Account",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
        )

        role_info = ft.Text(
            "New accounts are registered as Student.",
            size=13,
            color=ft.Colors.GREY_700,
        )

        register_btn = ft.ElevatedButton(
            "Register",
            width=320,
            height=45,
            on_click=self.register_clicked,
        )

        back_btn = ft.TextButton(
            "Back to Login",
            on_click=self.back_clicked,
        )

        card = ft.Container(
            width=360,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=25,

            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    logo,

                    title,

                    role_info,

                    ft.Container(height=15),

                    self.name,

                    self.email,

                    self.phone,

                    self.password,

                    ft.Container(height=10),

                    self.message,

                    ft.Container(height=10),

                    register_btn,

                    back_btn,
                ],
            ),
        )

        return ft.Container(
            expand=True,

            content=ft.Column(
                expand=True,

                alignment=ft.MainAxisAlignment.CENTER,

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[
                    card
                ],
            ),
        )
