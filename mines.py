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
import helper
#HEY GUYS, I NEED HELP. I AM TRYING TO LEARN PYGAME, BUT IT IS SO COMPLICATED
#I NEED HELP, PLEASE
#I NEED SOMEONE TO COME IN HERE, AND TELL ME HOW TO CODE PYGAME
def mines_main(win:pygame.display,username,password,file):
    data=helper.csv_get_data(file,{"username":username,"password":password})
    clock=pygame.time.Clock()
    while True:
        win.fill((255, 255, 255))
        keys = pygame.key.get_pressed()
        events=pygame.event.get()
        
        if keys[pygame.K_ESCAPE]:
            quit()
        pygame.display.flip()

if __name__=="__main__":
    pygame.init()
    win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    running = True
    file=helper.csv_file("data_storage.csv")
    mines_main(win,"bob1","<>",file)



pygame.init()

# 1. Grid Configuration
GRID_SIZE = 4
CELL_SIZE = 100
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
pygame.display.set_caption("4x4 Minesweeper")
font = pygame.font.SysFont(None, 40)

# 2. Game State Initialization
# Place exactly 3 mines randomly in 16 total cells
board = [False] * 16
mine_indices = random.sample(range(16), 3)
for idx in mine_indices:
    board[idx] = True

# Cell tracking states: 0 = Hidden, 1 = Revealed, 2 = Flagged
cell_state = [0] * 16
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            index = row * GRID_SIZE + col
            
            # Left Click: Reveal Cell
            if event.button == 1 and cell_state[index] == 0:
                if board[index]:
                    cell_state[index] = 1
                    game_over = True
                else:
                    reveal_cell(row, col)
                    # Win condition: 13 safe cells revealed (16 total - 3 mines)
                    if cell_state.count(1) == 13:
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
                        screen.blit(num_text, (col * CELL_SIZE + 35, row * CELL_SIZE + 35))
            elif cell_state[index] == 2:  # Flagged
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, ORANGE, rect.inflate(-30, -30))  # Flag marker
            else:  # Hidden
                pygame.draw.rect(screen, GRAY, rect)
                
            pygame.draw.rect(screen, DARK_GRAY, rect, 3)

    # End Game Overlay
    if game_over:
        text_str = "You Win!" if won else "Game Over!"
        text_color = WHITE if won else RED
        text = font.render(text_str, True, text_color)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
