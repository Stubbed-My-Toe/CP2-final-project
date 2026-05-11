#Darin
#function cards
    #deck has 52 cards
    #card types have 4 types hearts, spades, clubs, dimonds
    

import random


# this makes the deck and does all the card math stuff


class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(rank + " of " + suit)
        random.shuffle(self.cards)


    # picks a random card and removes it so we dont get duplicates
    def draw(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card


    def cards_left(self):
        return len(self.cards)




# returns the blackjack value of one card
def get_value(card):
    rank = card.split(" of ")[0]
    if rank in ["J", "Q", "K"]:
        return 10
    elif rank == "A":
        return 11  # ace starts as 11, we fix it later if we bust
    else:
        return int(rank)




# adds up all the cards in a hand
def hand_total(hand):
    total = 0
    aces = 0
    for card in hand:
        total += get_value(card)
        if "A" == card.split(" of ")[0]:
            aces += 1
    # if over 21 and we have aces, count them as 1 instead
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total




# short display name like "A♠" instead of "Ace of Spades"
def short_name(card):
    rank, suit = card.split(" of ")
    symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
    return rank + symbols[suit]
