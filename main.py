#from all files import all

#display 3 buttons
    #one to start the game to send to login screen
    #one to have a help button
    #one to exit the game
import pygame
import button
import Dice
import Blackjack
import helper
import slots
import mines
import plinko
import slider_screen
import cards
import deck
import installer
import Pygame_file
import pygame_widgets
def error():
    raise SystemExit(
    "\nCRITICAL_ERROR: Load-Bearing Coconut missing!\n"
    "The universe is collapsing. Please return the coconut to the root directory.\n"
    "Error Code: [DEVS_SCARED_TO_TOUCH_THIS_CODE]"
)
def check():
    try:
        img = pygame.image.load('images/coconut.jpg')
    except:
        error()
    check_points = [
        (50, 80),  
        (112, 112),
        (100, 100),   
        (98, 160)   
    ]
    data=[(109, 60, 45, 255),
    (83, 37, 24, 255),
    (100, 53, 37, 255),
    (38, 15, 9, 255)]
    for num,x in enumerate(check_points):
        try:
            color = img.get_at(x)
            if data[num]!=color:
                error()
        except:
            error()
def main():
    win=pygame
    check()














if __name__=="__main__":
    main()