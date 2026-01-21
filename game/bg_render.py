import pygame as py
import os

class bg_render:
    def __init__(self, width, height, colour_name, floor_name):
        self.width = width
        self.height = height
        self.colour_name = colour_name
        self.floor_name = floor_name

    def create_background(self):
        image_path = os.path.join("background", self.colour_name)
        tile = py.image.load(image_path)
        _, _, tile_width, tile_height = tile.get_rect()
        tile_coords = []

        # Render all tiles that will appear on screen
        for i in range(self.height // tile_height):
            for j in range(self.width // tile_width):
                temp_coords = [j * tile_width, i * tile_height]
                tile_coords.append(temp_coords)

            # Renders 1 tile in x direction beyond game window
            l_coords = [0 - tile_width, i * tile_height]
            tile_coords.append(l_coords)
            r_coords = [self.width, i * tile_height]
            tile_coords.append(r_coords)

            # Renders 1 tile in y direction beyond game window
            u_coords = [i * tile_width, 0 - tile_height]
            tile_coords.append(u_coords)
            d_coords = [i * tile_width, self.height]
            tile_coords.append(d_coords)
