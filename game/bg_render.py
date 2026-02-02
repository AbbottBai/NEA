import pygame as py
from pathlib import Path

class bg_render:
    def __init__(self, width, height, colour_name):
        self.width = width
        self.height = height
        self.colour_name = colour_name

        ROOT = Path(__file__).resolve().parent.parent  # project root (since this file is in /game)
        image_path = ROOT / "background" / colour_name

        self.tile = py.image.load(str(image_path)).convert()
        self.tile_w = self.tile.get_width()
        self.tile_h = self.tile.get_height()

        # how many tiles to cover screen + 2 extra (one off each side)
        self.cols = width // self.tile_w + 3
        self.rows = height // self.tile_h + 3

        # scrolling offsets (wrap with modulo)
        self.off_x = 0
        self.off_y = 0

    def shift(self, dx, dy):
        self.off_x = (self.off_x + dx) % self.tile_w
        self.off_y = (self.off_y + dy) % self.tile_h

    def draw(self, window):
        # start one tile up/left so always cover edges
        start_x = -self.tile_w - self.off_x
        start_y = -self.tile_h - self.off_y

        for row in range(self.rows):
            y = start_y + row * self.tile_h
            for col in range(self.cols):
                x = start_x + col * self.tile_w
                window.blit(self.tile, (x, y))
