
import pygame
import random
import helper_1
import theme_1 as T


# ── Constants ────────────────────────────────────────────────────────────────
GRID      = 5
CELLS     = GRID * GRID          # 25 tiles
CELL_SIZE = 90
CELL_GAD  = 8                    # gap between cells




def _calc_multiplier(safe_clicked, mines):
    """
    Fair-odds multiplier: probability of not hitting any mine after
    safe_clicked safe picks, with 3% house edge.
    Matches standard casino Mines math.
    """
    if safe_clicked == 0:
        return 1.0
    safe_total = CELLS - mines
    prob = 1.0
    for i in range(safe_clicked):
        remaining = CELLS - i
        safe_left = safe_total - i
        if remaining <= 0 or safe_left <= 0:
            return 0.0
        prob *= safe_left / remaining
    if prob <= 0:
        return 0.0
    return round(0.97 / prob, 2)   # 3% house edge




def mines_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data  = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash  = float(data["cash"])


    # ── Layout ────────────────────────────────────────────────────────────────
    board_px = GRID * CELL_SIZE + (GRID - 1) * CELL_GAD
    board_x  = W // 2 - board_px // 2 + 60   # slight right to leave room for panel
    board_y  = H // 2 - board_px // 2


    panel_x  = 40
    panel_w  = board_x - 80
    panel_y  = board_y


    CX = W // 2


<<<<<<< HEAD
    # Widgets
    bet_bar    = T.BetBar(panel_x + panel_w // 2, panel_y + 60,
                          min_bet=1, default=10, step=5)
=======
    bet_bar    = T.BetBar(CX, H - 120, min_bet=1, default=10, step=5)
    mine_slider_val = [3]   # mutable box
    btn_plus_m  = T.Button("+", (CX + 130, H - 160, 36, 36), font_size=18)
    btn_minus_m = T.Button("-", (CX + 88,  H - 160, 36, 36), font_size=18)
>>>>>>> 023def92691d8dff122b14308ce53f6fbbed71dc


    # Mine count controls (simple +/- buttons)
    mc_cx      = panel_x + panel_w // 2
    btn_minus  = T.Button("−", (mc_cx - 60, panel_y + 140, 44, 38), font_size=20)
    btn_plus   = T.Button("+", (mc_cx + 16, panel_y + 140, 44, 38), font_size=20)


    btn_start  = T.Button("Bet",
                          (panel_x + 10, panel_y + 200, panel_w - 20, 48),
                          color=T.ACCENT, hover_color=T.ACCENT_DIM,
                          text_color=T.BG, hover_text=T.BG, bold=True)


    btn_cashout = T.Button("Cash Out",
                           (panel_x + 10, panel_y + 200, panel_w - 20, 48),
                           color=T.WIN_GREEN, hover_color=(60, 180, 100),
                           text_color=T.BG, hover_text=T.BG, bold=True)


    btn_back   = T.make_back_button()
    banner     = T.Banner()


    # ── Game state ────────────────────────────────────────────────────────────
    state       = "betting"   # "playing" | "lost" | "won"
    board       = []          # True = mine
    revealed    = []          # True = clicked
    safe_clicks = 0
    bet         = 0.0
    mine_count  = 3


    def reset_board(mines):
        b = [False] * CELLS
        for idx in random.sample(range(CELLS), mines):
            b[idx] = True
        return b


    def cell_rect(idx):
        col = idx % GRID
        row = idx // GRID
        x   = board_x + col * (CELL_SIZE + CELL_GAD)
        y   = board_y + row * (CELL_SIZE + CELL_GAD)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)


    # Animate gem reveal — store (idx, timer) pairs
    gem_anims = {}   # idx -> frames_remaining (counts down from 8)


    clock   = pygame.time.Clock()
    running = True


    while running:
        mouse_pos = pygame.mouse.get_pos()
        events    = pygame.event.get()


        for e in events:
            if e.type == pygame.QUIT:
                running = False


            if btn_back.is_clicked(e):
                file.update_row(
                    {"username": username, "password": password},
                    {
                        "cash": cash,
                        "times_played_mines":
                            int(data.get("times_played_mines", 0)) + 1,
                    }
                )
                return


            # ── Betting phase ─────────────────────────────────────────────────
            if state == "betting":
                bet_bar.handle(e, cash)


                if btn_minus.is_clicked(e):
                    mine_count = max(1, mine_count - 1)
                if btn_plus.is_clicked(e):
                    mine_count = min(24, mine_count + 1)


                if btn_start.is_clicked(e):
                    bet = bet_bar.value
                    if bet > cash:
                        banner.show("Insufficient funds", T.LOSE_RED)
                    else:
                        cash        -= bet
                        board        = reset_board(mine_count)
                        revealed     = [False] * CELLS
                        safe_clicks  = 0
                        gem_anims    = {}
                        state        = "playing"
                        file.update_row(
                            {"username": username, "password": password},
                            {"cash": cash}
                        )


            # ── Playing phase ─────────────────────────────────────────────────
            elif state == "playing":
                # Tile click
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    for i in range(CELLS):
                        if not revealed[i] and cell_rect(i).collidepoint(e.pos):
                            revealed[i] = True
                            if board[i]:
                                # ── HIT MINE ─────────────────────────────────
                                state = "lost"
                                banner.show(
                                    f"💣  BOOM!  Lost ${bet:.2f}", T.LOSE_RED, 220
                                )
                                file.update_row(
                                    {"username": username, "password": password},
                                    {"cash": cash}
                                )
                            else:
                                # ── SAFE TILE ────────────────────────────────
                                safe_clicks += 1
                                gem_anims[i] = 10
                                # Auto-win if all safe tiles revealed
                                if safe_clicks == CELLS - mine_count:
                                    mult = _calc_multiplier(safe_clicks, mine_count)
                                    gain = round(bet * mult, 2)
                                    cash += gain
                                    banner.show(
                                        f"✨ Board cleared!  +${gain:.2f}", T.WIN_GREEN
                                    )
                                    file.update_row(
                                        {"username": username, "password": password},
                                        {"cash": cash}
                                    )
                                    state = "won"
                            break


                # Cash out button
                if btn_cashout.is_clicked(e) and safe_clicks > 0:
                    mult = _calc_multiplier(safe_clicks, mine_count)
                    gain = round(bet * mult, 2)
                    cash += gain
                    banner.show(f"💰 Cashed out!  +${gain:.2f}", T.GOLD)
                    file.update_row(
                        {"username": username, "password": password},
                        {"cash": cash}
                    )
                    state = "won"


            # ── End phase: click any unrevealed tile to start new round ───────
            elif state in ("lost", "won"):
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    state = "betting"


        # Tick gem animations
        for k in list(gem_anims):
            gem_anims[k] -= 1
            if gem_anims[k] <= 0:
                del gem_anims[k]


        # ── Current multiplier / profit values ────────────────────────────────
        cur_mult   = _calc_multiplier(safe_clicks, mine_count)
        cur_profit = round(bet * cur_mult, 2) if state == "playing" else 0.0
        next_mult  = _calc_multiplier(safe_clicks + 1, mine_count)
        next_profit = round(bet * next_mult, 2) if state == "playing" else 0.0


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        T.draw_logo_corner(win)
        T.draw_hud(win, cash, username)
        btn_back.draw(win)


        T.draw_text(win, "MINES", 42, T.TEXT, CX, 38, anchor="midtop", bold=True)


<<<<<<< HEAD
        # ── Left panel ────────────────────────────────────────────────────────
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, board_px)
        T.draw_rrect(win, T.PANEL, panel_rect, radius=14,
                     border=1, border_color=T.BORDER)
=======
        # board cells
        for i in range(CELLS):
            r = cell_rect(i)
            try:
                if revealed[i]:
                    if board[i]:
                        T.draw_rrect(win, (120, 30, 30), r, radius=10,
                                    border=2, border_color=T.LOSE_RED)
                        T.draw_text(win, "X", 38, T.LOSE_RED,
                                    r.centerx, r.centery, anchor="center", bold=True)
                    else:
                        T.draw_rrect(win, (25, 65, 40), r, radius=10,
                                    border=2, border_color=T.WIN_GREEN)
                        T.draw_text(win, "✓", 36, T.WIN_GREEN,
                                    r.centerx, r.centery, anchor="center", bold=True)
                else:
                    # Show mines on game-over
                    if state in ("lost", "won") and board[i]:
                        T.draw_rrect(win, (70, 25, 25), r, radius=10,
                                    border=2, border_color=T.LOSE_RED)
                        T.draw_text(win, "X", 38, T.LOSE_RED,
                                    r.centerx, r.centery, anchor="center", bold=True)
                    else:
                        T.draw_rrect(win, T.PANEL_LITE, r, radius=10,
                                    border=1, border_color=T.BORDER)
                        T.draw_text(win, "?", 32, T.TEXT_DIM,
                                    r.centerx, r.centery, anchor="center")
            except:
                pass

        # HUD strip
        hud = pygame.Rect(CX - 320, H - 150, 640, 120)
        T.draw_rrect(win, T.PANEL, hud, radius=12, border=1, border_color=T.BORDER)
>>>>>>> 023def92691d8dff122b14308ce53f6fbbed71dc


        if state == "betting":
            # Bet amount label
            T.draw_text(win, "Bet Amount", 14, T.TEXT_DIM,
                        panel_x + 16, panel_y + 14, anchor="topleft")
            bet_bar.draw(win)
<<<<<<< HEAD


            # Mine count
            T.draw_text(win, "Mines", 14, T.TEXT_DIM,
                        panel_x + 16, panel_y + 116, anchor="topleft")
            T.draw_text(win, str(mine_count), 26, T.TEXT,
                        mc_cx - 8, panel_y + 140, anchor="midleft")
            btn_minus.draw(win)
            btn_plus.draw(win)


=======
            T.draw_text(win, f"Mines: {mine_count}", 18, T.TEXT_DIM,
                        CX - 60, H - 130, anchor="midleft")
            btn_minus_m.draw(win)
            btn_plus_m.draw(win)
>>>>>>> 023def92691d8dff122b14308ce53f6fbbed71dc
            btn_start.draw(win)


            # Show starting multiplier hint
            hint_mult = _calc_multiplier(1, mine_count)
            T.draw_text(win,
                        f"First gem: x{hint_mult:.2f}",
                        13, T.TEXT_DIM,
                        panel_x + panel_w // 2, panel_y + 260,
                        anchor="midtop")


        elif state == "playing":
            # Live stats
            T.draw_text(win, "Total Profit", 13, T.TEXT_DIM,
                        panel_x + 16, panel_y + 14, anchor="topleft")
            T.draw_text(win, f"${cur_profit:.2f}", 28, T.WIN_GREEN,
                        panel_x + 16, panel_y + 32, anchor="topleft", bold=True)


            T.draw_text(win, f"x{cur_mult:.2f}", 18, T.GOLD,
                        panel_x + 16, panel_y + 70, anchor="topleft")


            T.draw_text(win, "Profit on Next Tile", 13, T.TEXT_DIM,
                        panel_x + 16, panel_y + 104, anchor="topleft")
            T.draw_text(win, f"${next_profit:.2f}", 22, T.TEXT,
                        panel_x + 16, panel_y + 122, anchor="topleft")


            T.draw_text(win, f"Mines: {mine_count}", 13, T.TEXT_DIM,
                        panel_x + 16, panel_y + 158, anchor="topleft")
            T.draw_text(win, f"Gems found: {safe_clicks}", 13, T.TEXT_DIM,
                        panel_x + 16, panel_y + 178, anchor="topleft")


            if safe_clicks > 0:
                btn_cashout.draw(win)
            else:
                T.draw_text(win, "Reveal a gem to\nenable cashout",
                            14, T.TEXT_DIM,
                            panel_x + panel_w // 2, panel_y + 210,
                            anchor="midtop")


        elif state in ("lost", "won"):
            result_col  = T.WIN_GREEN if state == "won" else T.LOSE_RED
            result_text = "YOU WON!" if state == "won" else "YOU LOST"
            T.draw_text(win, result_text, 26, result_col,
                        panel_x + panel_w // 2, panel_y + 30, anchor="midtop", bold=True)


            if state == "won":
                gain = round(bet * _calc_multiplier(safe_clicks, mine_count), 2)
                T.draw_text(win, f"+${gain:.2f}", 22, T.GOLD,
                            panel_x + panel_w // 2, panel_y + 70, anchor="midtop")


            T.draw_text(win, "Click any tile\nto play again",
                        15, T.TEXT_DIM,
                        panel_x + panel_w // 2, panel_y + 120,
                        anchor="midtop")


        # ── Board ─────────────────────────────────────────────────────────────
        for i in range(CELLS):
            r       = cell_rect(i)
            is_mine = board[i] if board else False
            hovered = r.collidepoint(mouse_pos) and state == "playing" and not revealed[i]
            anim    = i in gem_anims


            if revealed[i]:
                if is_mine:
                    # Exploded mine — red cell
                    T.draw_rrect(win, (110, 25, 25), r, radius=10,
                                 border=2, border_color=T.LOSE_RED)
                    T.draw_text(win, "💣", 34, T.LOSE_RED,
                                r.centerx, r.centery, anchor="center")
                else:
                    # Safe gem — green cell, scale-in animation
                    scale = 1.0 if not anim else (1.0 - gem_anims.get(i, 0) * 0.05)
                    cell_col = (20, 80, 45)
                    T.draw_rrect(win, cell_col, r, radius=10,
                                 border=2, border_color=T.WIN_GREEN)
                    gem_size = int(36 * max(0.5, scale))
                    T.draw_text(win, "💎", gem_size, T.WIN_GREEN,
                                r.centerx, r.centery, anchor="center")


            else:
                # End of round — reveal all mines
                if state in ("lost", "won") and is_mine:
                    mine_col = (80, 20, 20) if state == "lost" else (60, 20, 20)
                    T.draw_rrect(win, mine_col, r, radius=10,
                                 border=2, border_color=T.LOSE_RED)
                    T.draw_text(win, "💣", 30, T.LOSE_RED,
                                r.centerx, r.centery, anchor="center")
                else:
                    # Normal hidden tile
                    tile_col = T.ACCENT_DIM if hovered else T.PANEL_LITE
                    border_c = T.ACCENT    if hovered else T.BORDER
                    T.draw_rrect(win, tile_col, r, radius=10,
                                 border=1, border_color=border_c)
                    if state == "playing":
                        # Show faint diamond hint on hover
                        if hovered:
                            T.draw_text(win, "?", 28, T.TEXT,
                                        r.centerx, r.centery, anchor="center")
                        else:
                            T.draw_text(win, "·", 28, T.TEXT_DIM,
                                        r.centerx, r.centery, anchor="center")


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)
<<<<<<< HEAD

=======
if __name__=="__main__":
    pygame.init()
    file=helper_1.csv_file("data_storage.csv")
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    mines_main(win,"demo","demo",file)
>>>>>>> 023def92691d8dff122b14308ce53f6fbbed71dc
