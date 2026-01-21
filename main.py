import pygame as py
from screen_controller import screen_controller
from login_screen import login_screen
from signup_screen import signup_screen
from info_screen import info_screen
from lobby_screen import lobby_screen

py.init()
clock = py.time.Clock()

width = 1200
height = 700
window_size = (width, height)
window = py.display.set_mode(window_size)
py.display.set_caption("Computer Science Revision Game")

run = True

screen_controller = screen_controller(width, height)

while run:

    for event in py.event.get():

        next_screen_str = screen_controller.handle_screen(event)

        if next_screen_str == "login_screen":
            next_screen = login_screen(width, height)
        elif next_screen_str == "signup_screen":
            next_screen = signup_screen(width, height)
        elif next_screen_str == "info_screen":
            next_screen = info_screen(width, height)
        elif next_screen_str == "lobby_screen":
            next_screen = lobby_screen(width, height)
        else:
            next_screen = screen_controller
            # I fixed the double input bug by getting rid of a .handle_screen


        if next_screen:
            screen_controller = next_screen

        if event.type == py.QUIT:
            run = False

    screen_controller.draw(window)
    clock.tick(30)
    py.display.update()

py.quit()