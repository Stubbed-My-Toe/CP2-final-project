import pygame


# ─── Palette ──────────────────────────────────────────────────────────────────
BG          = (10,  12,  14)   # near-black background
PANEL       = (18,  22,  26)   # card / panel surface
PANEL_LITE  = (26,  32,  38)   # slightly lighter panel
BORDER      = (35,  42,  50)   # subtle border
ACCENT      = (100, 220, 170)  # Cleek mint-green (logo colour)
ACCENT_DIM  = (60,  140, 105)  # muted accent
TEXT        = (230, 235, 240)  # primary text
TEXT_DIM    = (110, 120, 135)  # secondary / disabled text
WIN_GREEN   = (80,  220, 130)
LOSE_RED    = (220, 70,  70)
GOLD        = (220, 180, 60)
WHITE       = (255, 255, 255)
BLACK       = (0,   0,   0)


# ─── Fonts ────────────────────────────────────────────────────────────────────
_fonts = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("Segoe UI", size, bold=bold)
    return _fonts[key]


def font_mono(size):
    key = ("mono", size)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("Consolas", size)
    return _fonts[key]


# ─── Drawing helpers ──────────────────────────────────────────────────────────
def draw_rrect(surface, color, rect, radius=10, border=0, border_color=None):
    """Rounded rectangle. If border > 0 draws outline too."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border > 0 and border_color:
        pygame.draw.rect(surface, border_color, rect, width=border, border_radius=radius)


def draw_text(surface, text, size, color, x, y, anchor="topleft", bold=False):
    surf = font(size, bold).render(str(text), True, color)
    r = surf.get_rect(**{anchor: (x, y)})
    surface.blit(surf, r)
    return r


def draw_text_mono(surface, text, size, color, x, y, anchor="topleft"):
    surf = font_mono(size).render(str(text), True, color)
    r = surf.get_rect(**{anchor: (x, y)})
    surface.blit(surf, r)
    return r


# ─── Logo ─────────────────────────────────────────────────────────────────────
def draw_logo(surface, x, y, size=52):
    """Draw the Cleek logo (chip + wordmark) at top-right corner."""
    # chip circle
    cx, cy = x, y + size // 2
    r = size // 2
    pygame.draw.circle(surface, ACCENT, (cx, cy), r)
    pygame.draw.circle(surface, BG, (cx, cy), r - 6)
    # spade symbol (simplified)
    spade_pts = [
        (cx, cy - r + 14),
        (cx + 10, cy - 2),
        (cx + 6, cy + 2),
        (cx + 3, cy + 8),
        (cx - 3, cy + 8),
        (cx - 6, cy + 2),
        (cx - 10, cy - 2),
    ]
    pygame.draw.polygon(surface, ACCENT, spade_pts)
    # outer tick marks
    for i in range(8):
        import math
        angle = math.radians(i * 45)
        ix = cx + int((r - 3) * math.cos(angle))
        iy = cy + int((r - 3) * math.sin(angle))
        ox = cx + int(r * math.cos(angle))
        oy = cy + int(r * math.sin(angle))
        pygame.draw.line(surface, ACCENT, (ix, iy), (ox, oy), 2)
    # word mark
    draw_text(surface, "Cleek", size - 12, ACCENT, cx + r + 8, cy, anchor="midleft", bold=True)


def draw_logo_corner(surface, margin=14):
    """Draw logo pinned to top-right of surface."""
    w = surface.get_width()
    logo_w = 120
    draw_logo(surface, w - logo_w - margin, margin)


# ─── HUD wallet strip ─────────────────────────────────────────────────────────
def draw_hud(surface, cash, username=""):
    """Top-left HUD showing balance and username."""
    hud_rect = pygame.Rect(14, 14, 260, 44)
    draw_rrect(surface, PANEL_LITE, hud_rect, radius=8, border=1, border_color=BORDER)
    draw_text(surface, f"${cash:,.2f}", 22, ACCENT, 28, 36, anchor="midleft", bold=True)
    if username:
        draw_text(surface, username, 15, TEXT_DIM, 180, 36, anchor="midright")


# ─── Generic button ───────────────────────────────────────────────────────────
class Button:
    def __init__(self, label, rect, color=PANEL_LITE, hover_color=ACCENT,
                 text_color=TEXT, hover_text=BG, radius=8, font_size=18, bold=False):
        self.label = label
        self.rect  = pygame.Rect(rect)
        self.color = color
        self.hover_color = hover_color
        self.text_color  = text_color
        self.hover_text  = hover_text
        self.radius = radius
        self.font_size = font_size
        self.bold  = bold
        self._hovered = False


    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        self._hovered = self.rect.collidepoint(mx, my)
        bg = self.hover_color if self._hovered else self.color
        tc = self.hover_text  if self._hovered else self.text_color
        draw_rrect(surface, bg, self.rect, self.radius, border=1,
                   border_color=ACCENT if not self._hovered else ACCENT_DIM)
        draw_text(surface, self.label, self.font_size, tc,
                  self.rect.centerx, self.rect.centery, anchor="center", bold=self.bold)


    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# ─── Back-to-menu button ──────────────────────────────────────────────────────
def make_back_button(x=20, y=20):
    return Button("Main Menu", (x, y, 130, 38),
                  color=PANEL_LITE, hover_color=LOSE_RED,
                  hover_text=WHITE, font_size=16)


# ─── Bet input widget ─────────────────────────────────────────────────────────
class BetBar:
    """A compact bet-adjust strip: [−] $amount [+] [MAX]"""
    def __init__(self, cx, y, min_bet=1, max_bet=None, default=10, step=5):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.bet     = default
        self.step    = step
        self._cx = cx
        self._y  = y
        w = 40
        self.btn_minus = Button("−", (cx - 120, y, w, 36), font_size=20)
        self.btn_plus  = Button("+", (cx +  80, y, w, 36), font_size=20)
        self.btn_max   = Button("MAX", (cx + 128, y, 52, 36), font_size=14,
                                color=PANEL_LITE, hover_color=GOLD, hover_text=BG)


    def handle(self, event, cash):
        if self.btn_minus.is_clicked(event):
            self.bet = max(self.min_bet, self.bet - self.step)
        if self.btn_plus.is_clicked(event):
            limit = min(self.max_bet or cash, cash)
            self.bet = min(limit, self.bet + self.step)
        if self.btn_max.is_clicked(event):
            self.bet = min(self.max_bet or cash, cash)


    def draw(self, surface):
        self.btn_minus.draw(surface)
        self.btn_plus.draw(surface)
        self.btn_max.draw(surface)
        label_rect = pygame.Rect(self._cx - 76, self._y, 152, 36)
        draw_rrect(surface, PANEL, label_rect, radius=6, border=1, border_color=BORDER)
        draw_text(surface, f"BET  ${self.bet}", 18, ACCENT,
                  label_rect.centerx, label_rect.centery, anchor="center", bold=True)


    @property
    def value(self):
        return self.bet


# ─── Notification banner ──────────────────────────────────────────────────────
class Banner:
    def __init__(self):
        self.msg   = ""
        self.color = ACCENT
        self.timer = 0


    def show(self, msg, color=ACCENT, duration=120):
        self.msg   = msg
        self.color = color
        self.timer = duration


    def update_draw(self, surface):
        if self.timer <= 0:
            return
        self.timer -= 1
        alpha = min(255, self.timer * 4)
        s = font(28, bold=True).render(self.msg, True, self.color)
        s.set_alpha(alpha)
        cx = surface.get_width() // 2
        cy = surface.get_height() // 2 - 60
        r  = s.get_rect(center=(cx, cy))
        bg = pygame.Surface((r.w + 30, r.h + 14), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        surface.blit(bg, (r.x - 15, r.y - 7))
        surface.blit(s, r)
