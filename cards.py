# ...existing code...
import random
import trandom
class Deck:
    def __init__(self):
        self.rand=trandom.alternate_random(1,100000000)
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        random.seed(next(self.rand))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def cards_left(self):
        return len(self.cards)


def get_value(card):
    rank = card.split(" of ")[0]
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11
    return int(rank)


def hand_total(hand):
    total = 0
    aces = 0
    for c in hand:
        total += get_value(c)
        if c.split(" of ")[0] == "A":
            aces += 1
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def short_name(card):
    rank, suit = card.split(" of ")
    symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
    return rank + symbols.get(suit, "?")
# ...existing code...
