import pygame as py

class QuestionOverlay:
    """
    Big 2x2 buttons like Kahoot:
    A (top-left), B (top-right), C (bottom-left), D (bottom-right)
    Return chosen option when user answers, otherwise None.
    """
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.font_q = py.font.SysFont("arial", 36, True)
        self.font_opt = py.font.SysFont("arial", 28, True)

        pad = 30
        box_w = (width - pad * 3) // 2
        box_h = (height - 220 - pad * 3) // 2

        top_y = 180
        left_x = pad
        right_x = pad * 2 + box_w
        bottom_y = top_y + pad + box_h

        self.rects = {
            "A": py.Rect(left_x,  top_y,    box_w, box_h),
            "B": py.Rect(right_x, top_y,    box_w, box_h),
            "C": py.Rect(left_x,  bottom_y, box_w, box_h),
            "D": py.Rect(right_x, bottom_y, box_w, box_h),
        }

        self.hover = None

    def handle_event(self, event):
        # Keyboard answers
        if event.type == py.KEYDOWN:
            key_map = {py.K_a: "A", py.K_b: "B", py.K_c: "C", py.K_d: "D"}
            if event.key in key_map:
                return key_map[event.key]

        # Mouse hover
        if event.type == py.MOUSEMOTION:
            mx, my = event.pos
            self.hover = None
            for k, r in self.rects.items():
                if r.collidepoint(mx, my):
                    self.hover = k
                    break

        # Mouse click
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for k, r in self.rects.items():
                if r.collidepoint(mx, my):
                    return k

        return None

    def draw(self, window, question_dict):
        # dark overlay
        overlay = py.Surface((self.w, self.h))
        overlay.set_alpha(210)
        overlay.fill((0, 0, 0))
        window.blit(overlay, (0, 0))

        # Question text (simple wrap)
        q_text = question_dict["text"]
        lines = self._wrap_text(q_text, self.font_q, self.w - 60)
        y = 40
        for line in lines[:3]:
            surf = self.font_q.render(line, True, (255, 255, 255))
            window.blit(surf, (30, y))
            y += surf.get_height() + 6

        # Draw options
        for opt in ("A", "B", "C", "D"):
            r = self.rects[opt]
            # base colour by option (Kahoot vibe without needing exact colours)
            base = {"A": (200, 60, 60), "B": (60, 120, 220), "C": (70, 180, 90), "D": (220, 170, 60)}[opt]
            col = base

            # hover highlight
            if self.hover == opt:
                col = (min(255, col[0] + 30), min(255, col[1] + 30), min(255, col[2] + 30))

            py.draw.rect(window, col, r, border_radius=16)
            py.draw.rect(window, (255, 255, 255), r, 3, border_radius=16)

            text = f"{opt}) {question_dict[opt]}"
            text_lines = self._wrap_text(text, self.font_opt, r.w - 20)
            ty = r.y + 18
            for line in text_lines[:3]:
                surf = self.font_opt.render(line, True, (255, 255, 255))
                window.blit(surf, (r.x + 14, ty))
                ty += surf.get_height() + 4

        hint = py.font.SysFont("arial", 20).render("Click an answer or press A/B/C/D", True, (220, 220, 220))
        window.blit(hint, (30, self.h - 40))

    def _wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if font.size(" ".join(cur))[0] > max_width:
                cur.pop()
                lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
        return lines