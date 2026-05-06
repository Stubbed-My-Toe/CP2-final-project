#Brett
# make the ui


#button to go back


#button to raize bet


#button to lowwer bet


#button to spin


#lable for how much cash the user has


#text box for the users bet that they can click on and change


#if the user clicks go back then go back to main menu


#if the user clicks lowwer bet lower the bet

#if the user clicked raise bet raise the bet

# if the user clicked the text box then alow the user to change what is in it


# if the uesr clicks spin then do the spinning animation and pick 3 random numbers


# if the numbers (put in a list) are in a list of lists then return the dictionary return of that combo


# mulitply the bet by the amount and add that to user amount of cash



import pygame
import random
from pathlib import Path
import helper
pygame.init()
win = pygame.display.set_mode((800, 600))
def weghted_random(l1,wheghts):
    rnum=random.uniform(0,100)
    pnum=0
    for num,x in enumerate(wheghts):
        if x>rnum>pnum:
            return l1[num]
        pnum=x




class Sprite:
    def __init__(self,win,path_to_images:Path,starting_image:int,x:float,y:float,size:tuple,data):
        self.fPath=Path(path_to_images)
        self.ims = [
            pygame.transform.scale(pygame.image.load(str(f)).convert_alpha(),size)
            for f in self.fPath.iterdir() if f.is_file()]        
        self.cim=self.ims[starting_image]
        self.win=win
        self.x=x
        self.y=y
        self.data=data
    def render(self):
        self.win.blit(self.cim, (self.x, self.y))
    def move(self,x,y):
        self.x+=x
        self.y+=y
    def teleport(self,x,y):
        self.x=x
        self.y=y
    def costume(self,image:int):
        self.cim=self.ims[image]
    def get_pos(self,choise=""):
        if choise=="":
            return self.x,self.y
        elif choise=="x":
            return self.x
        elif choise=="y":
            return self.y
<<<<<<< HEAD
=======
    def stored_data(self):
        return self.data
>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575

# 1 & 2: Load and optimize the image
# Use convert_alpha() for PNGs with transparency
offsetx=0
offset=0
<<<<<<< HEAD
face=[[Sprite(win,"inages",0,100+offsetx,100+offset,(100,100)),Sprite(win,"inages",1,175+offsetx,100+offset,(100,100)),Sprite(win,"inages",2,250+offsetx,100+offset,(100,100))],
[Sprite(win,"inages",0,100+offsetx,200+offset,(100,100)),Sprite(win,"inages",1,175+offsetx,200+offset,(100,100)),Sprite(win,"inages",2,250+offsetx,200+offset,(100,100))],
[Sprite(win,"inages",0,100+offsetx,300+offset,(100,100)),Sprite(win,"inages",1,175+offsetx,300+offset,(100,100)),Sprite(win,"inages",2,250+offsetx,300+offset,(100,100))],

]

=======
face=[[Sprite(win,"inages",0,100+offsetx,100+offset,(100,100),(100+offsetx,100+offset)),Sprite(win,"inages",1,175+offsetx,100+offset,(100,100),(175+offsetx,100+offset)),Sprite(win,"inages",2,250+offsetx,100+offset,(100,100),(250+offsetx,100+offset))],
[Sprite(win,"inages",0,100+offsetx,200+offset,(100,100),(100+offsetx,200+offset)),Sprite(win,"inages",1,175+offsetx,200+offset,(100,100),(175+offsetx,200+offset)),Sprite(win,"inages",2,250+offsetx,200+offset,(100,100),(250+offsetx,200+offset))],
[Sprite(win,"inages",0,100+offsetx,300+offset,(100,100),(100+offsetx,300+offset)),Sprite(win,"inages",1,175+offsetx,300+offset,(100,100),(175+offsetx,300+offset)),Sprite(win,"inages",2,250+offsetx,300+offset,(100,100),(250+offsetx,300+offset))],
[Sprite(win,"inages",0,100+offsetx,400+offset,(100,100),(100+offsetx,400+offset)),Sprite(win,"inages",1,175+offsetx,400+offset,(100,100),(175+offsetx,400+offset)),Sprite(win,"inages",2,250+offsetx,400+offset,(100,100),(250+offsetx,400+offset))],
]


>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575
running = True
var=False
spinning=False
vol=0
volconst=0
stopping=0
stop=True
Clock=pygame.time.Clock()
<<<<<<< HEAD
=======
fin=0
cooldown=0
whegts=[1.25,3.75,8.75,18.75,38.75,60,100]
costumes=[6,5,4,3,2,1,0]
>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

<<<<<<< HEAD
    win.fill((255, 255, 255)) # Clear screen
    
=======

    win.fill((255, 255, 255)) # Clear screen
   
>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575
    # 3: Draw (blit) image at coordinates (x, y)
    for q in face:
        for w in q:
            w.render()
            x,y= w.get_pos()
<<<<<<< HEAD
            if y>300:
                w.teleport(x,100)
            if y<100:
                w.teleport(x,300)
=======
            if y>400:
                w.teleport(x,100)
                w.costume(weghted_random(costumes,whegts))
            if y<100:
                w.teleport(x,400)
                w.costume(weghted_random(costumes,whegts))
>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575
    if var:
        for x in face:
            for num,y in enumerate(x):
                y.move(0,vol-(num))
                if vol<10:
                    vol+=.1
                    volconst=vol
                    stop=False
                else:
                    stop=True
    if stopping:
        # 1. Update shared variables ONCE per frame
        if vol > 0:
            vol -= 0.1
        else:
            vol = volconst
            stopping += 1

        # 2. Run the movement logic
        for x in face:
            for num, y in enumerate(x):
<<<<<<< HEAD
                target_y = 200 # Set your desired finish line here
                
                if stopping > num or y.get_pos("y") >= target_y and stopping==num:
                    # Snap to target and stop
                    y.teleport(y.get_pos("x"), target_y)
=======
                target_y = y.stored_data()[1]
               
                if stopping-3 >= num or y.get_pos("y") >= target_y and stopping==num:
                    # Snap to target and stop
                    y.teleport(y.get_pos("x"), target_y)
                    for num2,z in enumerate(face):
                        for num3,s in enumerate(z):
                            if num3==num:
                                target_y = s.stored_data()[1]
                                s.teleport(s.get_pos("x"), target_y)
                                
>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575
                elif stopping == num:
                    # Slow down as it approaches
                    y.move(0, vol)
                else:
                    # Move at full speed
                    y.move(0, volconst)
<<<<<<< HEAD
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not spinning and stop:
        var=True
        spinning=True
        vol=-10
    if keys[pygame.K_x] and spinning and not stopping:
        var=False
        spinning=True
        stopping=1
=======
    if stopping==3:
        stopping=0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not spinning and cooldown<0:
        var=True
        spinning=True
        vol=-10
        cooldown=100
    if keys[pygame.K_SPACE] and spinning and not stopping and cooldown<0:
        var=False
        spinning=False
        stopping=1
        cooldown=30
    cooldown-=1
>>>>>>> e6e11017fb3851bd108da47f1ccd87dc1186b575
    # 4: Update display
    pygame.display.flip()
    Clock.tick(60)
pygame.quit()






       

