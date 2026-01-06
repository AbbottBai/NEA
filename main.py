import pygame as py
from screen_controller import screen_controller

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

        next_screen = screen_controller.handle_screen(event)
        if next_screen:
            screen_controller = next_screen

        if event.type == py.QUIT:
            run = False

    screen_controller.draw(window)
    clock.tick(30)
    py.display.update()

py.quit()