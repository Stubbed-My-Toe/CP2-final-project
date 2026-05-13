import pygame
import random
import sys
#Commented pandas because it is not being used yet 
#import pandas

#Isaac
#pygame

#display mines window
#display 5x5 grid
#ask user to enter bet amount (when the bet amount is conrimed and the game starts, the bet amount is subtracted fro mthe ballance)
#ask user to choose amount of bombs(1-24)
#else the defalt is 3

#display 5x5 grid
#ask user to enter bet amount (when the bet amount is confirmed and the game starts, the bet amount is subtracted from the balance)
#ask user to choose amount of bombs(1-24)
#else the default is 3
#bomb amount changes multiplier for each square correctly guessed, scaling with the amount of bombs placed on the field, 1 being the lowest ending multiplier, and 24 being the highest

#GAME
    #Have two buttons appear at the bottom of the screen, one that will say cashout, and one that will say quit.
    #boxes will appear as well. One that says their multiplier, one thats the actual amount that they will earn if they cashout
    #quit means they will lose their bet, and the multiplier, and close the game.
    #If user selects cashout,the amount of their bet * multiplier will be added to their account.
 
       #When bomb input and bet is put in, put that many mines on the field as blank tiles randomly, and the multipliers as blank tiles as well. 
        #have users click tiles, if safe, turn tile blue, and increase multiplier. 
        #if tile turns red, it's a bomb, and it will say game over, end the game

        #The Game resets and is playable again and the player can choose to go back home or play different games on the side bar

        #The Game resets and is playable again and the player can choose to go back home or play different games on the side bar

import pygame
import pymunk
import pymunk.pygame_util
import math
import random
import helper
import time
from slider_screen import vertical_slider
import pygame_widgets
from button import button
#Commented pandas because it is not being used yet 
#import pandas

#Isaac
#pygame

#display mines window
#display 5x5 grid
#ask user to enter bet amount (when the bet amount is conrimed and the game starts, the bet amount is subtracted fro mthe ballance)
#ask user to choose amount of bombs(1-24)
#else the defalt is 3

#display 5x5 grid
#ask user to enter bet amount (when the bet amount is confirmed and the game starts, the bet amount is subtracted from the balance)
#ask user to choose amount of bombs(1-24)
#else the default is 3
#bomb amount changes multiplier for each square correctly guessed, scaling with the amount of bombs placed on the field, 1 being the lowest ending multiplier, and 24 being the highest

#GAME
    #Have two buttons appear at the bottom of the screen, one that will say cashout, and one that will say quit.
    #boxes will appear as well. One that says their multiplier, one thats the actual amount that they will earn if they cashout
    #quit means they will lose their bet, and the multiplier, and close the game.
    #If user selects cashout,the amount of their bet * multiplier will be added to their account.
 
       #When bomb input and bet is put in, put that many mines on the field as blank tiles randomly, and the multipliers as blank tiles as well. 
        #have users click tiles, if safe, turn tile blue, and increase multiplier. 
        #if tile turns red, it's a bomb, and it will say game over, end the game

        #The Game resets and is playable again and the player can choose to go back home or play different games on the side bar

        #The Game resets and is playable again and the player can choose to go back home or play different games on the side bar

import pygame
import random

pygame.init()

# 1. Grid Configuration
GRID_SIZE = 10
CELL_SIZE = 60  # Reduced size slightly so a 10x10 grid fits comfortably on standard screens
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("10x10 Minesweeper")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# 2. Game State Initialization
# FIX: Changed * 10 to * 100 to match the 100 cells in a 10x10 grid
board = [False] * 100  
mine_indices = random.sample(range(100), 3)  # Places exactly 3 mines
for idx in mine_indices:
    board[idx] = True

# Cell tracking states: 0 = Hidden, 1 = Revealed, 2 = Flagged
cell_state = [0] * 100
game_over = False
won = False

# 3. Helpers for Proximity and Chain Reactions
def count_adjacent_mines(row, col):
    count = 0
    for r in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
        for c in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
            if board[r * GRID_SIZE + c]:
                count += 1
    return count

def reveal_cell(row, col):
    index = row * GRID_SIZE + col
    if cell_state[index] != 0:  # Skip if already revealed or flagged
        return

    cell_state[index] = 1  # Reveal
    
    # If the cell has zero adjacent mines, automatically reveal neighbors
    if count_adjacent_mines(row, col) == 0:
        for r in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
            for c in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
                reveal_cell(r, c)

# 4. Main Game Loop
running = True
while running:
    clock.tick(60)  # Caps frame rate at 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            
            # Boundary safeguard check
            if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                index = row * GRID_SIZE + col
                
                # Left Click: Reveal Cell
                if event.button == 1 and cell_state[index] == 0:
                    if board[index]:
                        cell_state[index] = 1
                        game_over = True
                    else:
                        reveal_cell(row, col)
                        # FIX: Win condition updated to 97 safe cells (100 total - 3 mines)
                        if cell_state.count(1) == 97:
                            game_over = True
                            won = True
                            
                # Right Click: Toggle Flag
                elif event.button == 3:
                    if cell_state[index] == 0:
                        cell_state[index] = 2
                    elif cell_state[index] == 2:
                        cell_state[index] = 0

    # 5. Rendering Layout
    screen.fill(BLACK)
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            index = row * GRID_SIZE + col
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if cell_state[index] == 1:  # Revealed
                if board[index]:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    mines_near = count_adjacent_mines(row, col)
                    if mines_near > 0:
                        num_text = font.render(str(mines_near), True, BLUE)
                        screen.blit(num_text, (col * CELL_SIZE + (CELL_SIZE//3), row * CELL_SIZE + (CELL_SIZE//4)))
            elif cell_state[index] == 2:  # Flagged
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, ORANGE, rect.inflate(-20, -20))  # Flag marker
            else:  # Hidden
                pygame.draw.rect(screen, GRAY, rect)
                
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

    # End Game Overlay
    if game_over:
        text_str = "You Win!" if won else "Game Over!"
        text_color = WHITE if won else RED
        text = font.render(text_str, True, text_color)
        # Centers text layout roughly in the middle
        overlay_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, overlay_rect)

    pygame.display.flip()  # FIX: Required to update the graphics display context

pygame.quit()


def reset_game():
    """Generates a clean board layout for a new match."""
    global board, cell_state, game_over, won
    board = [False] * 100
    mine_indices = random.sample(range(100), 3)
    for idx in mine_indices:
        board[idx] = True
    cell_state = [0] * 100
    game_over = False
    won = False

def mines_main(win, username, password, file: helper.csv_file):
    global game_over, won, cell_state, board
    
    # Initialize the board state for the first run
    reset_game()
    clock = pygame.time.Clock()
    
    # Fetch player profile metrics from your CSV helper
    data = helper.csv_get_data(file, {"username": username, "password": password})
    
    # Instantiate UI Buttons (Positioned centrally near the bottom framework)
    returne = button("Return", WIDTH // 2 - 110, HEIGHT - 80, 100, 40, (100, 100, 100), (140, 140, 140))
    play_again = button("Play Again", WIDTH // 2 + 10, HEIGHT - 80, 110, 40, (100, 100, 100), (140, 140, 140))
    
    running = True
    while running:
        clock.tick(60)
        win.fill(BLACK)
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
                
            # Intercept system actions when the match finishes
            if game_over:
                if returne.is_clicked(event):
                    # Save metrics back to database before closing context
                    file.update_row(
                        {"username": username, "password": password}, 
                        {
                            "cash": game_state["cash"],
                            "times_played_blackjack": data["times_played_blackjack"],
                            "times_played_dice": data["times_played_dice"],
                            "times_played_plinko": data["times_played_plinko"],
                            "times_played_slots": data["times_played_slots"],
                            "times_played_mines": int(data.get("times_played_mines", 0)) + 1
                        }
                    )
                    return  # Break loop and exit to standard menu framework
                    
                if play_again.is_clicked(event):
                    reset_game()
                    continue

            # Core Gameplay Input Handling
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    index = row * GRID_SIZE + col
                    
                    if event.button == 1 and cell_state[index] == 0:  # Left Click
                        if board[index]:
                            cell_state[index] = 1
                            game_over = True
                        else:
                            reveal_cell(row, col)
                            if cell_state.count(1) == 97:  # Win condition validation
                                game_over = True
                                won = True
                                
                    elif event.button == 3:  # Right Click Flagging
                        if cell_state[index] == 0:
                            cell_state[index] = 2
                        elif cell_state[index] == 2:
                            cell_state[index] = 0

        # 2. Render Grid Map Matrix
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                index = row * GRID_SIZE + col
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if cell_state[index] == 1:
                    if board[index]:
                        pygame.draw.rect(win, RED, rect)
                    else:
                        pygame.draw.rect(win, WHITE, rect)
                        mines_near = count_adjacent_mines(row, col)
                        if mines_near > 0:
                            num_text = font.render(str(mines_near), True, BLUE)
                            win.blit(num_text, (col * CELL_SIZE + 35, row * CELL_SIZE + 35))
                elif cell_state[index] == 2:
                    pygame.draw.rect(win, GRAY, rect)
                    pygame.draw.rect(win, ORANGE, rect.inflate(-30, -30))
                else:
                    pygame.draw.rect(win, GRAY, rect)
                    
                pygame.draw.rect(win, DARK_GRAY, rect, 1)

        # 3. Render Post-Game UI Overlays
        if game_over:
            text_str = "You Win!" if won else "Game Over!"
            text_color = WHITE if won else RED
            text = font.render(text_str, True, text_color)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
            
            # Draw the Interactive Selection Elements on screen
            returne.draw(win)
            play_again.draw(win)

        pygame.display.flip()
