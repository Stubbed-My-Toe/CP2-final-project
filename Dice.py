#Brett
#Pseudocode for dice

import pygame as py
import pygame_widgets as pw

#from slider screen bring in all
from slider_screen import *
#function for entering bet amount

    #display how much money do you want to place 
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
import pygame
import subprocess
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
font = pygame.font.SysFont('Arial', 32)

# Button settings
button_rect = pygame.Rect(150, 120, 100, 50)
button_color = (0, 200, 0)  # Green
text_surf = font.render('Run', True, (255, 255, 255))

running = True
while running:
    screen.fill((30, 30, 30)) # Dark background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked the button area
            if button_rect.collidepoint(event.pos):
                print("Running slider.py...")
                # subprocess.Popen runs the file using the current Python interpreter
                subprocess.Popen([sys.executable, 'slider.py'])

    # Draw the button and text
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(text_surf, (button_rect.x + 22, button_rect.y + 10))
    
    pygame.display.flip()

pygame.quit()
