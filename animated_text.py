import pygame as py

class animated_text():
    def __init__(self, text, x, y, color, font_size, speed):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.speed = speed
        self.font = py.font.SysFont("Arial", 60, bold=True)
        self.start_time = py.time.get_ticks()
        self.fin_typing = False
        self.animate = True

    def fade(self, window):
        # Gets the time elapsed since start of animation
        elapsed = (py.time.get_ticks() - self.start_time) / (1000 / self.speed)

        # Fade in by increasing alpha value gradually towards 255
        alpha = min(int(elapsed * 255), 255)
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)
        window.blit(text_surface, text_surface.get_rect(center = (self.x, self.y)))

    def typing(self, window):
        elapsed = (py.time.get_ticks() - self.start_time) / (1000 / self.speed)

        # Reveal characters one by one based on elapsed time
        letters_to_show = int(elapsed * 10)
        visible_text = self.text[:letters_to_show]
        if letters_to_show >= len(self.text):
            self.fin_typing = True

        text_surface = self.font.render(visible_text, True, self.color)
        window.blit(text_surface, text_surface.get_rect(center = (self.x, self.y)))