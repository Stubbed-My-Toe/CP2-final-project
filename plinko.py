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
def create_chip(space, x, y,bet):
    body = pymunk.Body(1, 1)
    body.position = (x, y)
    circle = pymunk.Circle(body, 40)
    circle.collision_type = 1
    circle.elasticity = 0.6
    circle.friction = 0
    circle.reward_value = bet
    space.add(body, circle)
    return circle
bet_return = 0
multiplier = 0.0
def on_bucket_hit(arbiter, space, data):
    # ball (A) hits bucket (B)
    ball, bucket = arbiter.shapes
    
    # Send the ball and the values to the safe removal function
    space.add_post_step_callback(remove_and_update, ball, bucket.multiplier)
    return True
def create_peg(space, x, y):
    body = space.static_body
    circle = pymunk.Circle(body, 20, (x, y))
    circle.elasticity = 0.8
    circle.friction = 0
    
    space.add(circle)
    return circle
def create_bucket(name,x,y,hight,width):
    box=pymunk.Poly.create_box(bod)
def remove_shape(arbiter, space, data):
    shape_to_kill = arbiter.shapes[0]
    # This schedules the removal for the very near future
    space.add_post_step_callback(actual_delete, shape_to_kill)
    return True 
def actual_delete(space, shape):
    space.remove(shape, shape.body)


def plinko_main(win,username,password):
    space = pymunk.Space()
    space.gravity = (0, 300)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(win)
    layers=10
    spaecing=120
    pegs=[]
    start=(1000,200)
    for x in range(layers):
        for y in range(x+1):
            r=start[0]+(y-(x/2))*spaecing
            c=start[1]+x*(spaecing)
            pegs.append(create_peg(space,int(r),int(c)))
    bottom_y = start[1] + (layers * spaecing)
    for i in range(layers+1):
        box_x = start[0] + (i - (layers / 2)) * spaecing
        b_body = space.static_body
        b_body.position = (box_x, bottom_y)
        b_shape = pymunk.Poly.create_box(b_body, (spaecing * 0.9, 20))
        b_shape.collision_type = 2
        b_shape.multiplier = 2.0   
        space.add(b_shape)

    bet=10
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
                chips.append(create_chip(space, x,y,bet))
        space.step(1/120)
        win.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
    pygame.quit()
if __name__=="__main__":
    pygame.init()
    win=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    plinko_main(win,1,1)