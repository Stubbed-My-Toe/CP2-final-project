#from cards bring in all

'''-Darin's part of pseudo code-'''
# Blackjack game pseudo code
# The main function will display the options
# Options are: change bet amount, start game, return to menu

# Start with bet = 5 dollars (default)
# bet can be changed to any number between 1 and current cash

# Create a variable called deck - bjdeck = deck(False)
# The deck has all 52 cards (no jokers)
# The counting deck func: when pulling a random card, it randomly selects a card and removes it from deck (counts how many left)

# When player starts game:
    # Check if bet amount is 0. If yes, ask to change bet first.
    # Use the saved bet amount for the round.

# Deal cards:
    # Player gets two cards face up
    # Dealer gets one card face up

# Check if player's hand value equals 21:
    # If yes, player wins automatically (blackjack) and gets 2x bet

# Player turn:
    # Options: HIT or STAND
    # If player hits, draw a random card from deck and add to player's hand face up
    # If player stands, they don't draw any more cards
    # After each hit, check:
        # If hand value is exactly 21, player wins (stop)
        # If hand value is over 21, player busts and loses (stop)

# Dealer turn (happens after player stands or wins, but not if player busted):
    # Dealer draws cards for however many times the player hit
    # But even if player didn't hit at all (0 hits), dealer still draws at least one card
    # Dealer must keep drawing until their hand value is at least 17 (simple rule)
    # If dealer goes over 21, dealer busts and player wins

# Determine winner:
    # Player wins if:
        # Player has blackjack (21 on first two cards)
        # Player's hand value is greater than dealer's hand value (both under 22)
        # Dealer busts
    # Player loses if:
        # Player busts
        # Dealer's hand value is greater than player's (both under 22)
    # Push (tie) if both have same value

# Winnings calculation:
    # Win = get back bet amount x2 (so net profit of bet amount)
    # Loss = lose the bet amount
    # Push = get bet amount back (no change)

# After round ends:
    # Update cash
    # Return to main menu
    # Player can change bet again or start a new game
import pygame
from cards import Deck, hand_total, short_name
import helper
import time
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 180, 0)
RED    = (200, 50, 50)
GRAY   = (100, 100, 100)
YELLOW = (220, 200, 50)
DARK   = (30, 30, 30)
BTNBG  = (60, 60, 60)

# window
WIDTH = 1080
HEIGHT = 1080



class Game:
    def __init__(self,file:helper.csv_file,username,password):
        self.data=helper.csv_get_data(file,{"username":username,"password":password})
        self.cash = int(self.data["cash"])
        self.bet = 5
        self.state = "menu"  # menu, playing, result
        self.player = []
        self.dealer = []
        self.deck = None
        self.message = ""

    def new_round(self):
        self.deck = Deck()
        self.player = [self.deck.draw(), self.deck.draw()]
        self.dealer = [self.deck.draw()]
        self.message = ""
        self.state = "playing"

        # instant blackjack
        if hand_total(self.player) == 21:
            self.end_round("blackjack")

    def hit(self):
        self.player.append(self.deck.draw())
        total = hand_total(self.player)
        if total > 21:
            self.end_round("bust")
        elif total == 21:
            self.dealer_turn()

    def stand(self):
        self.dealer_turn()

    def dealer_turn(self):
        player_total = hand_total(self.player)

        # dealer hits until they meet or beat the player's total
        while hand_total(self.dealer) < player_total:
            self.dealer.append(self.deck.draw())

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
            self.message = "Busted! -$" + str(self.bet)
        elif reason == "blackjack":
            self.cash += self.bet * 2
            self.message = "BLACKJACK!! +$" + str(self.bet * 2)
        elif reason == "dealer_bust":
            self.cash += self.bet
            self.message = "Dealer busted! +$" + str(self.bet)
        elif reason == "compare":
            if p > d:
                self.cash += self.bet
                self.message = "You win! (" + str(p) + " vs " + str(d) + ")  +$" + str(self.bet)
            elif d > p:
                self.cash -= self.bet
                self.message = "Dealer wins. (" + str(d) + " vs " + str(p) + ")  -$" + str(self.bet)
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
    def max(self):
        self.bet = self.cash

# helper to draw text
def write(text, f, color, x, y,screen):
    screen.blit(f.render(text, True, color), (x, y))


# draws a button and returns the rect so we can click-check it
def button(text, x, y,screen, w=120, h=38, color=BTNBG):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=4)
    pygame.draw.rect(screen, GRAY, rect, 2, border_radius=4)
    label = font_med.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return rect
def bj_main(screen,username,password,file:helper.csv_file):
    delay=0
    global font_big
    global font_med
    global font_small
    font_big   = pygame.font.SysFont("Arial", 28, bold=True)
    font_med   = pygame.font.SysFont("Arial", 20)
    font_small = pygame.font.SysFont("Arial", 16)
    data=file
    pygame.display.set_caption("Blackjack")
    clock = pygame.time.Clock()

    tic=0
    
    game = Game(file,username,password)
    running = True

    while running:
        screen.fill(DARK)

        # top bar
        write("BLACKJACK", font_big, WHITE, 20, 15,screen)
        write("Cash: $" + str(game.cash), font_med, GREEN, 20, 55,screen)
        write("Bet: $" + str(game.bet), font_med, YELLOW, 210, 55,screen)

        # buttons we might draw this frame (set to None if not shown)
        btn_deal     = None
        btn_hit      = None
        btn_stand    = None
        btn_bet_up   = None
        btn_bet_down = None

        if game.state in ("menu", "result"):
            btn_deal     = button("DEAL", 20, 100,screen, 120, 38, (0, 120, 0))
            btn_bet_up   = button("+$5",  350, 48,screen, 80, 32)
            allin   = button("ALL IN",  620, 48,screen, 80, 32)
            btn_bet_down = button("-$5",  440, 48,screen, 80, 32)
            returner= button("return",530,48,screen,80,32)

        if game.state in ("playing", "result"):
            # dealer hand
            write("Dealer:  " + game.hand_str(game.dealer), font_med, WHITE, 20, 150,screen)
            dval = hand_total(game.dealer)
            dcol = RED if dval > 21 else WHITE
            write("Total: " + str(dval), font_small, dcol, 20, 178,screen)

            # player hand
            write("You:     " + game.hand_str(game.player), font_med, WHITE, 20, 225,screen)
            pval = hand_total(game.player)
            pcol = RED if pval > 21 else (GREEN if pval == 21 else WHITE)
            write("Total: " + str(pval), font_small, pcol, 20, 253,screen)

            write("Cards left: " + str(game.deck.cards_left()), font_small, GRAY, 20, 415,screen)

        if game.state == "playing":
            btn_hit   = button("HIT",   20,  300,screen, 100, 38)
            btn_stand = button("STAND", 130, 300,screen, 100, 38)

        if game.state == "result":
            if "+" in game.message:
                mcol = GREEN
            elif "-" in game.message:
                mcol = RED
            else:
                mcol = YELLOW
            write(game.message, font_small, mcol, 20, 310,screen)

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if btn_deal and btn_deal.collidepoint(mx, my):
                    game.new_round()
                if btn_hit and btn_hit.collidepoint(mx, my):
                    game.hit()
                if btn_stand and btn_stand.collidepoint(mx, my):
                    game.stand()
                if allin and allin.collidepoint(mx,my):
                    game.max()
                if returner and returner.collidepoint(mx,my):
                    stats = game.data 
                    file.update_row(
                        {"username": username, "password": password},
                        {
                            "cash": game.cash,
                            "times_played_blackjack": int(stats["times_played_blackjack"]) + 1,
                            "times_played_dice": stats["times_played_dice"],
                            "times_played_plinko": stats["times_played_plinko"],
                            "times_played_slots": stats["times_played_slots"],
                        }
                    )
                    return
                
        if pygame.mouse.get_pressed()[0] and tic<0:
            tic=max(5-(max(delay,8))/20,0)
            mx, my = pygame.mouse.get_pos()
            if btn_bet_up and btn_bet_up.collidepoint(mx, my):
                if delay>250:
                    game.change_bet(5)
                game.change_bet(5)
                delay+=1
                print(tic,delay)
            if btn_bet_down and btn_bet_down.collidepoint(mx, my):
                if delay>250:
                    game.change_bet(-5)
                game.change_bet(-5)
                delay+=1
        elif not(pygame.mouse.get_pressed()[0]):
            delay=0
        tic-=1
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

        
if __name__=="__main__":
    pygame.init()
    pygame.mixer.init(0)
    win=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    file=helper.csv_file("data_storage.csv")
    bj_main(win,"test","<NULL>",file)