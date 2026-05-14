import pygame
import random
import math
import helper_1
import theme_1 as T


GRID  = 5
CELLS = GRID * GRID
CELL_SIZE = 90
PAD_BOARD = 16




def _calc_multiplier(safe_clicked, mines):
    """Fair odds: probability of not hitting any mine after k safe picks."""
    safe_total = CELLS - mines
    prob = 1.0
    for i in range(safe_clicked):
        remaining = CELLS - i
        safe_left  = safe_total - i
        if remaining <= 0 or safe_left <= 0:
            return 0.0
        prob *= safe_left / remaining
    if prob <= 0:
        return 0.0
    return round(0.97 / prob, 3)   # 3 % house edge




def mines_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data  = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash  = float(data["cash"])


    CX = W // 2
    board_px = GRID * CELL_SIZE + (GRID - 1) * PAD_BOARD
    board_x  = CX - board_px // 2
    board_y  = H // 2 - board_px // 2 - 20


    bet_bar    = T.BetBar(CX, H - 120, min_bet=1, default=10, step=5)
    mine_slider_val = [3]   # mutable box
    btn_plus_m  = T.Button("+", (CX + 130, H - 120, 36, 36), font_size=18)
    btn_minus_m = T.Button("−", (CX + 88,  H - 120, 36, 36), font_size=18)


    btn_start   = T.Button("Start Game", (CX - 80, H - 68, 160, 44),
                           color=T.ACCENT, hover_color=T.ACCENT_DIM,
                           text_color=T.BG, hover_text=T.BG, bold=True)
    btn_cashout = T.Button("Cash Out",   (CX - 90, H - 68, 170, 44),
                           color=T.WIN_GREEN, hover_color=(60, 180, 100),
                           text_color=T.BG, hover_text=T.BG, bold=True)
    btn_reset   = T.Button("New Round",  (CX + 90, H - 68, 140, 44),
                           color=T.PANEL_LITE)
    btn_back    = T.make_back_button()
    banner      = T.Banner()


    # ── Game state ──────────────────────────────────────────────────────────
    state      = "betting"   # "playing" | "lost" | "won"
    board      = []          # True = mine
    revealed   = []          # True = clicked
    safe_clicks = 0
    bet        = 0
    mine_count = 3


    def reset_board(mines):
        b = [False] * CELLS
        for idx in random.sample(range(CELLS), mines):
            b[idx] = True
        return b


    def cell_rect(idx):
        col = idx % GRID
        row = idx // GRID
        x = board_x + col * (CELL_SIZE + PAD_BOARD)
        y = board_y + row * (CELL_SIZE + PAD_BOARD)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)


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
                     "times_played_mines": int(data.get("times_played_mines", 0)) + 1}
                )
                return


            if state == "betting":
                bet_bar.handle(e, cash)
                if btn_plus_m.is_clicked(e):
                    mine_count = min(24, mine_count + 1)
                if btn_minus_m.is_clicked(e):
                    mine_count = max(1, mine_count - 1)


                if btn_start.is_clicked(e):
                    bet = bet_bar.value
                    if bet > cash:
                        banner.show("Insufficient funds", T.LOSE_RED)
                    else:
                        cash    -= bet
                        board    = reset_board(mine_count)
                        revealed = [False] * CELLS
                        safe_clicks = 0
                        state    = "playing"


            elif state == "playing":
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    pos = e.pos
                    for i in range(CELLS):
                        if not revealed[i] and cell_rect(i).collidepoint(pos):
                            revealed[i] = True
                            if board[i]:
                                # Hit a mine
                                state = "lost"
                                banner.show(f"BOOM!  Lost ${bet:.2f}", T.LOSE_RED, 200)
                                file.update_row(
                                    {"username": username, "password": password},
                                    {"cash": cash}
                                )
                            else:
                                safe_clicks += 1
                                if safe_clicks == CELLS - mine_count:
                                    mult = _calc_multiplier(safe_clicks, mine_count)
                                    gain = round(bet * mult, 2)
                                    cash += gain
                                    banner.show(f"Board cleared!  +${gain:.2f}", T.WIN_GREEN)
                                    file.update_row(
                                        {"username": username, "password": password},
                                        {"cash": cash}
                                    )
                                    state = "won"
                            break


                if btn_cashout.is_clicked(e) and safe_clicks > 0:
                    mult = _calc_multiplier(safe_clicks, mine_count)
                    gain = round(bet * mult, 2)
                    cash += gain
                    banner.show(f"Cashed out!  +${gain:.2f}", T.GOLD)
                    file.update_row(
                        {"username": username, "password": password},
                        {"cash": cash}
                    )
                    state = "won"


            elif state in ("lost", "won"):
                if btn_reset.is_clicked(e):
                    state = "betting"


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        T.draw_logo_corner(win)
        T.draw_hud(win, cash, username)
        btn_back.draw(win)


        T.draw_text(win, "MINES", 48, T.TEXT, CX, 50, anchor="midtop", bold=True)


        # board cells
        for i in range(CELLS):
            r = cell_rect(i)
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


        # HUD strip
        hud = pygame.Rect(CX - 320, H - 150, 640, 120)
        T.draw_rrect(win, T.PANEL, hud, radius=12, border=1, border_color=T.BORDER)


        if state == "betting":
            bet_bar.draw(win)
            T.draw_text(win, f"Mines: {mine_count}", 18, T.TEXT_DIM,
                        CX + 60, H - 120, anchor="midleft")
            btn_minus_m.draw(win)
            btn_plus_m.draw(win)
            btn_start.draw(win)


        elif state == "playing":
            mult = _calc_multiplier(safe_clicks, mine_count)
            gain = round(bet * mult, 2)
            T.draw_text(win, f"Bet: ${bet:.2f}   Safe: {safe_clicks}   Next cashout: ${gain:.2f}",
                        18, T.TEXT, CX, H - 120, anchor="midtop")
            btn_cashout.draw(win)


        elif state in ("lost", "won"):
            T.draw_text(win, "Round over", 22, T.TEXT_DIM, CX, H - 115, anchor="midtop")
            btn_reset.draw(win)


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)
