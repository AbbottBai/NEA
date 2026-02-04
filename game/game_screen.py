import pygame as py
from game.player import player
from game.bg_render import bg_render
from game.zombie import zombie
import random


class game_screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg = bg_render(width, height, "Blue.png")
        self.cam_x = 0 #Added in camera view variables
        self.cam_y = 0

        # Zombie spawning variables
        self.start_time_ms = py.time.get_ticks()
        self.last_spawn_ms = 0
        self.spawn_interval_ms = 800    # start ~1.25 zombies/sec
        self.min_interval_ms = 250      # cap at 4 zombies/sec
        self.ramp_every_ms = 4000       # every 4s, speed up spawns
        self.ramp_step_ms = 60          # subtract 60ms each ramp

        # Player setup
        p_w, p_h = 64, 64
        start_x = width // 2 - p_w // 2
        start_y = height // 2 - p_h // 2

        margin_x = width // 3
        margin_y = height // 3

        self.p = player(
            start_x, start_y, p_w, p_h,
            h_velocity=6, v_velocity=6,
            l_boundary=margin_x, r_boundary=width - margin_x,
            u_boundary=margin_y, d_boundary=height - margin_y
        )

        self.zombie_list = []

        self.bg_speed = 6

    def handle_screen(self, event):
        if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
            return "lobby_screen"
        return None

    def shift_background_from_player_flags(self):
        dx = 0
        dy = 0

        if self.p.left_background_shift:
            dx += self.bg_speed
        if self.p.right_background_shift:
            dx -= self.bg_speed
        if self.p.bg_upshift:
            dy -= self.bg_speed
        if self.p.bg_downshift:
            dy += self.bg_speed

        if dx or dy:
            self.bg.shift(dx, dy)

            # Shifts camera with background
            self.cam_x -= dx
            self.cam_y -= dy

    def spawn_zombie(self):
        side = random.choice(["left", "right", "top", "bottom"])
        pad = 60  # How far off-screen they start

        if side == "left":
            sx, sy = -pad, random.randint(0, self.height)
        elif side == "right":
            sx, sy = self.width + pad, random.randint(0, self.height)
        elif side == "top":
            sx, sy = random.randint(0, self.width), -pad
        else:
            sx, sy = random.randint(0, self.width), self.height + pad

        # Convert screen spawn position into world position
        wx = sx - self.cam_x
        wy = sy - self.cam_y

        z = zombie(wx, wy, width=64, end=0, player_x=0, player_y=0)
        self.zombie_list.append(z)

    def handle_zombie(self):
        now = py.time.get_ticks()

        elapsed = now - self.start_time_ms
        ramps = elapsed // self.ramp_every_ms
        self.spawn_interval_ms = max(self.min_interval_ms, 800 - ramps * self.ramp_step_ms)

        if now - self.last_spawn_ms >= self.spawn_interval_ms:
            self.last_spawn_ms = now
            self.spawn_zombie()

        # Player world coords
        player_wx = self.p.x - self.cam_x
        player_wy = self.p.y - self.cam_y

        # Zombies chase the world position
        for z in self.zombie_list:
            z.set_target(player_wx, player_wy)

        self.zombie_list = [z for z in self.zombie_list if z.visible]



    def draw(self, window):
        self.bg.draw(window)
        self.p.draw_player(window)
        self.shift_background_from_player_flags()
        self.handle_zombie()
        for z in self.zombie_list:
            z.draw(window, self.cam_x, self.cam_y)