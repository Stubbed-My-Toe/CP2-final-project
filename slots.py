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
from pathlib import Path
pygame.init()
win = pygame.display.set_mode((800, 600))
class Sprite:
    def __init__(self,win,path_to_images:Path,starting_image:int,x:float,y:float,size:tuple):
        self.fPath=Path(path_to_images)
        self.ims = [
            pygame.transform.scale(pygame.image.load(str(f)).convert_alpha(),size)
            for f in self.fPath.iterdir() if f.is_file()]        
        self.cim=self.ims[starting_image]
        self.win=win
        self.x=x
        self.y=y
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

# 1 & 2: Load and optimize the image
# Use convert_alpha() for PNGs with transparency
offsetx=0
offset=0
face=[[Sprite(win,"inages",0,100+offsetx,100+offset,(100,100)),Sprite(win,"inages",1,175+offsetx,100+offset,(100,100)),Sprite(win,"inages",2,250+offsetx,100+offset,(100,100))],
[Sprite(win,"inages",0,100+offsetx,200+offset,(100,100)),Sprite(win,"inages",1,175+offsetx,200+offset,(100,100)),Sprite(win,"inages",2,250+offsetx,200+offset,(100,100))],
[Sprite(win,"inages",0,100+offsetx,300+offset,(100,100)),Sprite(win,"inages",1,175+offsetx,300+offset,(100,100)),Sprite(win,"inages",2,250+offsetx,300+offset,(100,100))],

]

running = True
var=False
spinning=False
vol=0
volconst=0
stopping=0
stop=True
Clock=pygame.time.Clock()
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((255, 255, 255)) # Clear screen
    
    # 3: Draw (blit) image at coordinates (x, y)
    for q in face:
        for w in q:
            w.render()
            x,y= w.get_pos()
            if y>300:
                w.teleport(x,100)
            if y<100:
                w.teleport(x,300)
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
                target_y = 200 # Set your desired finish line here
                
                if stopping > num or y.get_pos("y") >= target_y and stopping==num:
                    # Snap to target and stop
                    y.teleport(y.get_pos("x"), target_y)
                elif stopping == num:
                    # Slow down as it approaches
                    y.move(0, vol)
                else:
                    # Move at full speed
                    y.move(0, volconst)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not spinning and stop:
        var=True
        spinning=True
        vol=-10
    if keys[pygame.K_x] and spinning and not stopping:
        var=False
        spinning=True
        stopping=1
    # 4: Update display
    pygame.display.flip()
    Clock.tick(60)
pygame.quit()



        