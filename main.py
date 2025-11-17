import pygame as py
from first_screen import first_screen

py.init()
clock = py.time.Clock()

width = 1200
height = 700
window_size = (width, height)
window = py.display.set_mode(window_size)
py.display.set_caption("Computer Science Revision Game")

run = True

current_screen = first_screen(width, height)

while run:

    for event in py.event.get():

        next_screen = current_screen.handle_screen()
        if next_screen:
            current_screen = next_screen

        current_screen.draw(window)

        if event.type == py.QUIT:
            run = False


    clock.tick(30)
    py.display.update()

py.quit()