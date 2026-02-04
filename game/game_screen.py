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
            # Shift zombies same as background
            """
            for z in self.zombie_list:
                z.x += dx
                z.y += dy"""

    def spawn_zombie(self):
        side = random.choice(["left", "right", "top", "bottom"])
        pad = 60  # How far off-screen they start

        if side == "left":
            x = -pad
            y = random.randint(0, self.height)
        elif side == "right":
            x = self.width + pad
            y = random.randint(0, self.height)
        elif side == "top":
            x = random.randint(0, self.width)
            y = -pad
        else:  # bottom
            x = random.randint(0, self.width)
            y = self.height + pad

        z = zombie(x, y, width=64, end=0, player_x=self.p.x, player_y=self.p.y)
        self.zombie_list.append(z)

    def handle_zombie(self):
        now = py.time.get_ticks()

        # Ramp difficulty up over time by reducing interval
        elapsed = now - self.start_time_ms
        ramps = elapsed // self.ramp_every_ms
        target_interval = max(self.min_interval_ms,
                              800 - ramps * self.ramp_step_ms)  # starts at 800ms
        self.spawn_interval_ms = target_interval

        # Spawn zombies when timer says so
        if now - self.last_spawn_ms >= self.spawn_interval_ms:
            self.last_spawn_ms = now
            self.spawn_zombie()

        # Update each zombie's target (player position)
        for z in self.zombie_list:
            z.set_target(self.p.x, self.p.y)

        # Remove dead/invisible zombies
        self.zombie_list = [z for z in self.zombie_list if z.visible]



    def draw(self, window):
        self.bg.draw(window)
        self.handle_zombie()
        self.p.draw_player(window)
        self.shift_background_from_player_flags()
        for z in self.zombie_list:
            z.draw(window)