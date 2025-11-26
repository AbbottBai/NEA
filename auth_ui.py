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
    def __init__(self, x, y, width, height, colour, placeholder=""):
        self.rect = py.Rect(x, y, width, height)
        self.base_colour = colour
        self.active_colour = dark_gray
        self.colour = self.base_colour

        self.placeholder = placeholder
        self.text = ""

        self.font = py.font.SysFont("Arial", 35)
        self.active = False

        self.security = 0
        self.stars = ""

    def handle_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.colour = self.active_colour if self.active else self.base_colour

        elif event.type == py.KEYDOWN and self.active:
            if event.key == py.K_RETURN:
                pass
            elif event.key == py.K_BACKSPACE:
                self.text = self.text[:-1]
                self.stars = self.stars[:-1]
            else:
                # event.unicode ensures only real characters (not shift, ctrl, etc...)
                if event.unicode != "":
                    self.text += event.unicode

                    # security = 1 → hide real text with stars
                    if self.security == 1:
                        self.stars += "*"

    def draw(self, window):
        # Draw placeholder if empty and not typing
        if self.text == "" and not self.active:
            text_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        else:
            if self.security == 0:
                text_surface = self.font.render(self.text, True, black)
            else:
                text_surface = self.font.render(self.stars, True, black)

        window.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        # Draw border
        py.draw.rect(window, self.colour, self.rect, 3)

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