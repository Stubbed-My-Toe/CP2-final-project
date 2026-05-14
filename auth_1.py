import pygame
import helper_1
import theme_1 as T




# ─── Simple text-input widget ─────────────────────────────────────────────────
class TextInput:
    def __init__(self, rect, placeholder="", password=False, font_size=20):
        self.rect        = pygame.Rect(rect)
        self.placeholder = placeholder
        self.password    = password
        self.font_size   = font_size
        self.text        = ""
        self.active      = False
        self.cursor_tick = 0


    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB):
                if len(self.text) < 32:
                    self.text += event.unicode


    def draw(self, surface):
        self.cursor_tick += 1
        border_col = T.ACCENT if self.active else T.BORDER
        T.draw_rrect(surface, T.PANEL, self.rect, radius=8,
                     border=2, border_color=border_col)
        display = ("•" * len(self.text)) if self.password else self.text
        if display:
            T.draw_text(surface, display, self.font_size, T.TEXT,
                        self.rect.x + 12, self.rect.centery, anchor="midleft")
        else:
            T.draw_text(surface, self.placeholder, self.font_size, T.TEXT_DIM,
                        self.rect.x + 12, self.rect.centery, anchor="midleft")
        # blinking cursor
        if self.active and (self.cursor_tick // 30) % 2 == 0:
            shown = ("•" * len(self.text)) if self.password else self.text
            tw = T.font(self.font_size).size(shown)[0]
            cx = self.rect.x + 14 + tw
            cy = self.rect.centery
            pygame.draw.line(surface, T.ACCENT,
                             (cx, cy - 10), (cx, cy + 10), 2)


    @property
    def value(self):
        return self.text.strip()




# ─── Shared background draw ───────────────────────────────────────────────────
def _draw_bg(surface):
    surface.fill(T.BG)
    w, h = surface.get_size()
    # subtle diagonal lines texture
    for i in range(-h, w + h, 48):
        pygame.draw.line(surface, (20, 24, 28), (i, 0), (i + h, h), 1)
    T.draw_logo_corner(surface)




# ─── LOGIN SCREEN ─────────────────────────────────────────────────────────────
def login_screen(win, csv_file_obj):
    """
    Returns user data dict on success, or None if user quit.
    """
    W, H = win.get_size()
    cx   = W // 2


    box_w, box_h = 420, 360
    box = pygame.Rect(cx - box_w // 2, H // 2 - box_h // 2, box_w, box_h)


    inp_user = TextInput((cx - 160, H // 2 - 70, 320, 46), placeholder="Username")
    inp_pass = TextInput((cx - 160, H // 2 - 10, 320, 46), placeholder="Password", password=True)


    btn_login  = T.Button("Sign In",  (cx - 160, H // 2 + 58, 148, 44),
                          color=T.ACCENT, hover_color=T.ACCENT_DIM,
                          text_color=T.BG, hover_text=T.BG, bold=True)
    btn_signup = T.Button("Create Account", (cx + 12, H // 2 + 58, 148, 44), font_size=15)


    error_msg = ""
    clock     = pygame.time.Clock()


    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return None


            inp_user.handle(e)
            inp_pass.handle(e)


            if btn_login.is_clicked(e):
                data = helper_1.csv_get_data(
                    csv_file_obj,
                    {"username": inp_user.value, "password": inp_pass.value}
                )
                if data:
                    return data
                else:
                    error_msg = "Invalid username or password."


            if btn_signup.is_clicked(e):
                result = signup_screen(win, csv_file_obj)
                if result:
                    return result


        _draw_bg(win)
        T.draw_rrect(win, T.PANEL, box, radius=16, border=1, border_color=T.BORDER)


        T.draw_text(win, "Welcome Back", 32, T.TEXT, cx, box.y + 32, anchor="midtop", bold=True)
        T.draw_text(win, "Sign in to your Cleek account", 16, T.TEXT_DIM, cx, box.y + 72, anchor="midtop")


        T.draw_text(win, "Username", 14, T.TEXT_DIM, cx - 160, H // 2 - 88, anchor="topleft")
        inp_user.draw(win)
        T.draw_text(win, "Password", 14, T.TEXT_DIM, cx - 160, H // 2 - 28, anchor="topleft")
        inp_pass.draw(win)


        btn_login.draw(win)
        btn_signup.draw(win)


        if error_msg:
            T.draw_text(win, error_msg, 15, T.LOSE_RED, cx, H // 2 + 112, anchor="midtop")


        pygame.display.flip()
        clock.tick(60)




# ─── SIGN-UP SCREEN ───────────────────────────────────────────────────────────
def signup_screen(win, csv_file_obj):
    W, H = win.get_size()
    cx   = W // 2


    box_w, box_h = 420, 420
    box = pygame.Rect(cx - box_w // 2, H // 2 - box_h // 2, box_w, box_h)


    inp_user  = TextInput((cx - 160, H // 2 - 90, 320, 46), placeholder="Username")
    inp_pass  = TextInput((cx - 160, H // 2 - 30, 320, 46), placeholder="Password", password=True)
    inp_pass2 = TextInput((cx - 160, H // 2 + 30, 320, 46), placeholder="Confirm Password", password=True)


    btn_create = T.Button("Create Account", (cx - 160, H // 2 + 96, 148, 44),
                          color=T.ACCENT, hover_color=T.ACCENT_DIM,
                          text_color=T.BG, hover_text=T.BG, bold=True)
    btn_back   = T.Button("Back", (cx + 12, H // 2 + 96, 148, 44), font_size=15)


    error_msg   = ""
    success_msg = ""
    clock       = pygame.time.Clock()


    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return None
            inp_user.handle(e)
            inp_pass.handle(e)
            inp_pass2.handle(e)


            if btn_back.is_clicked(e):
                return None


            if btn_create.is_clicked(e):
                u = inp_user.value
                p = inp_pass.value
                p2 = inp_pass2.value
                if not u or not p:
                    error_msg = "Username and password required."
                elif p != p2:
                    error_msg = "Passwords do not match."
                elif len(u) < 3:
                    error_msg = "Username must be at least 3 characters."
                else:
                    ok = helper_1.csv_add_user(csv_file_obj, u, p, cash=1000)
                    if ok:
                        # auto-login
                        data = helper_1.csv_get_data(csv_file_obj, {"username": u, "password": p})
                        return data
                    else:
                        error_msg = "Username already taken."


        _draw_bg(win)
        T.draw_rrect(win, T.PANEL, box, radius=16, border=1, border_color=T.BORDER)


        T.draw_text(win, "Create Account", 32, T.TEXT, cx, box.y + 32, anchor="midtop", bold=True)
        T.draw_text(win, "Join Cleek — starts with $1,000", 16, T.TEXT_DIM, cx, box.y + 72, anchor="midtop")


        T.draw_text(win, "Username",         14, T.TEXT_DIM, cx - 160, H // 2 - 108, anchor="topleft")
        inp_user.draw(win)
        T.draw_text(win, "Password",         14, T.TEXT_DIM, cx - 160, H // 2 - 48,  anchor="topleft")
        inp_pass.draw(win)
        T.draw_text(win, "Confirm Password", 14, T.TEXT_DIM, cx - 160, H // 2 + 12,  anchor="topleft")
        inp_pass2.draw(win)


        btn_create.draw(win)
        btn_back.draw(win)


        if error_msg:
            T.draw_text(win, error_msg, 15, T.LOSE_RED, cx, H // 2 + 148, anchor="midtop")


        pygame.display.flip()
        clock.tick(60)
