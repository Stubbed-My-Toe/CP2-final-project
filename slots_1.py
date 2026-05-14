import pygame
import random
import helper_1
import theme_1 as T


# ─── Slot symbols (drawn with text) ──────────────────────────────────────────
SYMBOLS     = ["7", "★", "♦", "♣", "♥", "A", "BAR"]
SYM_COLORS  = [T.GOLD, T.ACCENT, (100, 160, 240), T.TEXT, T.LOSE_RED, T.TEXT, T.TEXT_DIM]
WEIGHTS     = [2, 4, 8, 14, 20, 25, 100]   # cumulative weights
MULTIPLIERS = [200, 70, 30, 15, 7, 5, 3]   # index matches sorted symbol rarity
COLS        = 3
ROWS        = 3   # visible rows per reel
REEL_COUNT  = 3
CELL_W      = 110
CELL_H      = 90
REEL_PAD    = 16




def _weighted(symbols, weights):
    r = random.uniform(0, 100)
    prev = 0
    for i, w in enumerate(weights):
        if prev < r <= w:
            return i
        prev = w
    return len(symbols) - 1




class Reel:
    """One column of symbols that can spin and stop."""
    def __init__(self, x, y):
        self.x    = x
        self.y    = y                    # top-left of visible area
        self.syms = [random.randint(0, 6) for _ in range(ROWS + 4)]
        self.vel  = 0.0
        self.offset = 0.0               # pixel scroll within a cell
        self.spinning = False
        self.target_sym = None


    def start(self):
        self.vel     = 28.0
        self.spinning = True


    def stop(self, result_idx):
        self.target_sym = result_idx
        self.spinning   = False
        # spin a bit more before locking
        self.vel = max(self.vel, 16.0)


    def update(self):
        if self.vel <= 0:
            return
        self.offset += self.vel
        while self.offset >= CELL_H:
            self.offset -= CELL_H
            self.syms.pop()
            self.syms.insert(0, random.randint(0, 6))
        # decelerate
        if not self.spinning:
            self.vel *= 0.88
            if self.vel < 1.5:
                self.vel = 0.0
                self.offset = 0.0
                if self.target_sym is not None:
                    self.syms[1] = self.target_sym   # lock middle row


    @property
    def stopped(self):
        return self.vel == 0.0


    def middle_sym(self):
        return self.syms[1]


    def draw(self, surface):
        clip = pygame.Rect(self.x, self.y, CELL_W, ROWS * CELL_H)
        surface.set_clip(clip)
        for i in range(ROWS + 2):
            cy = self.y + (i - 1) * CELL_H + int(self.offset)
            idx = self.syms[i] if i < len(self.syms) else 0
            r = pygame.Rect(self.x + 4, cy + 4, CELL_W - 8, CELL_H - 8)
            T.draw_rrect(surface, T.PANEL_LITE, r, radius=8)
            sym = SYMBOLS[idx]
            col = SYM_COLORS[idx]
            sz  = 36 if len(sym) <= 1 else 22
            T.draw_text(surface, sym, sz, col,
                        self.x + CELL_W // 2, cy + CELL_H // 2,
                        anchor="center", bold=True)
        surface.set_clip(None)




def slots_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data  = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash  = float(data["cash"])


    CX = W // 2
    board_w = REEL_COUNT * CELL_W + (REEL_COUNT - 1) * REEL_PAD
    board_x = CX - board_w // 2
    board_y = H // 2 - (ROWS * CELL_H) // 2


    reels = [
        Reel(board_x + i * (CELL_W + REEL_PAD), board_y)
        for i in range(REEL_COUNT)
    ]


    bet_bar = T.BetBar(CX, H - 110, min_bet=1, default=10, step=5)
    btn_spin = T.Button("SPIN", (CX - 80, H - 60, 160, 48),
                        color=T.ACCENT, hover_color=T.ACCENT_DIM,
                        text_color=T.BG, hover_text=T.BG, bold=True, font_size=22)
    btn_back = T.make_back_button()
    banner   = T.Banner()


    spinning   = False
    stopping   = False
    results    = []
    stop_timers = [0, 0, 0]   # frame delays for each reel stop
    cooldown   = 0


    clock   = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
            if btn_back.is_clicked(e):
                file.update_row(
                    {"username": username, "password": password},
                    {"cash": cash,
                     "times_played_slots": int(data["times_played_slots"]) + 1}
                )
                return


            if not spinning and btn_spin.is_clicked(e) and cooldown <= 0:
                bet = bet_bar.value
                if bet > cash:
                    banner.show("Insufficient funds", T.LOSE_RED)
                else:
                    cash -= bet
                    # Decide results before spinning starts
                    results = [_weighted(SYMBOLS, WEIGHTS) for _ in range(REEL_COUNT)]
                    for r in reels:
                        r.start()
                    stop_timers = [90, 140, 190]  # frames until each reel stops
                    spinning   = True
                    stopping   = False
                    cooldown   = 40


            bet_bar.handle(e, cash)


        cooldown -= 1


        # ── Reel stop logic ───────────────────────────────────────────────────
        if spinning:
            for i, (reel, timer) in enumerate(zip(reels, stop_timers)):
                if timer > 0:
                    stop_timers[i] -= 1
                elif reel.spinning:
                    reel.stop(results[i])


            for r in reels:
                r.update()


            # All reels stopped
            if all(r.stopped for r in reels) and not stopping:
                stopping = True
                spinning  = False
                # Check win: middle row all same
                mid = [r.middle_sym() for r in reels]
                if mid[0] == mid[1] == mid[2]:
                    mult = MULTIPLIERS[mid[0]]
                    bet_val = bet_bar.value + bet_bar.value  # already deducted, recalc
                    # we need to store bet before spin
                    gain = round(bet_bar.value * mult, 2)
                    cash += gain
                    banner.show(f"WIN!  {SYMBOLS[mid[0]]} x{mult}  +${gain:.2f}", T.WIN_GREEN, 180)
                else:
                    banner.show("No match", T.LOSE_RED)
                file.update_row(
                    {"username": username, "password": password},
                    {"cash": cash}
                )
        else:
            for r in reels:
                r.update()


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        # subtle vertical glow behind board
        glow = pygame.Surface((board_w + 60, ROWS * CELL_H + 60), pygame.SRCALPHA)
        glow.fill((100, 220, 170, 12))
        win.blit(glow, (board_x - 30, board_y - 30))


        T.draw_logo_corner(win)
        T.draw_hud(win, cash, username)
        btn_back.draw(win)


        T.draw_text(win, "SLOTS", 48, T.TEXT, CX, 50, anchor="midtop", bold=True)


        # board frame
        board_rect = pygame.Rect(board_x - 8, board_y - 8,
                                 board_w + 16, ROWS * CELL_H + 16)
        T.draw_rrect(win, T.PANEL, board_rect, radius=14, border=2, border_color=T.BORDER)


        for r in reels:
            r.draw(win)


        # payline highlight
        mid_y = board_y + CELL_H + CELL_H // 2
        pygame.draw.line(win, T.ACCENT,
                         (board_x - 12, mid_y), (board_x + board_w + 12, mid_y), 2)


        # bet + spin
        bet_bar.draw(win)
        label = "SPINNING..." if spinning else "SPIN"
        btn_spin.label = label
        btn_spin.draw(win)


        # paytable hint
        T.draw_text(win, "Match the centre row  |  7 = 200x  ★ = 70x  ♦ = 30x  ♣ = 15x  ♥ = 7x",
                    13, T.TEXT_DIM, CX, H - 18, anchor="midbottom")


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)