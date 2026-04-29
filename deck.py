#import random
#make class called deck
#init func with bool input of joker
#shuffle func that adds all but jokers to deck and if joker adds 2 jokers
#draw card func to pull a random card and return it then remove it from deck
#make len func to return length of deck
# make iter func thta returns the deck
import random
class deck:
    def __init__(self,joker):
        """joker is a bool, true will add jokers and false will not"""
        self.joker=joker
        self.shuffle()
    def shuffle(self):
        """shuffles the deck"""
        self.deck=['2 of Hearts', '3 of Hearts', '4 of Hearts', '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds', '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', 'King of Diamonds', 'Ace of Diamonds', '2 of Clubs', '3 of Clubs', '4 of Clubs', '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs', 'King of Clubs', 'Ace of Clubs', '2 of Spades', '3 of Spades', '4 of Spades', '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades', 'Ace of Spades']
        if self.joker:
            self.deck.append("joker")
            self.deck.append("joker")
        random.shuffle(self.deck)
    def draw_card(self,aceval=1,jackval=11,queenval=12,kingval=13,jokerval=14):
        """returns a card from the deck and removes it
        if there is no card in the deck it will shuffle the deck then return a card and its val"""
        if not self.deck:
            self.shuffle()
        card=self.deck.pop(random.randint(0,len(self.deck)-1))
        if "Ace" in card:
            val = aceval
        elif "2" in card:
            val = 2
        elif "3" in card:
            val = 3
        elif "4" in card:
            val = 4
        elif "5" in card:
            val = 5
        elif "6" in card:
            val = 6
        elif "7" in card:
            val = 7
        elif "8" in card:
            val = 8
        elif "9" in card:
            val = 9
        elif "10" in card:
            val = 10
        elif "Jack" in card:
            val=jackval
        elif "Queen" in card:
            val=queenval
        elif "King" in card:
            val=kingval
        elif "joker" in card:
            val=jokerval
        if "Heart" in card:
            sute="Heart"
            color="red"
        elif "Diamond" in card:
            sute="Diamond"
            color="red"
        elif "Spade" in card:
            sute="Spade"
            color="black"
        elif "Club" in card:
            sute="Club"
            color="black"
        return card,val,sute,color
    def __len__(self):
        return len(self.deck)
    def __iter__(self):
        return self.deck

#example on how to use:
if "__main__"==__name__:
    bjdeck=deck(False)
    for x in range(3):
        card,val,sute,color=bjdeck.draw_card()
        print(f"the card is {card}\nthe value is {val}\nthe suite is {sute}\nthe color is {color}")
    