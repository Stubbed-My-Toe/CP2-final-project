import pygame
import random
import helper_1
import theme_1 as T


# ─── Card drawing ─────────────────────────────────────────────────────────────
SUITS  = ["♠", "♥", "♦", "♣"]
RANKS  = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_W, CARD_H = 72, 104
CARD_GAP = 14


RED_SUITS = {"♥", "♦"}




def card_value(rank):
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11
    return int(rank)




def hand_total(hand):
    total = sum(card_value(r) for r, s in hand)
    aces  = sum(1 for r, s in hand if r == "A")
    while total > 21 and aces:
        total -= 10
        aces  -= 1
    return total




def new_deck():
    deck = [(r, s) for r in RANKS for s in SUITS] * 6
    random.shuffle(deck)
    return deck




def draw_card(surface, rank, suit, cx, cy, face_up=True):
    """Draw a single card centred at (cx, cy)."""
    rect = pygame.Rect(cx - CARD_W // 2, cy - CARD_H // 2, CARD_W, CARD_H)
    if not face_up:
        T.draw_rrect(surface, (30, 50, 80), rect, radius=8,
                     border=1, border_color=T.BORDER)
        # cross-hatch back
        for i in range(0, CARD_W, 10):
            pygame.draw.line(surface, (40, 60, 90),
                             (rect.x + i, rect.y), (rect.x, rect.y + i), 1)
        return


    bg = T.WHITE
    T.draw_rrect(surface, bg, rect, radius=8, border=1, border_color=(180, 180, 180))
    col = (200, 30, 30) if suit in RED_SUITS else (20, 20, 20)
    rf  = T.font(15, bold=True)
    # top-left rank + suit
    surface.blit(rf.render(rank, True, col), (rect.x + 4, rect.y + 4))
    surface.blit(rf.render(suit, True, col), (rect.x + 4, rect.y + 18))
    # centre suit
    sf = T.font(34)
    ss = sf.render(suit, True, col)
    surface.blit(ss, ss.get_rect(center=rect.center))




def draw_hand(surface, hand, cx, baseline_y, face_down_idx=None):
    """Draw a row of cards centred at cx."""
    n   = len(hand)
    total_w = n * CARD_W + (n - 1) * CARD_GAP
    start_x = cx - total_w // 2 + CARD_W // 2
    for i, (rank, suit) in enumerate(hand):
        face_up = (face_down_idx is None) or (i != face_down_idx)
        draw_card(surface, rank, suit, start_x + i * (CARD_W + CARD_GAP),
                  baseline_y, face_up=face_up)




# ─── Game states ──────────────────────────────────────────────────────────────
BETTING   = "betting"
PLAYING   = "playing"
DEALER    = "dealer"
RESULT    = "result"




def blackjack_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data  = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash  = float(data["cash"])


    CX = W // 2


    bet_bar   = T.BetBar(CX, H - 100, min_bet=1, default=10, step=5)
    btn_deal  = T.Button("Deal",  (CX - 240, H - 100, 110, 44),
                         color=T.ACCENT, hover_color=T.ACCENT_DIM,
                         text_color=T.BG, hover_text=T.BG, bold=True)
    btn_hit   = T.Button("Hit",   (CX - 60, H - 100, 110, 44),
                         color=T.PANEL_LITE, bold=True)
    btn_stand = T.Button("Stand", (CX + 60, H - 100, 110, 44),
                         color=T.PANEL_LITE, bold=True)
    btn_again = T.Button("Play Again", (CX - 60, H - 100, 130, 44),
                         color=T.ACCENT, hover_color=T.ACCENT_DIM,
                         text_color=T.BG, bold=True)
    btn_back  = T.make_back_button()
    banner    = T.Banner()


    deck         = new_deck()
    player_hand  = []
    dealer_hand  = []
    bet          = 0
    state        = BETTING
    result_msg   = ""
    result_color = T.TEXT


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
                     "times_played_blackjack": int(data["times_played_blackjack"]) + 1}
                )
                return


            # ── Betting phase ─────────────────────────────────────────────────
            if state == BETTING:
                bet_bar.handle(e, cash)
                if btn_deal.is_clicked(e):
                    bet = bet_bar.value
                    if bet > cash:
                        banner.show("Insufficient funds", T.LOSE_RED)
                    elif bet <= 0:
                        banner.show("Place a bet first", T.TEXT_DIM)
                    else:
                        cash -= bet
                        if len(deck) < 20:
                            deck = new_deck()
                        player_hand = [deck.pop(), deck.pop()]
                        dealer_hand = [deck.pop(), deck.pop()]
                        state = PLAYING
                        # Blackjack instant win check
                        if hand_total(player_hand) == 21:
                            state = DEALER  # show dealer then resolve


            # ── Playing phase ─────────────────────────────────────────────────
            elif state == PLAYING:
                if btn_hit.is_clicked(e):
                    player_hand.append(deck.pop())
                    if hand_total(player_hand) > 21:
                        result_msg   = "Bust!  Dealer wins."
                        result_color = T.LOSE_RED
                        state = RESULT
                    elif hand_total(player_hand) == 21:
                        state = DEALER


                if btn_stand.is_clicked(e):
                    state = DEALER


            # ── Result phase ──────────────────────────────────────────────────
            elif state == RESULT:
                if btn_again.is_clicked(e):
                    state = BETTING


        # ── Dealer auto-draw ──────────────────────────────────────────────────
        if state == DEALER:
            while hand_total(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            pt = hand_total(player_hand)
            dt = hand_total(dealer_hand)
            if pt > 21:
                result_msg   = "Bust!  Dealer wins."
                result_color = T.LOSE_RED
            elif dt > 21 or pt > dt:
                gain = round(bet * 2, 2)
                cash += gain
                result_msg   = f"You win! +${gain:.2f}"
                result_color = T.WIN_GREEN
            elif pt == dt:
                cash += bet   # push
                result_msg   = "Push — bet returned."
                result_color = T.GOLD
            else:
                result_msg   = f"Dealer wins.  -{bet:.2f}"
                result_color = T.LOSE_RED
            banner.show(result_msg, result_color)
            file.update_row(
                {"username": username, "password": password},
                {"cash": cash}
            )
            state = RESULT


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        # felt-ish green table area
        table = pygame.Rect(80, 120, W - 160, H - 240)
        T.draw_rrect(win, (12, 36, 24), table, radius=20, border=2, border_color=(20, 55, 35))


        T.draw_logo_corner(win)
        T.draw_hud(win, cash, username)
        btn_back.draw(win)


        T.draw_text(win, "BLACKJACK", 44, T.TEXT, CX, 44, anchor="midtop", bold=True)


        # ── Dealer cards ──────────────────────────────────────────────────────
        DEALER_Y = 230
        PLAYER_Y = H - 290


        # Show dealer's hole card face-down while player is still playing
        hide_idx = 1 if state in (PLAYING, BETTING) else None
        draw_hand(win, dealer_hand, CX, DEALER_Y, face_down_idx=hide_idx)


        # Dealer total — only show visible card total while playing
        if dealer_hand:
            if state in (PLAYING,):
                vis_total = card_value(dealer_hand[0][0])
                T.draw_text(win, f"Dealer: {vis_total}", 22, T.TEXT_DIM,
                            CX, DEALER_Y - CARD_H // 2 - 30, anchor="midbottom", bold=True)
            elif state in (DEALER, RESULT):
                dt = hand_total(dealer_hand)
                col = T.LOSE_RED if dt > 21 else T.TEXT
                T.draw_text(win, f"Dealer: {dt}", 22, col,
                            CX, DEALER_Y - CARD_H // 2 - 30, anchor="midbottom", bold=True)


        # ── Player cards ──────────────────────────────────────────────────────
        draw_hand(win, player_hand, CX, PLAYER_Y)


        if player_hand:
            pt = hand_total(player_hand)
            pc = T.LOSE_RED if pt > 21 else T.WIN_GREEN if pt == 21 else T.TEXT
            T.draw_text(win, f"You: {pt}", 26, pc,
                        CX, PLAYER_Y + CARD_H // 2 + 14, anchor="midtop", bold=True)


        # ── Phase-specific buttons ─────────────────────────────────────────────
        # Always draw HUD panel above buttons
        hud2 = pygame.Rect(CX - 280, H - 120, 560, 66)
        T.draw_rrect(win, T.PANEL, hud2, radius=10, border=1, border_color=T.BORDER)


        if state == BETTING:
            bet_bar.draw(win)
            btn_deal.draw(win)
        elif state == PLAYING:
            T.draw_text(win, f"Bet: ${bet:.2f}", 20, T.GOLD,
                        CX - 170, H - 80, anchor="midleft")
            btn_hit.draw(win)
            btn_stand.draw(win)
        elif state == RESULT:
            T.draw_text(win, result_msg, 24, result_color,
                        CX, H - 80, anchor="center", bold=True)
            btn_again.draw(win)


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)