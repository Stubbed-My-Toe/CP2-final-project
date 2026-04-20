import pygame
import pymunk
import pymunk.pygame_util

# Initialize Pygame and Pymunk
pygame.init()
space = pymunk.Space()
space.gravity = (0, 1800) # Positive Y is down in Pygame

# Create Static Pegs
def create_peg(space, x, y):
	body = space.static_body
	circle = pymunk.Circle(body, 10, (x, y))
	circle.elasticity = 0.5
	circle.friction = 0.5
	space.add(circle)
	return circle

# Create Falling Chip
def create_chip(space, x, y):
	body = pymunk.Body(1, 1)
	body.position = (x, y)
	circle = pymunk.Circle(body, 15)
	circle.elasticity = 0.4
	circle.friction = 0.5
	space.add(body, circle)
	return circle

# --- Setup ---
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create some pegs in a grid pattern
layers=9
spaecing=60
offset=50
pegs=[]
for x in range(layers):
    for y in range(x):
        if x%2==0:
             offsett=offset
        else:
             offsett=0
        pegs.append(create_peg(space, (x-offsett)+300, y*spaecing-30))

chips = []

# --- Main Loop ---
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Drop a new chip on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            chips.append(create_chip(space, x, y))

    # 2. Physics Step
    # Using 1/60 for a stable 60 FPS simulation
    space.step(1/60)

    # 3. Drawing
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)  # Automatically draws Pymunk shapes
    pygame.display.flip()

    # 4. Framerate Control
    clock.tick(60)

pygame.quit()
