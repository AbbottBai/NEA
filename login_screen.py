import pygame as py
from animated_text import animated_text
from auth_ui import input_box, button
from main import event

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
        self.box_width = 750
        self.box_height = 200
        self.email_box = input_box(width//2, height//2, self.box_width, self.box_height, light_gray, "Enter your email")
        self.password_box = input_box(width//2, height//2+400, self.box_width, self.box_height, light_gray, "Enter your password")