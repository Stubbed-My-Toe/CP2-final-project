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
import trandom
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
    circle.friction = .2
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
    circle.friction = .3
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
def plinko_main(win,username,password,file:helper.csv_file):
    rand=trandom.alternate_random(1,100000000)
    data=helper.csv_get_data(file,{"username":username,"password":password})
    font = pygame.font.SysFont('Arial', 30)
    super = pygame.font.SysFont('Arial', 500)
    times1 = font.render('x50', True, (0, 0, 0))
    times2 = font.render('x4', True, (0, 0, 0))
    times3 = font.render('x3', True, (0, 0, 0))
    times4 = font.render('x.8', True, (0, 0, 0))
    times5 = font.render('x.3', True, (0, 0, 0))
    times6 = font.render('x.8', True, (0, 0, 0))
    times7 = font.render('x3', True, (0, 0, 0))
    times8 = font.render('x4', True, (0, 0, 0))
    times9 = font.render('x50', True, (0, 0, 0))
    bruh = super.render('bruh', True, (0, 0, 0))
    moneybox = pygame_widgets.textbox.TextBox(win, 100, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=passing, radius=10, borderThickness=5)
    returne=button("return",300,300,100,40,(100,100,100),(100,100,200))
    drop=button("drop",300,350,100,40,(100,100,100),(100,100,200))
    bet_slider=vertical_slider(3,win,[400,500],[300,450],[300,10])
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
        b_shape = pymunk.Poly.create_box(b_body, (spaecing * 0.9, 40))
        b_shape.collision_type = 2
        b_shape.multiplier = [50,4,3,.8,.3,.8,3,4,50][i]
        space.add(b_shape)

    bet=10
    chips = []
    running = True
    while running:
        speed=1
        win.fill((255, 255, 255))
        space.debug_draw(draw_options)
        returne.draw(win)
        drop.draw(win)
        moneybox.setText(f"money: {game_state["cash"]}")
        monney=int(game_state["cash"])
        bet=bet_slider.get_val()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            speed=100
        #print(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (drop.is_clicked(event) or keys[pygame.K_a]) and not game_state['dropped']:
                if bet <= monney:
                    game_state['cash'] -= bet
                    random.seed(next(rand))
                    x, y = 1000 + random.uniform(-1, 1), 160
                    chips.append(create_chip(space, x, y, bet))
                    game_state['dropped'] = True
            if returne.is_clicked(event):
                file.update_row(
                        {"username": username, "password": password}, 
                        {"cash": game_state["cash"],"times_played_blackjack":data["times_played_blackjack"],"times_played_dice":data["times_played_dice"],"times_played_plinko":int(data["times_played_plinko"])+1,"times_played_slots":data["times_played_slots"],}
                    )
                bet_slider.kill()
                del moneybox
                return
        listt=[]
        for x in range(500,1461,120):
            listt.append(x)
        win.blit(times1, (listt[0], 1040)) 
        win.blit(times2, (listt[1], 1040))
        win.blit(times3, (listt[2], 1040))
        win.blit(times4, (listt[3], 1040)) 
        win.blit(times5, (listt[4], 1040))
        win.blit(times6, (listt[5], 1040))
        win.blit(times7, (listt[6], 1040)) 
        win.blit(times8, (listt[7], 1040))
        win.blit(times9, (listt[8], 1040))
        if bet==0:
            win.blit(bruh, (500,500))
        for x in range(13):
            space.step((1*speed)/800)
        bet_slider.update_ui(pygame.event.get())
        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()

if __name__=="__main__":
    pygame.init()
    pygame.mixer.init(0)
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