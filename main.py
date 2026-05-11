#from all files import all

#display 3 buttons
    #one to start the game to send to login screen
    #one to have a help button
    #one to exit the game
import pygame
import button
#import Dice
#import Blackjack
import helper
import slots
#import mines
import plinko
#import slider_screen
#import cards
#import deck
#import installer
import hashlib
#import Pygame_file
import pygame_widgets
import time
def error():
    raise SystemExit(
    "\nCRITICAL_ERROR: Load-Bearing Coconut missing!\n"
    "The universe is collapsing. Please return the coconut to the root directory.\n"
    "Error Code: [DEVS_SCARED_TO_TOUCH_THIS_CODE]"
)
def check():
    try:
        with open("images/coconut.jpg", "rb") as f:
            file_bytes = f.read()
            # Create a unique SHA-256 string for this specific file
            if hashlib.sha256(file_bytes).hexdigest()!="8a2eb9ac1cbded56a8dc018d02b74a30f14dd3163b7ceed4e9908ec7d077de18":
                raise TabError
    except:
        error()
     
# Example: store this string once, then check other images against it
def checker(file,user,passer):
    global data
    try:
        data=helper.csv_get_data(file,{"username":user.getText(),"password":passer.getText()})
    except:
        makeer(file,user.getText(),passer.getText())
def makeer(file:helper.csv_file,user,passer):
    global data
    file.add([user,passer,200,0,0,0,0])
    data=data=helper.csv_get_data(file,{"username":user,"password":passer})
def main():
    global data
    pygame.init()
    data=None
    win=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    check()
    file=helper.csv_file("data_storage.csv")
    usernameb = pygame_widgets.textbox.TextBox(win, 100, 100, 300, 50, fontSize=30,borderColour=(0, 0, 255), textColour=(0, 0, 0),placeholderText="username")
    passwordb = pygame_widgets.textbox.TextBox(win, 100, 160, 300, 50, fontSize=30,borderColour=(0, 0, 255), textColour=(0, 0, 0),placeholderText="password")
    passwordb.isPassword = True
    make_acount=button.button("login/make account",30,250,300,50,(100,100,100),(100,100,200))
    return_button=button.button("save and quit",30,30,300,50,(100,100,100),(100,100,200))
    dice_btn=button.button("dice (WIP)",30,90,300,50,(100,100,100),(100,100,200))
    slots_btn=button.button("slots",30,150,300,50,(100,100,100),(100,100,200))
    black_jack=button.button("blackjack",30,210,300,50,(100,100,100),(100,100,200))
    plinko_btn=button.button("plinko",30,270,300,50,(100,100,100),(100,100,200))
    mines_btn=button.button("mines (WIP)",30,330,300,50,(100,100,100),(100,100,200))
    clock=pygame.time.Clock()
    moneybox = pygame_widgets.textbox.TextBox(win, 500, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=plinko.passing, radius=10, borderThickness=5)
    while True:
        win.fill((255, 255, 255))
        events=pygame.event.get()
        for event in events:
            if return_button.is_clicked(event):
                quit()
            if make_acount.is_clicked(event):
                makeer(file,usernameb.getText(),passwordb.getText())
                time.sleep(1)
        if data==None:
            make_acount.draw(win)
            pass
        else:
            if data=="bad":
                data=None
                continue
            else:
                moneybox.setText(f"money: {data["cash"]}")
                dice_btn.draw(win)
                slots_btn.draw(win)
                black_jack.draw(win)
                plinko_btn.draw(win)
                mines_btn.draw(win)
                usernameb.hide()
                passwordb.hide()
                for event in events:
                    if dice_btn.is_clicked(event):
                        moneybox.hide()
                        pass #dice main
                    if slots_btn.is_clicked(event):
                        moneybox.hide()
                        slots.slots_main(win,data["username"],data["password"],file)
                    if black_jack.is_clicked(event):
                        moneybox.hide()
                        pass
                    if plinko_btn.is_clicked(event):
                        moneybox.hide()
                        plinko.plinko_main(win,data["username"],data["password"],file)
                    if mines_btn.is_clicked(event):
                        moneybox.hide()
                        pass
                    moneybox.show()
        pygame_widgets.update(events)
                
            
        return_button.draw(win)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()















if __name__=="__main__":
    main()