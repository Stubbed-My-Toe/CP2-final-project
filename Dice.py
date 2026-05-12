#Brett
# make the ui
from main import *

import pygame
import pygame_widgets

#button to go back



#button to raize bet



#Button to lesson bet


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
import trandom
import random
from pathlib import Path
import helper
from slider_screen import vertical_slider
import pygame_widgets
from button import button
from collections import Counter

def weghted_random(l1,wheghts):
   rand=trandom.alternate_random(1,1000000000)
   random.seed(next(rand))
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
       self.costumee=starting_image
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
       self.costumee=image
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
   def get_costume(self):
       return self.costumee

def score(dice:list):
    counts = Counter(dice)
    score = 0
    if len(counts) == 6:
        return 1500
    occurrences = sorted(counts.values(), reverse=True)
    if occurrences == [6]: return 3000
    if occurrences == [5, 1]: return 2000
    if occurrences == [4, 2]: return 2000
    if occurrences == [3, 3]: return 2500
    if occurrences == [2, 2, 2]: return 1500
    if occurrences[0] == 4:
        score += 1000
        for num in counts:
            if counts[num] == 4: counts[num] = 0
    for num in range(1, 7):
        if counts[num] >= 3:
            score += 300 if num == 1 else num * 100
            counts[num] -= 3
    score += counts[1] * 100
    score += counts[5] * 50
    
    return score

def passing():
    pass



def dice_main(win,username,password,file:helper.csv_file):
    data=helper.csv_get_data(file,{"username":username,"password":password})
    offsetx=0
    offset=0
    face=[Sprite(win,"images/dice",0,100,20,(100,100),""),Sprite(win,"images/dice",0,100,130,(100,100),""),Sprite(win,"images/dice",0,100,240,(100,100),""),Sprite(win,"images/dice",0,100,350,(100,100),""),Sprite(win,"images/dice",0,100,460,(100,100),""),Sprite(win,"images/dice",0,100,570,(100,100),"")]
    info=Sprite(win,"images/diccc",0,600,20,(1000,1000),"")
    tic=0
    cash=int(data["cash"])
    stoped=True
    Clock=pygame.time.Clock()
    costumes=[5,4,3,2,1,0]
    bet_slider=vertical_slider(3,win,[600,500],[500,450],[300,10])
    moneybox = pygame_widgets.textbox.TextBox(win, 1000, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=passing, radius=10, borderThickness=5)
    super = pygame.font.SysFont('Arial', 500)
    bruh = super.render('bruh', True, (0, 0, 0))
    returne=button("return",300,600,200,40,(100,100,100),(100,100,200))
    drop=button("roll",300,650,200,40,(100,100,100),(100,100,200))
    keep=button("keep",300,700,200,40,(100,100,100),(100,100,200))
    rand=trandom.alternate_random(0,5)
    while True:
        events=pygame.event.get()
        win.fill((255, 255, 255)) # Clear screen
        # 3: Draw (blit) image at coordinates (x, y)
        for x in face:
            x.render()
        returne.draw(win)
        drop.draw(win)
        keep.draw(win)
        if tic>=0:
            for x in face:
                x.costume(next(rand))
            tic-=1
        for event in events:
            if drop.is_clicked(event):
                if tic<0:
                    tic=30
            if keep.is_clicked(event):
                pass 
            if returne.is_clicked(event):
                file.update_row(
                        {"username": username, "password": password}, 
                        {"cash": cash,"times_played_blackjack":data["times_played_blackjack"],"times_played_dice":data["times_played_dice"],"times_played_plinko":data["times_played_plinko"],"times_played_slots":int(data["times_played_slots"])+1,}
                    )
                bet_slider.kill()
                del moneybox
                return
        pygame_widgets.update(events)
        # 4: Update display
        pygame.display.flip()
        Clock.tick(60)
       
if __name__=="__main__":
    pygame.init()
    win=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    file=helper.csv_file("data_storage.csv")
    dice_main(win,"test","<NULL>",file)
    pygame.quit()
