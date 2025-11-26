import pygame as py
from animated_text import animated_text
from auth_ui import input_box, button

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

        self.email_box = input_box(width//2 - 300, height//2 - 300, self.box_width, self.box_height, light_gray, "Enter your email")
        self.password_box = input_box(width//2-300, height//2-100, self.box_width, self.box_height, light_gray, "Enter your password")
        self.password_box.security = 1
        self.submit_button = button("Login", width // 2 - self.button_width // 2, height // 2 + 100, self.button_width,
                               self.button_height, red, 0.5)

    def handle_screen(self, event):
        self.email_box.handle_event(event)
        self.password_box.handle_event(event)
        if self.submit_button.is_clicked(event):
            pass
        elif self.submit_button.is_clicked(event):
            pass

    def draw(self, window):
        window.blit(self.lb_background, (0, 0))
        self.email_box.draw(window)
        self.password_box.draw(window)
        self.submit_button.draw(window)