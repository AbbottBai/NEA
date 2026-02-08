from game.sprite_render import sprites
import pygame as py

r_run, r_idle, l_run, l_idle = sprites()

class player:
    def __init__(self, x, y, width, height, h_velocity, v_velocity, l_boundary, r_boundary, u_boundary, d_boundary):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.h_velocity = h_velocity
        self.v_velocity = v_velocity
        self.l_boundary = l_boundary
        self.r_boundary = r_boundary
        self.u_boundary = u_boundary
        self.d_boundary = d_boundary

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.moving = False
        self.run_count = 0
        self.idle_count = 0
        self.left_background_shift = False
        self.right_background_shift = False
        self.bg_upshift = False
        self.bg_downshift = False
        self.h_movement_counter = 0
        self.v_movement_counter = 0

        # Health / hit system
        self.hp = 100
        self.alive = True
        self.invuln_frames = 0 # Countdown (frames)
        self.invuln_duration = 30 # About 1s at 30fps
        self.damage_on_hit = 10

        self.hitbox_offset_x = 18
        self.hitbox_offset_y = 8
        self.hitbox_w = 28
        self.hitbox_h = 48

    def tick(self):
        # Call once per frame
        if self.invuln_frames > 0:
            self.invuln_frames -= 1

    def world_hitbox(self, cam_x, cam_y) -> py.Rect:
        """
        Return player's hitbox in WORLD coords.
        Player screen pos = (self.x, self.y)
        World pos = screen - cam
        """
        wx = (self.x - cam_x) + self.hitbox_offset_x
        wy = (self.y - cam_y) + self.hitbox_offset_y
        return py.Rect(int(wx), int(wy), self.hitbox_w, self.hitbox_h)

    def can_take_hit(self) -> bool:
        return self.invuln_frames == 0 and self.hp > 0

    def take_hit(self, dmg: int):
        if not self.can_take_hit():
            return
        self.hp = max(0, self.hp - dmg)
        self.invuln_frames = self.invuln_duration
        if self.hp == 0:
            self.alive = False

    def move_player(self):
        key = py.key.get_pressed()
        self.left_background_shift = False
        self.right_background_shift = False
        if key[py.K_a]:
            self.left_background_shift = False
            self.left = True
            self.right = False
            self.moving = True
            self.h_movement_counter -= self.h_velocity
            if self.x > self.l_boundary:
                self.x -= self.h_velocity
            else:
                self.right_background_shift = True

        if key[py.K_d]:
            self.right_background_shift = False
            self.left = False
            self.right = True
            self.moving = True
            self.h_movement_counter += self.h_velocity
            if self.x + self.width <= self.r_boundary:
                self.x += self.h_velocity
            else:
                self.left_background_shift = True

        if key[py.K_w]:
            self.bg_downshift = False
            self.down = False
            self.up = True
            self.moving = True
            self.v_movement_counter -= self.v_velocity
            if self.y >= self.u_boundary:
                self.y -= self.v_velocity
            else:
                self.bg_upshift = True
        else:
            self.bg_upshift = False

        if key[py.K_s]:
            self.bg_upshift = False
            self.up = False
            self.down = True
            self.moving = True
            self.v_movement_counter += self.v_velocity
            if self.y + self.height <= self.d_boundary:
                self.y += self.v_velocity
            else:
                self.bg_downshift = True
        else:
            self.bg_downshift = False

        if key[py.K_a] == False and key[py.K_d] == False and key[py.K_w] == False and key[py.K_s] == False:
            self.moving = False

    def draw_player(self, window):
        self.move_player()
        if not self.moving:
            self.run_count = 0
            if self.idle_count >= 33:
                self.idle_count = 0

            if self.left:
                window.blit(l_idle[self.idle_count // 3], (self.x, self.y))
                self.idle_count += 1
            elif self.right:
                window.blit(r_idle[self.idle_count // 3], (self.x, self.y))
                self.idle_count += 1
            else:
                window.blit(r_idle[self.idle_count // 3], (self.x, self.y))
                self.idle_count += 1

        else:
            self.idle_count = 0
            if self.run_count >= 36:
                self.run_count = 0

            if self.left:
                window.blit(l_run[self.run_count // 3], (self.x, self.y))
                self.run_count += 1
            elif self.right:
                window.blit(r_run[self.run_count // 3], (self.x, self.y))
                self.run_count += 1
            else:
                window.blit(r_run[self.run_count // 3], (self.x, self.y))
                self.run_count += 1