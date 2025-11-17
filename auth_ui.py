from animated_text import animated_text
import pygame as py

white = (255, 255, 255)
black = (0, 0, 0)
light_gray = (230, 230, 230)
dark_gray = (60, 60, 60)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 150, 255)

class input_box:
    def __init__(self, x, y, width, height, colour, text=''):
        self.rect = py.Rect(x, y, width, height)
        self.colour = colour
        self.text = text
        self.font = py.font.SysFont("Arial", 35, bold=False)
        self.text_surface = self.font.render(text, True, self.colour)
        self.active = False

    def handle_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            # Toggle active state
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.colour if self.active else light_gray
        elif event.type == py.KEYDOWN and self.active:
            if event.key == py.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == py.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text_surface = self.font.render(self.text, True, black)

    def draw(self, window):
        window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        py.draw.rect(window, self.color, self.rect, 2)

class button:
    def __init__(self, text, x, y, width, height, colour, speed):
        self.rect = py.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.speed = speed

        self.hover_color = light_blue
        self.font = py.font.SysFont("Arial", 35, bold=False)
        self.start_time = py.time.get_ticks()


    def draw(self, window):
        # Calculate elapsed time and fade alpha
        elapsed = (py.time.get_ticks() - self.start_time) / (1000 / self.speed)
        alpha = min(int(elapsed * 255), 255)

        # Create a transparent surface for the whole button
        button_surface = py.Surface((self.rect.width, self.rect.height), py.SRCALPHA)
        button_surface.set_alpha(alpha)

        # Determine button color (hover or normal)
        mouse_pos = py.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.colour

        # Draw button background on that surface
        py.draw.rect(button_surface, color, button_surface.get_rect(), border_radius=8)

        # Render text and blit onto the same surface
        text_surface = self.font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(text_surface, text_rect)

        # Finally, blit the entire faded button surface onto the main window
        window.blit(button_surface, self.rect.topleft)

    def is_clicked(self, event):
        return event.type == py.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)