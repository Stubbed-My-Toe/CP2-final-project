import pygame,sys
#make a button class
class button:
    #init the class with text, x, y, width, height, color, hover_color
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Arial", 30)
    #draw the button
    def draw(self, screen):
        # Change color if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        # Render and center text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        #make is clicked func that will return a bool depending on if it is clicked
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
if "__main__"==__name__:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Button Example")
    clock = pygame.time.Clock()

    # Create an instance of your button
    start_button = button( "Start Game",300, 250, 200, 50, (0, 128, 255), (0, 200, 255))

    while True:
        screen.fill((30, 30, 30)) # Clear screen with a dark grey

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Check for button click
            if start_button.is_clicked(event):
                print("button clicked")

        # Draw the button
        start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS