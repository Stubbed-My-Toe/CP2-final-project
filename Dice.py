#Brett
#Pseudocode for dice

import pygame as py
import pygame_widgets as pw

#from slider screen bring in all
from slider_screen import *
#function for entering bet amount
def bet():
    #display how much money do you want to place bets
    pw.box = TextBox(100,200)
    #user is brought to the slider screen.
    #user may change the bet amount or the slider amount or just run the game

#function for winning the game
    #if the computer is tied with the user then the user wins
        #amount is multiplied by the slider amount
    #if the user won the game
        #amount is multiplied by the slider amount
    #if the user lost the game
        #amount is not returned

#funtion for playing the game
    #while not false
        #call function entering bet amount
        #user press the run button.
            #call function winning the game