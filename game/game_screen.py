import pygame as py
from game.player import player
from game.bg_render import bg_render
from game.zombie import zombie
from game.projectile import projectile
from game.question_db import get_random_question, record_attempt
from game.question_overlay import QuestionOverlay
from game.score_db import submit_score
from game.settings_db import get_background
import random


class game_screen:
    def __init__(self, width, height, user_email):
        self.width = width
        self.height = height
        bg_file = get_background(user_email)
        self.bg = bg_render(width, height, bg_file)
        self.cam_x = 0 #Added in camera view variables
        self.cam_y = 0

        # Questions
        self.user_email = user_email  # pass real logged-in email here
        self.state = "PLAY"  # PLAY or QUESTION
        self.current_question = None
        self.q_overlay = QuestionOverlay(width, height)
        self.last_answer_result = None  # None / True / False (optional feedback)

        # Zombie spawning variables
        self.start_time_ms = py.time.get_ticks()
        self.last_spawn_ms = 0
        self.spawn_interval_ms = 800    # start ~1.25 zombies/sec
        self.min_interval_ms = 250      # cap at 4 zombies/sec
        self.ramp_every_ms = 4000       # every 4s, speed up spawns
        self.ramp_step_ms = 60          # subtract 60ms each ramp
        self.bullets = []
        self.cooldown_counter = 0
        self.cooldown_frames = 6
        self.max_bullets = 5

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
        self.score = 0
        self.pending_life_loss = False # Prevents accidentally subtracting multiple times

        self.zombie_list = []

        self.bg_speed = 6
        self.ui_font = py.font.SysFont("arial", 30, True)

    def handle_screen(self, event):
        # While question is showing, consume input here
        if self.state == "QUESTION":
            choice = self.q_overlay.handle_event(event)
            if choice and self.current_question:
                self.process_answer(choice)
            return None

        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                return "lobby_screen"
            if event.key == py.K_SPACE:
                self.try_shoot()
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

    def try_shoot(self):
        if self.cooldown_counter != 0:
            return
        if len(self.bullets) >= self.max_bullets:
            return

        self.cooldown_counter = self.cooldown_frames

        speed = 15
        keys = py.key.get_pressed()

        # Aim: if holding W/S, shoot vertical. Otherwise shoot left/right based on facing.
        if keys[py.K_w]:
            vx, vy = 0, -speed
        elif keys[py.K_s]:
            vx, vy = 0, speed
        else:
            vx = -speed if self.p.left else speed
            vy = 0

        # player center in WORLD coords
        pwx = (self.p.x - self.cam_x) + self.p.width / 2
        pwy = (self.p.y - self.cam_y) + self.p.height / 2

        b = projectile(pwx, pwy, 5, (0, 0, 0), vx, vy)
        self.bullets.append(b)

    def tick_cooldown(self): # For projectile
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

    def update_bullets(self):
        # iterate backwards so popping is safe
        for i in range(len(self.bullets) - 1, -1, -1):
            b = self.bullets[i]
            b.update()

            # remove if far off-screen (screen check is easiest)
            sx, sy = b.screen_pos(self.cam_x, self.cam_y)
            if sx < -100 or sx > self.width + 100 or sy < -100 or sy > self.height + 100:
                self.bullets.pop(i)
                continue

            # collision (WORLD coords)
            for z in self.zombie_list:
                if not z.visible:
                    continue

                hb = z.world_hitbox()  # world rect
                # circle-rect overlap quick check
                if hb.collidepoint(b.x, b.y):
                    died = z.hit()
                    if died:
                        self.score += 1
                    self.bullets.pop(i)
                    break

    def handle_player_hits(self):
        # Cooldowns tick first
        self.p.tick()

        if not self.zombie_list:
            return

        p_rect = self.p.world_hitbox(self.cam_x, self.cam_y)

        for z in self.zombie_list:
            if not z.visible:
                continue

            z_rect = z.world_hitbox()
            if p_rect.colliderect(z_rect):
                self.p.take_hit(self.p.damage_on_hit)
                break

    def process_answer(self, chosen):
        q = self.current_question
        correct = (chosen == q["correct"])

        # store attempt in DB
        record_attempt(self.user_email, q["id"], chosen, correct)

        if correct:
            # revive player
            self.p.hp = 100
            self.p.alive = True
            self.p.invuln_frames = 60  # brief i-frames after revive
            self.state = "PLAY"
            self.current_question = None
            self.pending_life_loss = False
        else:
            # wrong: keep them dead, but show another question (or keep same)
            # simplest: show a new random question
            self.current_question = get_random_question()

    def draw(self, window):
        self.bg.draw(window)
        self.p.draw_player(window)
        self.shift_background_from_player_flags()
        self.handle_zombie()
        self.handle_player_hits()

        # If game is over, save score and go back to lobby
        if self.p.lives <= 0:
            submit_score(self.user_email, self.score)
            return "lobby_screen"

        # If player is answering a question, pause gameplay updates
        if self.state == "QUESTION":
            if self.current_question:
                self.q_overlay.draw(window, self.current_question)
            return

        self.tick_cooldown()
        self.update_bullets()

        hp_text = self.ui_font.render(f"HP: {self.p.hp}", True, (255, 0, 0))
        window.blit(hp_text, (20, 20))

        score_text = self.ui_font.render(f"Score: {self.score}", True, (255, 255, 255))
        window.blit(score_text, (self.width - score_text.get_width() - 20, 20))

        lives_text = self.ui_font.render(f"Lives: {self.p.lives}", True, (255, 255, 255))
        window.blit(lives_text, (20, 55))

        if self.p.alive == False:
            alive_text = self.ui_font.render(f"You are dead", True, (255, 0, 0))
            window.blit(alive_text, (100, 20))

        for z in self.zombie_list:
            z.draw(window, self.cam_x, self.cam_y)

        for b in self.bullets:
            b.draw(window, self.cam_x, self.cam_y)

        if self.state == "PLAY" and not self.p.alive:
            # Lose exactly one life per death event
            if not self.pending_life_loss:
                self.p.lose_life()
                self.pending_life_loss = True

            # If no lives left, save score and return to lobby screen
            if self.p.lives <= 0:
                submit_score(self.user_email, self.score)
                return "lobby_screen"

            # Otherwise show a question to revive
            self.state = "QUESTION"
            self.current_question = get_random_question()
            self.last_answer_result = None