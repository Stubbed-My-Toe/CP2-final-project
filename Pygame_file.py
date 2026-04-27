#bring in pygame
import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 40)

# 1. Define button properties
button_rect = pygame.Rect(300, 250, 200, 50) # x, y, width, height
button_color = (0, 128, 255) # Blue

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 2. Check for click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos):
                print("Start Game Clicked!")
                from slider_screen import *
                slider_screen()
                

    screen.fill((30, 30, 30))
    
    # 3. Hover effect (optional)
    current_color = (0, 200, 255) if button_rect.collidepoint(mouse_pos) else button_color
    draw_button("START", button_rect, current_color)
    
    pygame.display.flip()

pygame.quit()