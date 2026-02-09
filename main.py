import pygame as py
from screen_controller import screen_controller
from login_screen import login_screen
from signup_screen import signup_screen
from info_screen import info_screen
from lobby_screen import lobby_screen
from game.game_screen import game_screen

py.init()
clock = py.time.Clock()

width = 1200
height = 700
window_size = (width, height)
window = py.display.set_mode(window_size)
py.display.set_caption("Computer Science Revision Game")

run = True

screen_controller = screen_controller(width, height)
current_user_email = None

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
        elif next_screen_str == "play_screen":
            next_screen = game_screen(width, height, current_user_email)

        else:
            next_screen = screen_controller
            # I fixed the double input bug by getting rid of a .handle_screen

        # Carry user_email across screens
        if next_screen:
            # If current screen has an email, pass it forward
            if hasattr(screen_controller, "user_email") and screen_controller.user_email:
                next_screen.user_email = screen_controller.user_email

            # Update global email if next_screen is login/signup and just set it
            if hasattr(next_screen, "user_email") and next_screen.user_email:
                current_user_email = next_screen.user_email

        if next_screen:
            screen_controller = next_screen

        # Capture logged-in email from screens that have it (login/signup/info/lobby etc.)
        if hasattr(screen_controller, "user_email") and screen_controller.user_email:
            current_user_email = screen_controller.user_email

        if event.type == py.QUIT:
            run = False

    screen_controller.draw(window)
    clock.tick(30)
    py.display.update()

py.quit()