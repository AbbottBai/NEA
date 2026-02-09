import pygame as py
from game.settings_db import set_background, get_background

class settings_screen:
    def __init__(self, width, height, user_email):
        self.width = width
        self.height = height
        self.user_email = user_email

        self.bg = py.image.load("lb_background.jpg")
        self.bg = py.transform.scale(self.bg, (width, height))

        self.font_title = py.font.SysFont("arial", 50, bold=True)
        self.font_btn = py.font.SysFont("arial", 28, bold=True)

        self.options = [
            "Blue.png", "Brown.png", "Grass.png", "Gray.png",
            "Green.png", "Pink.png", "Purple.png", "Yellow.png"
        ]

        self.selected = get_background(user_email)

        # Back button
        self.back_rect = py.Rect(40, 40, 140, 50)

        # Option buttons
        self.buttons = []
        start_y = 150
        btn_w, btn_h = 260, 60
        gap = 18
        cols = 2
        start_x = width // 2 - (cols * btn_w + (cols - 1) * 40) // 2

        for idx, opt in enumerate(self.options):
            r = idx // cols
            c = idx % cols
            x = start_x + c * (btn_w + 40)
            y = start_y + r * (btn_h + gap)
            self.buttons.append((opt, py.Rect(x, y, btn_w, btn_h)))

    def handle_screen(self, event):
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # back
            if self.back_rect.collidepoint(mx, my):
                return "lobby_screen"

            # options
            for opt, rect in self.buttons:
                if rect.collidepoint(mx, my):
                    self.selected = opt
                    set_background(self.user_email, opt)

        if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
            return "lobby_screen"

        return None

    def draw(self, window):
        window.blit(self.bg, (0, 0))

        title = self.font_title.render("Settings", True, (0, 0, 0))
        window.blit(title, (self.width // 2 - title.get_width() // 2, 60))

        # back button
        py.draw.rect(window, (180, 0, 0), self.back_rect, border_radius=10)
        back_txt = self.font_btn.render("Back", True, (255, 255, 255))
        window.blit(back_txt, back_txt.get_rect(center=self.back_rect.center))

        # option buttons
        for opt, rect in self.buttons:
            is_selected = (opt == self.selected)
            color = (80, 180, 90) if is_selected else (200, 200, 200)
            py.draw.rect(window, color, rect, border_radius=12)
            py.draw.rect(window, (40, 40, 40), rect, 2, border_radius=12)

            label = opt.replace(".png", "")
            txt = self.font_btn.render(label, True, (0, 0, 0))
            window.blit(txt, txt.get_rect(center=rect.center))