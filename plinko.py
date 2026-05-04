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
import random
import helper
import time
from slider_screen import vertical_slider
import pygame_widgets
from button import button
def create_chip(space, x, y,bet):
    body = pymunk.Body(1, 1)
    body.position = (x, y)
    circle = pymunk.Circle(body, 40)
    circle.collision_type = 1
    circle.elasticity = 0
    circle.friction = 0
    circle.bet_value = bet 
    space.add(body, circle)
    return circle
bet_return = 0
multiplier = 0.0
def on_bucket_hit(arbiter, space, data):
    chip_shape = arbiter.shapes[0]
    bucket_shape = arbiter.shapes[1]
    reward = int(chip_shape.bet_value * bucket_shape.multiplier)
    data['cash'] += reward
    data['dropped']=False
    data['sound'].play()
    space.add_post_step_callback(lambda s, b: s.remove(b, b.body), chip_shape)
    return False
def create_peg(space, x, y):
    body = space.static_body
    circle = pymunk.Circle(body, 20, (x, y))
    circle.elasticity = 0
    circle.friction = 0
    circle.collision_type = 3
    space.add(circle)
    return circle
def play_bounce(arbiter, space, data):
    global last_play_time
    global COOLDOWN
    current_time = pygame.time.get_ticks()
    
    # Only play if enough time has passed
    if current_time - last_play_time > COOLDOWN:
        data['sound'].play()
        last_play_time = current_time
        
    return True
def remove_shape(arbiter, space):
    global dropped
    dropped=False
    shape_to_kill = arbiter.shapes[0]
    space.add_post_step_callback(actual_delete, shape_to_kill)
    return True 
def actual_delete(space, shape):
    space.remove(shape, shape.body)

def passing():
    pass
last_play_time = 0
COOLDOWN = 1
def plinko_main(win,username,password,file):
    data=helper.csv_get_data(file,{"username":username,"password":password})
    
    returne=button("return",300,300,100,40,(100,100,100),(100,100,200))
    drop=button("drop",300,350,100,40,(100,100,100),(100,100,200))
    bet_slider=vertical_slider(3,win,[400,500],[300,400],[300,10])
    coin=pygame.mixer.Sound("sounds/chieuk-coin-257878 (1).wav")
    bounce=pygame.mixer.Sound("sounds/dragon-studio-pop-402322.wav")
    space = pymunk.Space()
    space.gravity = (0, 300)
    game_state = {'cash': int(data["cash"]), 'bet': 10, 'dropped': False,"sound":coin}
    space.on_collision(1, 2, begin=on_bucket_hit, data=game_state)
    space.on_collision(1, 3, begin=play_bounce, data={"sound":bounce})
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(win)
    layers=8
    spaecing=120
    pegs=[]
    start=(1000,100)
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
        b_shape.multiplier = [50,5,3,.8,.5,.8,3,5,50][i]
        space.add(b_shape)

    bet=10
    chips = []
    running = True
    font = pygame.font.SysFont('Arial', 30)
    while running:
        speed=1
        win.fill((255, 255, 255))
        space.debug_draw(draw_options)
        returne.draw(win)
        drop.draw(win)
        moneybox = pygame_widgets.textbox.TextBox(win, 100, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=passing, radius=10, borderThickness=5)
        moneybox.setText(f"money: {data["cash"]}")
        monney=int(data["cash"])
        bet=bet_slider.get_val()
        # 1. Event Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            speed=10
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Drop a new chip on mouse click
            if drop.is_clicked(event) and not game_state['dropped']:
                if bet <= monney:
                    x, y = 1000+random.uniform(-1,1),160
                    chips.append(create_chip(space, x,y,bet))
                    game_state['dropped'] = True

        for x in range(13*speed):
            space.step(1/1200)
        bet_slider.update_ui(pygame.event.get())
        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()

    pygame.quit()
if __name__=="__main__":
    pygame.init()
    win=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    file=helper.csv_file("data_storage.csv")
    plinko_main(win,"bob1","<>",file)

"""import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont('Arial', 24)

# 1. Pre-render your different text instances
score_surf = font.render('Score: 100', True, (255, 255, 255))
health_surf = font.render('Health: 80%', True, (255, 0, 0))
level_surf = font.render('Level: 5', True, (0, 255, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30)) # Clear screen

    # 2. Draw each instance at different coordinates
    screen.blit(score_surf, (20, 20))    # Top Left
    screen.blit(health_surf, (450, 20))  # Top Right
    screen.blit(level_surf, (270, 350))  # Bottom Center

    pygame.display.flip()"""