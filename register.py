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

        self.role = ft.Dropdown(
            width=320,
            label="Select Role",
            options=[
                ft.dropdown.Option("Student"),
                ft.dropdown.Option("Security"),
                ft.dropdown.Option("Admin"),
            ],
        )

        self.message = ft.Text(
            "",
            color=ft.Colors.RED,
            size=14,
        )

    # ------------------------
    # Register Button
    # ------------------------
    def register_clicked(self, e):

        name = self.name.value.strip()
        email = self.email.value.strip()
        phone = self.phone.value.strip()
        password = self.password.value.strip()
        role = self.role.value

        # Validation
        if not name or not email or not phone or not password or not role:
            self.message.value = "Please fill all fields."
            self.message.color = ft.Colors.RED
            self.page.update()
            return

        # Check duplicate email
        if get_user_by_email(email):
            self.message.value = "Email already exists."
            self.message.color = ft.Colors.RED
            self.page.update()
            return

        # Save user
        register_user(
            name=name,
            email=email,
            phone=phone,
            password=password,
            role=role,
        )

        self.message.value = "Registration Successful!"
        self.message.color = ft.Colors.GREEN

        # Clear fields
        self.name.value = ""
        self.email.value = ""
        self.phone.value = ""
        self.password.value = ""
        self.role.value = None

        self.page.update()

    # ------------------------
    # Back Button
    # ------------------------
    def back_clicked(self, e):
        from login import LoginPage

        login = LoginPage(self.page, self.show_screen)
        self.show_screen(login.build())

    # ------------------------
    # UI
    # ------------------------
    def build(self):

        logo = ft.Image(
            src="assets/logo.png",
            width=110,
            height=110,
        )

        title = ft.Text(
            "Create Account",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
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
                    ft.Container(height=15),
                    self.name,
                    self.email,
                    self.phone,
                    self.password,
                    self.role,
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
        controls=[card],
    ),
)