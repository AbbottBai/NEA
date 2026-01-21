import pygame as py
import os

def load_sprite(sprite_width, sprite_height, sheet_name, sprite_amount):
    right_sprites = []
    image_path = os.path.join("sprites", sheet_name)
    sprite_sheet = py.image.load(image_path).convert_alpha()
    # For functions are required because there are multiple sprites per image
    # This is because of animations
    for i in range(sprite_amount):
        sprite = sprite_sheet.subsurface((i * sprite_width), 0, sprite_width, sprite_height)
        right_sprites.append(sprite)

    return right_sprites

def sprites():
    r_run = load_sprite(32, 32, "run.png", 12)
    r_idle = load_sprite(32, 32, "idle.png", 11)

    l_run = []
    for i in range(len(r_run)):
        l_image = py.transform.flip(r_run[i], True, False)
        # This flips the image so for example "left run" can be reused to render "right run"
        l_run.append(l_image)

    l_idle = []
    for i in range(len(r_idle)):
        idle = py.transform.flip(r_idle[i], True, False)
        l_idle.append(idle)