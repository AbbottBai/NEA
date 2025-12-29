import pygame as py
from animated_text import animated_text
from auth_ui import button
from login_screen import login_screen
from signup_screen import signup_screen

white = (255, 255, 255)
black = (0, 0, 0)
light_gray = (230, 230, 230)
dark_gray = (60, 60, 60)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 150, 255)


class screen_controller:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.lb_background = py.image.load("lb_background.jpg")
        self.lb_background = py.transform.scale(self.lb_background, (self.width, self.height))
        self.button_width = 300
        self.button_height = 150
        self.login_button = button("Login", self.width // 2 - self.button_width // 2, self.height // 2 - 150, self.button_width, self.button_height,
                              red, 0.5)
        self.signup_button = button("Sign up", self.width // 2 - self.button_width // 2, self.height // 2 + 100, self.button_width,
                               self.button_height, red, 0.5)
        self.title_text = animated_text("Welcome to comp-sci revision game", self.width//2, self.height//2-250, black, 40, 1.5)

    def handle_screen(self, event):
        if self.login_button.is_clicked(event):
            return login_screen(self.width, self.height)
        elif self.signup_button.is_clicked(event):
            return signup_screen(self.width, self.height)

    def draw(self, window):
        window.blit(self.lb_background, (0, 0))
        self.login_button.draw(window)
        self.signup_button.draw(window)
        self.title_text.typing(window)