import pygame as py

class projectile:
    def __init__(self, x, y, radius, colour, vx, vy):
        self.x = float(x)      # WORLD x
        self.y = float(y)      # WORLD y
        self.radius = radius
        self.colour = colour
        self.vx = float(vx)
        self.vy = float(vy)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, window, cam_x, cam_y):
        sx = int(self.x + cam_x)
        sy = int(self.y + cam_y)
        py.draw.circle(window, self.colour, (sx, sy), self.radius)

    def screen_pos(self, cam_x, cam_y):
        return self.x + cam_x, self.y + cam_y