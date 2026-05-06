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
    def stored_data(self):
        return self.data
    def change_data(self,new_data):
        self.data=new_data


# 1 & 2: Load and optimize the image
# Use convert_alpha() for PNGs with transparency
offsetx=0
offset=0
face=[[Sprite(win,"inages",0,100+offsetx,100+offset,(100,100),[100+offsetx,100+offset,0]),Sprite(win,"inages",1,175+offsetx,100+offset,(100,100),[175+offsetx,100+offset,0]),Sprite(win,"inages",2,250+offsetx,100+offset,(100,100),[250+offsetx,100+offset,0])],
[Sprite(win,"inages",0,100+offsetx,200+offset,(100,100),[100+offsetx,200+offset,0]),Sprite(win,"inages",1,175+offsetx,200+offset,(100,100),[175+offsetx,200+offset,0]),Sprite(win,"inages",2,250+offsetx,200+offset,(100,100),[250+offsetx,200+offset,0])],
[Sprite(win,"inages",0,100+offsetx,300+offset,(100,100),[100+offsetx,300+offset,0]),Sprite(win,"inages",1,175+offsetx,300+offset,(100,100),[175+offsetx,300+offset,0]),Sprite(win,"inages",2,250+offsetx,300+offset,(100,100),[250+offsetx,300+offset,0])],
[Sprite(win,"inages",0,100+offsetx,400+offset,(100,100),[100+offsetx,400+offset,0]),Sprite(win,"inages",1,175+offsetx,400+offset,(100,100),[175+offsetx,400+offset,0]),Sprite(win,"inages",2,250+offsetx,400+offset,(100,100),[250+offsetx,400+offset,0])],
]


running = True
var=False
spinning=False
vol=0
volconst=0
stopping=0
stoped=True
Clock=pygame.time.Clock()
fin=0
cooldown=0
print()
whegts=[1.25,3.75,8.75,18.75,38.75,60,100]
costumes=[6,5,4,3,2,1,0]
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
            if y>400:
                w.teleport(x,100)
                w.costume(weghted_random(costumes,whegts))
            if y<100:
                w.teleport(x,400)
                w.costume(weghted_random(costumes,whegts))
    if spinning:
        if vol<10:
            vol+=1
        
        for x in face:
            for y in x:
                tdata=y.stored_data()
                y.change_data([tdata[0],tdata[1],vol])
                y.move(0,y.stored_data()[2])
    if stopping!=0:
        for num1,x in enumerate(face):#3
            for num2,y in enumerate(x):#4
                if num2<stopping:
                    y.teleport(y.stored_data()[0],y.stored_data()[1]) 
                elif num2==stopping:
                    tdata=y.stored_data()
                    if tdata[2]<0:
                        tdata[2]=0
                        stopping+=1
                    y.change_data([tdata[0],tdata[1],tdata[2]-1])
                    y.move(0,y.stored_data()[2])
                else:
                    tdata=y.stored_data()
                    y.change_data([tdata[0],tdata[1],vol])
                    y.move(0,y.stored_data()[2])
    if stopping>3:
        stopping=0
        stoped=True
        spinning=False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not spinning and cooldown<0 and stoped:
        var=True
        spinning=True
        stoped=False
        vol=-10
        cooldown=100
        print()
    if keys[pygame.K_SPACE] and spinning and cooldown<0:
        var=False
        spinning=False
        stopping=1
        cooldown=30
        stoped=False
    cooldown-=1

    # 4: Update display
    pygame.display.flip()
    Clock.tick(60)
pygame.quit()






       

