import pygame as py

class info_screen:
    def __init__(self, width, height, on_confirm, on_cancel):
        self.width = width
        self.height = height
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        self.font = py.font.SysFont(None, 36)

        self.yes_btn = py.Rect(width//2 - 120, height//2 + 40, 100, 40)
        self.no_btn  = py.Rect(width//2 + 20,  height//2 + 40, 100, 40)

    def draw_button(self, window, rect, text):
        py.draw.rect(window, (220, 220, 220), rect)
        py.draw.rect(window, (0, 0, 0), rect, 2)
        txt = self.font.render(text, True, (0, 0, 0))
        window.blit(txt, txt.get_rect(center=rect.center))

    def handle_screen(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            if self.yes_btn.collidepoint(event.pos):
                return self.on_confirm()
            if self.no_btn.collidepoint(event.pos):
                return self.on_cancel()

    def draw(self, window):
        window.fill((240, 240, 240))

        msg = self.font.render("Are you sure?", True, (0, 0, 0))
        window.blit(msg, msg.get_rect(center=(self.width//2, self.height//2 - 40)))

        self.draw_button(window, self.yes_btn, "Yes")
        self.draw_button(window, self.no_btn, "No")