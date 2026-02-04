import pygame as py
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent # .../game
SPRITES = HERE.parent / "zombie_sprite" # .../zombie_sprite

class zombie:
    right_images = [
        py.image.load(str(SPRITES / f"{i}E.png"))
        for i in range(1, 12)
    ]
    left_images = [py.transform.flip(img, True, False) for img in right_images]

    def __init__(self, x, y, width, end, player_x, player_y):
        self.x = x
        self.y = y
        self.width = width
        self.walk_count = 0
        self.velocity = 5
        self.end = end
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 10
        self.visible = True
        self.player_x = player_x
        self.player_y = player_y

    def set_target(self, px, py):
        self.player_x = px
        self.player_y = py

    def chase(self):
        dx = self.player_x - self.x
        dy = self.player_y - self.y

        dist = math.hypot(dx, dy)  # sqrt(dx^2 + dy^2)
        if dist == 0:
            return

        # normalize direction
        nx = dx / dist
        ny = dy / dist

        speed = 3
        self.x += nx * speed
        self.y += ny * speed

        # set velocity sign for animation direction
        self.velocity = speed if nx >= 0 else -speed

    def draw(self, window):
        if self.visible:
            self.chase()
            if self.walk_count >= 33:
                self.walk_count = 0

            if self.velocity > 0:
                window.blit(self.right_images[self.walk_count //3], (self.x, self.y))
                self.walk_count += 1
            else:
                window.blit(self.left_images[self.walk_count //3], (self.x, self.y))
                self.walk_count += 1

            py.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            py.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 20, self.y, 28, 60)
            #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

        else:
            pass


    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")