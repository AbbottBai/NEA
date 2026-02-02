import pygame as py
from game.player import player
from game.bg_render import bg_render

class game_screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg = bg_render(width, height, "Blue.png")

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

        self.bg_speed = 6

    def handle_screen(self, event):
        if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
            return "lobby_screen"
        return None

    def _shift_background_from_player_flags(self):
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

    def draw(self, window):
        self.bg.draw(window)
        self.p.draw_player(window)
        self._shift_background_from_player_flags()