import pygame
import random
import helper_1
import theme_1 as T




def _draw_slider_track(surface, rect, target, over):
    """Custom dice slider visual."""
    # track background
    T.draw_rrect(surface, T.PANEL_LITE, rect, radius=6)
    # fill region (win zone)
    track_w = rect.width - 4
    track_x = rect.x + 2
    track_y = rect.y + 2
    track_h = rect.height - 4
    if over:
        fill_x = track_x + int(track_w * target / 100)
        fill_w = track_w - int(track_w * target / 100)
        fill_col = T.WIN_GREEN
    else:
        fill_x = track_x
        fill_w = int(track_w * target / 100)
        fill_col = T.WIN_GREEN
    if fill_w > 0:
        pygame.draw.rect(surface, fill_col,
                         (fill_x, track_y, fill_w, track_h), border_radius=4)
    # handle
    hx = rect.x + int(rect.width * target / 100)
    pygame.draw.circle(surface, T.ACCENT, (hx, rect.centery), 10)
    pygame.draw.circle(surface, T.BG,     (hx, rect.centery),  5)




class DiceSlider:
    def __init__(self, rect):
        self.rect   = pygame.Rect(rect)
        self.target = 50.0
        self._drag  = False


    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._drag = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._drag = False
        if event.type == pygame.MOUSEMOTION and self._drag:
            rel = (event.pos[0] - self.rect.x) / self.rect.width
            self.target = max(1.0, min(99.0, rel * 100))


    def draw(self, surface, over):
        _draw_slider_track(surface, self.rect, self.target, over)


    @property
    def value(self):
        return round(self.target, 1)




def _calc_multiplier(target, over):
    try:
        if over:
            return round(99 / (100 - target), 4)
        else:
            return round(99 / target, 4)
    except ZeroDivisionError:
        return 0.0




def _roll_result_surf(win_w, roll, target, over, won):
    """Return a surface showing the animated roll value."""
    col = T.WIN_GREEN if won else T.LOSE_RED
    text = f"{roll:.2f}"
    return T.font(64, bold=True).render(text, True, col)




def dice_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash = float(data["cash"])


    CX = W // 2
    TRACK_Y = H // 2 + 20
    TRACK = pygame.Rect(CX - 350, TRACK_Y, 700, 28)


    slider = DiceSlider(TRACK)
    bet_bar = T.BetBar(CX, H // 2 - 80, min_bet=1, default=10, step=5)
    btn_over  = T.Button("Roll OVER",  (CX - 220, H // 2 + 80, 200, 48),
                         color=T.PANEL_LITE, hover_color=T.WIN_GREEN,
                         hover_text=T.BG, bold=True)
    btn_under = T.Button("Roll UNDER", (CX + 20,  H // 2 + 80, 200, 48),
                         color=T.PANEL_LITE, hover_color=T.LOSE_RED,
                         hover_text=T.WHITE, bold=True)
    btn_back  = T.make_back_button()
    banner    = T.Banner()


    roll_display = None   # last roll value
    over = True           # current direction


    clock = pygame.time.Clock()
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
                     "times_played_dice": int(data["times_played_dice"]) + 1}
                )
                return


            bet_bar.handle(e, cash)
            slider.handle(e)


            if btn_over.is_clicked(e) or btn_under.is_clicked(e):
                over = btn_over.is_clicked(e)
                bet  = bet_bar.value
                if bet > cash:
                    banner.show("Insufficient funds", T.LOSE_RED)
                else:
                    cash -= bet
                    roll  = random.uniform(0, 100)
                    won   = (roll > slider.value) if over else (roll < slider.value)
                    mult  = _calc_multiplier(slider.value, over)
                    if won:
                        gain = round(bet * mult, 2)
                        cash += gain
                        banner.show(f"+${gain:.2f}  (x{mult:.2f})", T.WIN_GREEN)
                    else:
                        banner.show(f"-${bet:.2f}  Rolled {roll:.2f}", T.LOSE_RED)
                    roll_display = (roll, slider.value, over, won)
                    # save after each round
                    file.update_row(
                        {"username": username, "password": password},
                        {"cash": cash}
                    )


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        # subtle grid
        for gy in range(0, H, 60):
            pygame.draw.line(win, (16, 20, 24), (0, gy), (W, gy))
        for gx in range(0, W, 60):
            pygame.draw.line(win, (16, 20, 24), (gx, 0), (gx, H))


        T.draw_logo_corner(win)
        T.draw_hud(win, cash, username)
        btn_back.draw(win)


        # title
        T.draw_text(win, "DICE", 52, T.TEXT, CX, 90, anchor="center", bold=True)
        T.draw_text(win, "Set your target — bet over or under", 18, T.TEXT_DIM,
                    CX, 148, anchor="center")


        # bet bar
        bet_bar.draw(win)


        # slider
        slider.draw(win, over)
        # target label
        T.draw_text(win, f"Target: {slider.value:.1f}", 18, T.TEXT,
                    CX, TRACK_Y + 38, anchor="midtop", bold=True)
        # range labels
        T.draw_text(win, "0", 14, T.TEXT_DIM, TRACK.x, TRACK_Y + 38, anchor="midtop")
        T.draw_text(win, "100", 14, T.TEXT_DIM, TRACK.right, TRACK_Y + 38, anchor="midtop")


        # multiplier preview
        mult = _calc_multiplier(slider.value, True)
        T.draw_text(win, f"Over multiplier: x{_calc_multiplier(slider.value, True):.2f}",
                    15, T.TEXT_DIM, CX - 220, H // 2 + 140, anchor="midtop")
        T.draw_text(win, f"Under multiplier: x{_calc_multiplier(slider.value, False):.2f}",
                    15, T.TEXT_DIM, CX + 20, H // 2 + 140, anchor="midtop")


        btn_over.draw(win)
        btn_under.draw(win)


        # last roll
        if roll_display:
            roll, tgt, ov, won = roll_display
            surf = _roll_result_surf(W, roll, tgt, ov, won)
            win.blit(surf, surf.get_rect(center=(CX, H - 140)))
            dir_str = f"Rolled {'OVER' if ov else 'UNDER'} {tgt:.1f}"
            T.draw_text(win, dir_str, 18, T.TEXT_DIM, CX, H - 90, anchor="midtop")


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)


