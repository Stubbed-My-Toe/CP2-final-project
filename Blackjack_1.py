# ...existing code...
import pygame
import sys
from Countcards import Deck, hand_total, short_name

pygame.init()

# window
WIDTH, HEIGHT = 1080, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# colors & fonts
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 180, 0)
RED    = (200, 50, 50)
GRAY   = (100, 100, 100)
YELLOW = (220, 200, 50)
DARK   = (30, 30, 30)
BTNBG  = (60, 60, 60)

font_big   = pygame.font.SysFont("Arial", 28, bold=True)
font_med   = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 16)
anim_font  = pygame.font.SysFont("Arial", 20, bold=True)

# card visual size (vertical)
CARD_W, CARD_H = 90, 140
CARD_SPACING_X = 130
BASE_X = 40
DEALER_Y = 150
PLAYER_Y = 225


class Game:
    def __init__(self):
        self.cash = 25
        self.bet = 5
        self.state = "menu"  # menu, playing, result
        self.player = []
        self.dealer = []
        self.deck = None
        self.message = ""

    def new_round(self):
        self.deck = Deck()
        self.player = []
        self.dealer = []
        # player card 1
        c = self.deck.draw()
        if c:
            animate_card_pygame(short_name(c), end_pos=(BASE_X, PLAYER_Y))
            self.player = [c]
        # player card 2
        c = self.deck.draw()
        if c:
            animate_card_pygame(short_name(c), end_pos=(BASE_X + CARD_SPACING_X, PLAYER_Y))
            self.player.append(c)
        # dealer card 1
        c = self.deck.draw()
        if c:
            animate_card_pygame(short_name(c), end_pos=(BASE_X, DEALER_Y))
            self.dealer = [c]
        self.message = ""
        self.state = "playing"
        if hand_total(self.player) == 21:
            self.end_round("blackjack")

    def hit(self):
        c = self.deck.draw()
        if not c:
            return
        pos_x = BASE_X + CARD_SPACING_X * (len(self.player))
        animate_card_pygame(short_name(c), end_pos=(pos_x, PLAYER_Y))
        self.player.append(c)
        total = hand_total(self.player)
        if total > 21:
            self.end_round("bust")
        elif total == 21:
            self.dealer_turn()

    def stand(self):
        self.dealer_turn()

    def dealer_turn(self):
        player_total = hand_total(self.player)
        while hand_total(self.dealer) < player_total:
            c = self.deck.draw()
            if not c:
                break
            pos_x = BASE_X + CARD_SPACING_X * (len(self.dealer))
            animate_card_pygame(short_name(c), end_pos=(pos_x, DEALER_Y))
            self.dealer.append(c)
        if hand_total(self.dealer) > 21:
            self.end_round("dealer_bust")
        else:
            self.end_round("compare")

    def end_round(self, reason):
        self.state = "result"
        p = hand_total(self.player)
        d = hand_total(self.dealer)
        if reason == "bust":
            self.cash -= self.bet
            self.message = f"Busted! -${self.bet}"
        elif reason == "blackjack":
            self.cash += self.bet * 2
            self.message = f"BLACKJACK!! +${self.bet * 2}"
        elif reason == "dealer_bust":
            self.cash += self.bet
            self.message = f"Dealer busted! +${self.bet}"
        elif reason == "compare":
            if p > d:
                self.cash += self.bet
                self.message = f"You win! ({p} vs {d})  +${self.bet}"
            elif d > p:
                self.cash -= self.bet
                self.message = f"Dealer wins. ({d} vs {p})  -${self.bet}"
            else:
                self.message = "Tie! No change."
        if self.cash <= 0:
            self.cash = 200
            self.message += "  | Broke! Reset to $200"

    def change_bet(self, amount):
        new_bet = self.bet + amount
        if 1 <= new_bet <= self.cash:
            self.bet = new_bet

    def hand_str(self, hand):
        return "  ".join(short_name(c) for c in hand)


def write(text, f, color, x, y):
    screen.blit(f.render(text, True, color), (x, y))


def button(text, x, y, w=120, h=38, color=BTNBG):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=4)
    pygame.draw.rect(screen, GRAY, rect, 2, border_radius=4)
    label = font_med.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return rect


def pump_events_allow_quit():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # keep other events in main loop by ignoring them here


def draw_hud(g):
    write("BLACKJACK", font_big, WHITE, 20, 15)
    write("Cash: $" + str(g.cash), font_med, GREEN, 20, 55)
    write("Bet: $" + str(g.bet), font_med, YELLOW, 210, 55)
    if g.state in ("playing", "result"):
        write("Dealer:", font_med, WHITE, 20, DEALER_Y)
        dval = hand_total(g.dealer)
        dcol = RED if dval > 21 else WHITE
        write("Total: " + str(dval), font_small, dcol, 20, DEALER_Y + CARD_H + 8)
        write("You:", font_med, WHITE, 20, PLAYER_Y)
        pval = hand_total(g.player)
        pcol = RED if pval > 21 else (GREEN if pval == 21 else WHITE)
        write("Total: " + str(pval), font_small, pcol, 20, PLAYER_Y + CARD_H + 8)
        if g.deck:
            write("Cards left: " + str(g.deck.cards_left()), font_small, GRAY, 20, PLAYER_Y + CARD_H + 40)


def draw_cards(g):
    """Draw card rectangles and labels for dealer and player."""
    # dealer
    for idx, card in enumerate(g.dealer):
        rx = BASE_X + CARD_SPACING_X * idx
        ry = DEALER_Y
        r = pygame.Rect(rx, ry, CARD_W, CARD_H)
        pygame.draw.rect(screen, WHITE, r, border_radius=8)
        pygame.draw.rect(screen, GRAY, r, 2, border_radius=8)
        lbl = anim_font.render(short_name(card), True, BLACK)
        screen.blit(lbl, (r.x + 8, r.y + 8))
    # player
    for idx, card in enumerate(g.player):
        rx = BASE_X + CARD_SPACING_X * idx
        ry = PLAYER_Y
        r = pygame.Rect(rx, ry, CARD_W, CARD_H)
        pygame.draw.rect(screen, WHITE, r, border_radius=8)
        pygame.draw.rect(screen, GRAY, r, 2, border_radius=8)
        lbl = anim_font.render(short_name(card), True, BLACK)
        screen.blit(lbl, (r.x + 8, r.y + 8))


def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)


def animate_card_pygame(card_text, start_pos=(-250, 200), end_pos=(40, 250), duration_ms=420):
    """Smooth time-based slide with ease-out. Keeps window responsive and shows other cards."""
    start = pygame.Vector2(start_pos)
    end = pygame.Vector2(end_pos)
    start_time = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        t = min(1.0, elapsed / max(1, duration_ms))
        eased = ease_out_cubic(t)
        pos = start.lerp(end, eased)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK)
        draw_hud(game)
        # draw existing cards (the new card is NOT appended yet, so it won't be shown in draw_cards)
        draw_cards(game)

        # draw animated card on top
        rect = pygame.Rect(int(pos.x), int(pos.y), CARD_W, CARD_H)
        pygame.draw.rect(screen, WHITE, rect, border_radius=8)
        pygame.draw.rect(screen, GRAY, rect, 2, border_radius=8)
        lbl = anim_font.render(card_text, True, BLACK)
        screen.blit(lbl, (rect.x + 8, rect.y + 8))

        pygame.display.flip()
        clock.tick(60)

        if t >= 1.0:
            break


# main loop
game = Game()
running = True
while running:
    screen.fill(DARK)
    # top HUD
    write("BLACKJACK", font_big, WHITE, 20, 15)
    write("Cash: $" + str(game.cash), font_med, GREEN, 20, 55)
    write("Bet: $" + str(game.bet), font_med, YELLOW, 210, 55)

    btn_deal = btn_hit = btn_stand = btn_bet_up = btn_bet_down = None

    if game.state in ("menu", "result"):
        btn_deal     = button("DEAL", 20, 100, 120, 38, (0, 120, 0))
        btn_bet_up   = button("+$5",  350, 48, 80, 32)
        btn_bet_down = button("-$5",  440, 48, 80, 32)

    if game.state in ("playing", "result"):
        draw_hud(game)
        draw_cards(game)

    if game.state == "playing":
        btn_hit   = button("HIT",   20,  400, 100, 38)
        btn_stand = button("STAND", 130, 400, 100, 38)

    if game.state == "result":
        if "+" in game.message:
            mcol = GREEN
        elif "-" in game.message:
            mcol = RED
        else:
            mcol = YELLOW
        write(game.message, font_small, mcol, 20, 450)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if btn_deal and btn_deal.collidepoint(mx, my):
                game.new_round()
            if btn_bet_up and btn_bet_up.collidepoint(mx, my):
                game.change_bet(5)
            if btn_bet_down and btn_bet_down.collidepoint(mx, my):
                game.change_bet(-5)
            if btn_hit and btn_hit.collidepoint(mx, my):
                game.hit()
            if btn_stand and btn_stand.collidepoint(mx, my):
                game.stand()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
