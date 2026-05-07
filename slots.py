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
from slider_screen import vertical_slider
import pygame_widgets
from button import button


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




def passing():
    pass



def slots_main(win,username,password,file:helper.csv_file):
    data=helper.csv_get_data(file,{"username":username,"password":password})
    offsetx=0
    offset=0
    face=[[Sprite(win,"images/slots",0,100+offsetx,100+offset,(100,100),[100+offsetx,100+offset,0]),Sprite(win,"images/slots",1,175+offsetx,100+offset,(100,100),[175+offsetx,100+offset,0]),Sprite(win,"images/slots",2,250+offsetx,100+offset,(100,100),[250+offsetx,100+offset,0])],
    [Sprite(win,"images/slots",0,100+offsetx,200+offset,(100,100),[100+offsetx,200+offset,0]),Sprite(win,"images/slots",1,175+offsetx,200+offset,(100,100),[175+offsetx,200+offset,0]),Sprite(win,"images/slots",2,250+offsetx,200+offset,(100,100),[250+offsetx,200+offset,0])],
    [Sprite(win,"images/slots",0,100+offsetx,300+offset,(100,100),[100+offsetx,300+offset,0]),Sprite(win,"images/slots",1,175+offsetx,300+offset,(100,100),[175+offsetx,300+offset,0]),Sprite(win,"images/slots",2,250+offsetx,300+offset,(100,100),[250+offsetx,300+offset,0])],
    [Sprite(win,"images/slots",0,100+offsetx,400+offset,(100,100),[100+offsetx,400+offset,0]),Sprite(win,"images/slots",1,175+offsetx,400+offset,(100,100),[175+offsetx,400+offset,0]),Sprite(win,"images/slots",2,250+offsetx,400+offset,(100,100),[250+offsetx,400+offset,0])],
    ]
    info=Sprite(win,"images/slot",1,600,20,(1000,1000),"")

    cash=int(data["cash"])




    bet=4
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
    try:
        womp=pygame.mixer.Sound("sounds/universfield-cartoon-fail-trumpet-278822.mp3")
        spin=pygame.mixer.Sound("sounds/freesound_community-spinner-sound-36693 (mp3cut.net).mp3")
        chaching=pygame.mixer.Sound("sounds/u_oepgi4ep3v-som_matricula-464025.mp3")
    except:
        pass
    whegts=[10, 25, 45, 65, 80, 92, 100] 
    multiplyer=[3,5,7,15,30,70,200]
    #multiplyer=[1000,1000,1000,1000,1000,1000,1000]
    costumes=[6,5,4,3,2,1,0]
    bet_slider=vertical_slider(3,win,[600,500],[500,450],[300,10])
    moneybox = pygame_widgets.textbox.TextBox(win, 1000, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=passing, radius=10, borderThickness=5)
    super = pygame.font.SysFont('Arial', 500)
    bruh = super.render('bruh', True, (0, 0, 0))
    returne=button("return",300,600,200,40,(100,100,100),(100,100,200))
    drop=button("spin/stop",300,650,200,40,(100,100,100),(100,100,200))
    while running:
        events=pygame.event.get()
        win.fill((255, 255, 255)) # Clear screen
        # 3: Draw (blit) image at coordinates (x, y)
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
                    if num2+1<stopping:
                        y.teleport(y.stored_data()[0],y.stored_data()[1])
                    elif num2+1==stopping:
                        tdata=y.stored_data()
                        if tdata[2]<0:
                            if abs(y.get_pos("y")-y.stored_data()[1])<10:
                                tdata[2]=0
                                stopping+=1
                            else:
                                y.change_data([y.stored_data()[0],y.stored_data()[1],(y.stored_data()[2]-1)])
                        y.change_data([tdata[0],tdata[1],tdata[2]-.1])
                        y.move(0,y.stored_data()[2])
                    else:
                        tdata=y.stored_data()
                        y.change_data([tdata[0],tdata[1],vol])
                        y.move(0,y.stored_data()[2])
        for num,q in enumerate(face):
            for w in q:
                w.render()
                x,y= w.get_pos()
                if y>400:
                    w.teleport(x,100)
                    if num>stopping:
                        w.costume(weghted_random(costumes,whegts))
                if y<100:
                    w.teleport(x,400)
                    if num>stopping:
                        w.costume(weghted_random(costumes,whegts))
        info.render()
        
        if stopping==4:
            stopping=0
            stoped=True
            spinning=False
            for num,x in enumerate(face):
                if num==0:
                    continue
                stat=[]
                for y in x:
                    stat.append(y.get_costume())
                fail=False
                if stat[0]==stat[1]==stat[2]:
                    cash+=bet*multiplyer[stat[0]]
                else:
                    fail=True
            try:
                spin.stop()
                if fail:
                    womp.play()
                else:
                    chaching.play()
            except:
                pass
        if not spinning and stoped:
            for x in face:
                for y in x:
                    y.teleport(y.stored_data()[0],y.stored_data()[1])
            bet_slider.update_ui(events)
        moneybox.setText(f"money: {cash}")
        returne.draw(win)
        drop.draw(win)
        keys = pygame.key.get_pressed()
        cooldown-=1
        if bet==0:
            win.blit(bruh, (500,500))
        bet=bet_slider.get_val()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if (drop.is_clicked(event)) and not spinning and cooldown<0 and stoped:
                if bet <= cash:
                    cash -= bet
                    var=True
                    spinning=True
                    stoped=True
                    vol=-10
                    cooldown=100
                    try:
                        spin.play(-1)
                    except:
                        pass
                    
            if (drop.is_clicked(event))and spinning and cooldown<0:
                var=False
                spinning=False
                stopping=1
                cooldown=30
                stoped=False

            if returne.is_clicked(event):
                file.update_row(
                        {"username": username, "password": password}, 
                        {"cash": cash,"times_played_blackjack":data["times_played_blackjack"],"times_played_dice":data["times_played_dice"],"times_played_plinko":data["times_played_plinko"],"times_played_slots":int(data["times_played_slots"])+1,}
                    )
                return
        pygame_widgets.update(events)
        # 4: Update display
        pygame.display.flip()
        Clock.tick(60)
       
if __name__=="__main__":
    pygame.init()
    win=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    file=helper.csv_file("data_storage.csv")
    slots_main(win,"bob1","<>",file)
    pygame.quit()
