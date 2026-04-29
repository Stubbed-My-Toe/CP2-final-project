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


    