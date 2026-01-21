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

class login_screen:
    def __init__(self, width, height):
        self.lb_background = py.image.load("lb_background.jpg")
        self.lb_background = py.transform.scale(self.lb_background, (width, height))
        self.box_width = 600
        self.box_height = 100
        self.button_width = 300
        self.button_height = 150
        self.width = width
        self.height = height

        self.email_box = input_box(self.width//2 - 300, self.height//2 - 300, self.box_width, self.box_height, light_gray, "Enter your email")
        self.password_box = input_box(self.width//2-300, self.height//2-100, self.box_width, self.box_height, light_gray, "Enter your password")
        self.password_box.security = 1
        self.submit_button = button("Login", width // 2 - self.button_width // 2, height // 2 + 100, self.button_width,
                               self.button_height, red, 0.5)

        self.font = py.font.SysFont("arial", 36)
        self.message = ""
        self.login_state = False

    def handle_screen(self, event):
        self.email_box.handle_event(event)
        self.password_box.handle_event(event)

        if self.submit_button.is_clicked(event):
            auth = authentication(self.email_box.text, self.password_box.text)
            self.login_state, self.message = auth.login_func()

            if self.login_state:
                return "info_screen"
            print(self.message)

    def draw(self, window):
        window.blit(self.lb_background, (0, 0))
        self.email_box.draw(window)
        self.password_box.draw(window)
        self.submit_button.draw(window)

        # Added in error message on screen, instead of just printing in console.
        if self.message:
            msg_surface = self.font.render(self.message, True, red)
            msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height // 2 + 55)) # +55 is the perfect position to be above the login button
            window.blit(msg_surface, msg_rect)