import pygame as py
from lobby_screen import lobby_screen

class info_screen:
    def __init__(self, width, height, on_confirm, on_cancel):
        self.width = width
        self.height = height
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        self.lb_background = py.image.load("lb_background.jpg")
        self.lb_background = py.transform.scale(self.lb_background, (width, height))
        self.font = py.font.SysFont(None, 36)
        self.button_font = py.font.SysFont(None, 32)

        # Continue button (bottom-right)
        self.continue_btn = py.Rect(width - 180, height - 80, 140, 45)

        # Multiline text
        self.text = (
            "Welcome to GCSE computer science laser tag.\n"
            "This is a next generation revision tool which will\n"
            "help you consolidate existing knowledge and\n"
            "learn new materials.\n\n"
            "This game aims to provide a fun and intuitive\n"
            "learning experience.\n"
            "I hope you enjoy!"
        )

    def draw_button(self, window):
        red = (180, 0, 0)
        dark_red = (120, 0, 0)

        # This creates a boarder for the continue button
        py.draw.rect(window, red, self.continue_btn, border_radius=6)
        py.draw.rect(window, dark_red, self.continue_btn, 2, border_radius=6)

        txt = self.button_font.render("Continue", True, (255, 255, 255))
        window.blit(txt, txt.get_rect(center=self.continue_btn.center))


    def handle_screen(self, event):
        # Detect when the continue button is clicked.
        if event.type == py.MOUSEBUTTONDOWN:
            if self.continue_btn.collidepoint(event.pos):
                return lobby_screen(self.width, self.height)

    def draw(self, window):
        # Draw background instead of just filling screen with white
        window.blit(self.lb_background, (0, 0))

        # Draw multiline text
        lines = self.text.split("\n")
        y = self.height // 2 - 120

        # Renders multiline text
        for line in lines:
            rendered = self.font.render(line, True, (0,0,0))
            rect = rendered.get_rect(center=(self.width // 2, y))
            window.blit(rendered, rect)
            y += 36

        # Draw button
        self.draw_button(window)