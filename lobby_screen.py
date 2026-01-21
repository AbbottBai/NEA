import pygame as py

# Creates a reusable class for buttons.
class Button:
    def __init__(self, rect, text, font, bg_colour,fg_colour):
        self.rect = py.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg_colour
        self.hover = (210,210,210)
        self.fg = fg_colour
        self.border = (40,40,40)
        self.border_w = 2
        self.radius = 14

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surf, mouse_pos):
        hovered = self.is_hovered(mouse_pos)
        color = self.hover if hovered else self.bg

        py.draw.rect(surf, color, self.rect, border_radius=self.radius)
        py.draw.rect(surf, self.border, self.rect, self.border_w, border_radius=self.radius)

        txt = self.font.render(self.text, True, self.fg)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == py.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def create_leaderboard_ui(screen, width, height):
    # Creates a placeholder for leaderboard data which will be integrated with backend later
    leaderboard = [
        {"name": "Player 1", "score": 100},
        {"name": "Player 2", "score": 95},
        {"name": "Player 3", "score": 90},
        {"name": "Player 4", "score": 85},
        {"name": "Player 5", "score": 80}
    ]

    # Set up fonts
    title_height = 80
    name_height = 50
    score_height = name_height - 5
    font_title = py.font.Font(None, title_height)
    font_name = py.font.Font(None, name_height)
    font_score = py.font.Font(None, score_height)

    # Create the leaderboard title
    title = font_title.render("Leaderboard", True, (0, 0, 0))
    screen.blit(title, (width // 2 - 170, 40))

    # Draw each player
    for i, player in enumerate(leaderboard):
        name = font_name.render(player["name"], True, (0,0,0))
        score = font_score.render(str(player["score"]), True, (0,0,0))

        # Position players from top to bottom based on index
        y_pos = height - (i * (name_height + score_height)) - 200
        x_pos = width // 2 - 150

        screen.blit(name, (x_pos + 10, y_pos))
        screen.blit(score, (x_pos + 250, y_pos))


# Actual lobby screen class
class lobby_screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.lb_background = py.image.load("lb_background.jpg")
        self.lb_background = py.transform.scale(self.lb_background, (self.width, self.height))

        # Buttons
        button_w, button_h = 360, 80 # I combined the play and signout button width and heights as they are equal
        gap = 40
        bottom_margin = 40

        total_width = button_w + gap + button_w # These calculates and positions the buttons
        start_x = (self.width - total_width) // 2 + 200
        y_play = self.height - bottom_margin - button_h
        y_sign = self.height - bottom_margin - button_h
        #The calculations looks confusing as it had to be fine tuned a lot.

        self.play_button = Button(
            (start_x, y_play, button_w, button_h),
            "Play Game",
            py.font.SysFont("arial", 30, bold=True),
            (255,0,0),
            (0,0,255)
        )

        self.signout_button = Button(
            (start_x + button_w + gap, y_sign, button_w, button_h),
            "Sign out",
            py.font.SysFont("arial", 26, bold=True),
            (255,0,0),
            (0,0,255)
        )

        self.setting_button = Button(
            (start_x - button_w - gap, y_play, button_w, button_h),
        "Settings",
            py.font.SysFont("arial", 28, bold=True),
            (128, 128, 128),
            (0, 0, 255)
        )

    def handle_screen(self, event):
        if self.play_button.clicked(event):
            return "play" #not working, just a placeholder for now.
        if self.signout_button.clicked(event):
            return "login_screen" # This switches screen back to login screen.
        return None

    def draw(self, window):
        window.blit(self.lb_background, (0, 0))
        mouse = py.mouse.get_pos()

        self.play_button.draw(window, mouse)
        self.signout_button.draw(window, mouse)
        self.setting_button.draw(window, mouse)
        create_leaderboard_ui(window, self.width, self.height)
