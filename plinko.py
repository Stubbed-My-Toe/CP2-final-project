# make the ui
# set var space to pymunk space class and set the gravity to 0,1800
# define plinko peg
#define it with peramaters space, x,y,radeus,elascity,friction
#create body with pymunk.static body
#set the position
#make it a circle
#set the friction and elasticity
#add it to space and return the shape
#define plinko chip
#define it with peramaters space, x,y,radeus,elascity,friction,mass
#create body with pymunk.body
#set the position
#make it a circle
#set the friction and elasticity
#add it to space and return the shape
#button to go back
#button to raize bet
#button to lowwer bet
#button to drop chip
#lable for how much cash the user has
#text box for the users bet that they can click on and change
#if the user clicks go back then go back to main menu
#if the user clicks lowwer bet lower the bet
#if the user clicked raise bet raise the bet
# if the user clicked the text box then alow the user to change what is in it
# if the uesr clicks drop chip then:
# simulate the chip untill it hits a score thing
# add the score*bet to amount of cash
import pygame
import pymunk
import pymunk.pygame_util
import math
def create_chip(space, x, y):
	body = pymunk.Body(1, 1)
	body.position = (x, y)
	circle = pymunk.Circle(body, 6)
	circle.elasticity = 0.6
	circle.friction = 0
	space.add(body, circle)
	return circle

def create_peg(space, x, y):
	body = space.static_body
	circle = pymunk.Circle(body, 20, (x, y))
	circle.elasticity = 0.8
	circle.friction = 0
	space.add(circle)
	return circle

def plinko_main(win,username,password):
    space = pymunk.Space()
    space.gravity = (0, 300)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(win)
    layers=9
    spaecing=100
    pegs=[]
    start=(1000,500)
    for x in range(layers):
        for y in range(x+1):
            r=start[0]+(y-(x/2))*spaecing
            c=start[1]+x*(spaecing)
            pegs.append(create_peg(space,int(r),int(c)))
    chips = []
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Drop a new chip on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                chips.append(create_chip(space, x,y))
        space.step(1/120)
        win.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        for _ in range(4):
            space.step(1/3000)
    pygame.quit()
if __name__=="__main__":
    pygame.init()
    win=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    plinko_main(win,1,1)