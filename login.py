import flet as ft
from database import login_user


class LoginPage:

    def __init__(self, page: ft.Page, show_screen):
        self.page = page
        self.show_screen = show_screen

        # Email Field
        self.email = ft.TextField(
            label="Email",
            hint_text="Enter your email",
            width=320,
            border_radius=10,
            prefix_icon=ft.Icons.EMAIL,
        )

        # Password Field
        self.password = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            width=320,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK,
        )

        # Message
        self.message = ft.Text(
            "",
            size=14,
            color=ft.Colors.RED,
        )

    # -------------------------
    # LOGIN BUTTON
    # -------------------------
    def login_clicked(self, e):

        email = self.email.value.strip()
        password = self.password.value.strip()

        if email == "" or password == "":
            self.message.value = "Please fill all fields."
            self.message.color = ft.Colors.RED
            self.page.update()
            return

        user = login_user(email, password)

        if user is None:
            self.message.value = "Invalid email or password."
            self.message.color = ft.Colors.RED
            self.page.update()
            return

        self.message.value = "Login Successful!"
        self.message.color = ft.Colors.GREEN
        self.page.update()

        role = user["role"]

        if role == "Student":
            from student import StudentPage
            self.show_screen(StudentPage(self.page, user).build())

        elif role == "Security":
            from security import SecurityPage
            self.show_screen(SecurityPage(self.page, user).build())

        elif role == "Admin":
            from admin import AdminPage
            self.show_screen(AdminPage(self.page, user).build())

    # -------------------------
    # REGISTER BUTTON
    # -------------------------
    def register_clicked(self, e):

        from register import RegisterPage

        register = RegisterPage(
            self.page,
            self.show_screen
        )

        self.show_screen(register.build())

    # -------------------------
    # UI
    # -------------------------
    def build(self):

        logo = ft.Image(
            src="assets/logo.png",
            width=120,
            height=120,
        )

        title = ft.Text(
            "SAFE CAMPUS",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
        )

        subtitle = ft.Text(
            "Campus Security Management System",
            size=15,
            color=ft.Colors.GREY_700,
        )

        login_button = ft.ElevatedButton(
            "Login",
            width=320,
            height=45,
            on_click=self.login_clicked,
        )

        register_button = ft.TextButton(
            "Create New Account",
            on_click=self.register_clicked,
        )

        card = ft.Container(
            width=360,
            padding=25,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo,
                    title,
                    subtitle,

                    ft.Container(height=20),

                    self.email,
                    self.password,

                    ft.Container(height=10),

                    self.message,

                    ft.Container(height=10),

                    login_button,

                    register_button,
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