import pygame as py
from auth_ui import input_box, button
from authentication import authentication

white = (255, 255, 255)
black = (0, 0, 0)
light_gray = (230, 230, 230)
dark_gray = (60, 60, 60)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 150, 255)

class signup_screen:
    def __init__(self, width, height):
        self.lb_background = py.image.load("lb_background.jpg")
        self.lb_background = py.transform.scale(self.lb_background, (width, height))
        self.box_width = 600
        self.box_height = 100
        self.button_width = 300
        self.button_height = 150

        self.email_box = input_box(width//2 - 300, height//2 - 325, self.box_width, self.box_height, light_gray, "Enter your email")

        self.password_box = input_box(width//2-300, height//2-200, self.box_width, self.box_height, light_gray, "Enter your password")
        self.password_box.security = 1

        self.password_box2 = input_box(width//2-300, height//2-75, self.box_width, self.box_height, light_gray, "Enter your password again")
        self.password_box2.security = 1

        self.submit_button = button("Sign up", width // 2 - self.button_width // 2, height // 2 + 100, self.button_width,
                               self.button_height, red, 0.5)

        self.error = False
        self.error_message = ""
        font = py.font.SysFont("Arial", 30)
        self.error_surface = font.render(self.error_message, True, red)
        self.signup_status = False
        self.user_email = None

    def handle_screen(self, event):
        self.email_box.handle_event(event)
        self.password_box.handle_event(event)
        self.password_box2.handle_event(event)

        if self.submit_button.is_clicked(event):
            auth = authentication(self.email_box.text, self.password_box.text)

            # 1) Email format check
            self.error, self.error_message = auth.email_check()
            if self.error:
                font = py.font.SysFont("Arial", 30)
                self.error_surface = font.render(self.error_message, True, red)
                return

            # 2) Email duplicate check
            if auth.email_exists():
                self.error = True
                self.error_message = "Email already exists"
                font = py.font.SysFont("Arial", 30)
                self.error_surface = font.render(self.error_message, True, red)
                return

            # 3) Password checks
            self.error, self.error_message = auth.password_check(self.password_box2.text)
            if self.error:
                font = py.font.SysFont("Arial", 30)
                self.error_surface = font.render(self.error_message, True, red)
                return

            # 4) Create account
            self.error, self.error_message = auth.sign_up()
            if self.error:
                font = py.font.SysFont("Arial", 30)
                self.error_surface = font.render(self.error_message, True, red)
                return

            self.signup_status = True
            self.user_email = self.email_box.text
            return "info_screen"

    def draw(self, window):
        window.blit(self.lb_background, (0, 0))
        self.email_box.draw(window)
        self.password_box.draw(window)
        self.password_box2.draw(window)
        self.submit_button.draw(window)
        window.blit(self.error_surface, (300, 400))