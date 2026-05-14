# main.py — Cleek Casino  (entry point)
import sys
import pygame
import math


import helper_1
import auth_1
import theme_1 as T
import Blackjack_3
import Dice_1
import slots_1
import mines_1
import plinko_1


# ─── Game catalog ──────────────────────────────────────────────────────────────
GAMES = [
    {
        "name":    "Blackjack",
        "icon":    "♠",
        "desc":    "Beat the dealer to 21",
        "call":    Blackjack_3.blackjack_main,
        "color":   T.ACCENT,
    },
    {
        "name":    "Dice",
        "icon":    "⬡",
        "desc":    "Over / Under 0–100",
        "call":    Dice_1.dice_main,
        "color":   (100, 160, 240),
    },
    {
        "name":    "Slots",
        "icon":    "7",
        "desc":    "Match the centre row",
        "call":    slots_1.slots_main,
        "color":   T.GOLD,
    },
    {
        "name":    "Mines",
        "icon":    "✕",
        "desc":    "Dodge the mines — cash out",
        "call":    mines_1.mines_main,
        "color":   T.LOSE_RED,
    },
    {
        "name":    "Plinko",
        "icon":    "◉",
        "desc":    "Drop a chip — win big",
        "call":    plinko_1.plinko_main,
        "color":   T.ACCENT_DIM,
    },
]


CARD_W, CARD_H = 220, 280
CARD_GAP = 28




def _card_rect(i, n, cx, cy):
    total = n * CARD_W + (n - 1) * CARD_GAP
    x = cx - total // 2 + i * (CARD_W + CARD_GAP)
    return pygame.Rect(x, cy - CARD_H // 2, CARD_W, CARD_H)




def _hovered_card(pos, n, cx, cy):
    for i in range(n):
        if _card_rect(i, n, cx, cy).collidepoint(pos):
            return i
    return -1




def main_menu(win, data, csv_file):
    W, H  = win.get_size()
    CX    = W // 2
    cy    = H // 2 + 20


    btn_quit = T.Button("Sign Out", (W - 160, H - 52, 130, 38),
                        color=T.PANEL_LITE, hover_color=T.LOSE_RED,
                        hover_text=T.WHITE, font_size=15)
    banner = T.Banner()


    hover_idx = -1
    hover_lift = [0.0] * len(GAMES)   # vertical lift animation per card


    clock = pygame.time.Clock()
    running = True
    while running:
        cash = float(helper_1.csv_get_data(csv_file,
                    {"username": data["username"],
                     "password": data["password"]})["cash"])


        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if btn_quit.is_clicked(e):
                return "logout"


            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                idx = _hovered_card(pos, len(GAMES), CX, cy)
                if idx >= 0:
                    game = GAMES[idx]
                    game["call"](win, data["username"], data["password"], csv_file)
                    # refresh data after returning
                    data = helper_1.csv_get_data(csv_file,
                               {"username": data["username"],
                                "password": data["password"]})


        # ── Hover animation ───────────────────────────────────────────────────
        mx, my = pygame.mouse.get_pos()
        hover_idx = _hovered_card((mx, my), len(GAMES), CX, cy)
        for i in range(len(GAMES)):
            target = 18.0 if i == hover_idx else 0.0
            hover_lift[i] += (target - hover_lift[i]) * 0.14


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        # animated diagonal grid
        t = pygame.time.get_ticks() / 5000
        for k in range(-H, W + H, 64):
            alpha = 18
            pygame.draw.line(win, (20, 25, 30), (k, 0), (k + H, H), 1)


        T.draw_logo_corner(win)
        T.draw_hud(win, cash, data["username"])
        btn_quit.draw(win)


        # headline
        T.draw_text(win, "Choose a Game", 38, T.TEXT, CX, 68, anchor="midtop", bold=True)
        T.draw_text(win, "Your balance carries across all games", 17, T.TEXT_DIM,
                    CX, 116, anchor="midtop")


        # game cards
        for i, game in enumerate(GAMES):
            lift = int(hover_lift[i])
            r    = _card_rect(i, len(GAMES), CX, cy)
            r.y -= lift


            hov  = (i == hover_idx)
            bg   = T.PANEL_LITE if not hov else T.PANEL
            border_col = game["color"] if hov else T.BORDER


            T.draw_rrect(win, bg, r, radius=16, border=2, border_color=border_col)


            # glow on hover
            if hov:
                glow = pygame.Surface((CARD_W + 20, CARD_H + 20), pygame.SRCALPHA)
                gc   = game["color"]
                pygame.draw.rect(glow, (*gc, 25),
                                 (0, 0, CARD_W + 20, CARD_H + 20), border_radius=20)
                win.blit(glow, (r.x - 10, r.y - 10))


            # big icon
            T.draw_text(win, game["icon"], 72, game["color"],
                        r.centerx, r.y + 70, anchor="midtop")


            # name
            T.draw_text(win, game["name"], 24, T.TEXT,
                        r.centerx, r.y + 160, anchor="midtop", bold=True)


            # description
            T.draw_text(win, game["desc"], 14, T.TEXT_DIM,
                        r.centerx, r.y + 194, anchor="midtop")


            # play button
            pb = pygame.Rect(r.x + 20, r.bottom - 50, CARD_W - 40, 36)
            col = game["color"] if hov else T.BORDER
            T.draw_rrect(win, col if hov else T.PANEL, pb, radius=8,
                         border=1, border_color=col)
            T.draw_text(win, "Play", 15, T.BG if hov else T.TEXT_DIM,
                        pb.centerx, pb.centery, anchor="center", bold=hov)


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)




def main():
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Cleek Casino")


    csv_file = helper_1.csv_file("data_storage.csv")


    while True:
        data = auth_1.login_screen(win, csv_file)
        if data is None:
            break


        result = main_menu(win, data, csv_file)
        if result == "logout":
            continue
        break


    pygame.quit()
    sys.exit()




if __name__ == "__main__":
    main()
