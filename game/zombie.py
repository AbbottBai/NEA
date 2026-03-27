import pygame as py
import math # math is a library used for mathematical calculations
from pathlib import Path # pathlib is a library which manages files and project directories.

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
        # Uses the user's current coordinates as the target for the zombie to move towards

    def chase(self):
        dx = self.player_x - self.x
        dy = self.player_y - self.y
        # Calculates the distance to the user

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

    def draw(self, window, cam_x, cam_y):
        if not self.visible:
            return

        self.chase()

        if self.walk_count >= 33:
            self.walk_count = 0
            # Resets animation when the last frame has been displayed

        sx = self.x + cam_x
        sy = self.y + cam_y

        if self.velocity > 0:
            window.blit(self.right_images[self.walk_count // 3], (sx, sy))
        else:
            window.blit(self.left_images[self.walk_count // 3], (sx, sy))
        self.walk_count += 1

        # Hitbox should be in screen coords for drawing
        self.hitbox = (sx + 20, sy, 28, 60)

        py.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        py.draw.rect(window, (0, 128, 0),
                     (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 4
            # Subtracts 4 from the health of zombies when they are hit by the user

        if self.health <= 0:
            self.visible = False
            # Removes the zombie from view if their health is negative
            return True  # died this hit

        return False  # still alive

    def world_hitbox(self):
        return py.Rect(self.x + 20, self.y, 28, 60)