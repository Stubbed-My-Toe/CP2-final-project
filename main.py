#Brett
#from all files import all

#display 3 buttons
    #one to start the game to send to login screen
    #one to have a help button
    #one to exit the game
import pygame
import button
import Dice
import Blackjack
import helper
import slots
import mines
import plinko
import slider_screen
import cards
import deck
import installer
#import Pygame_file
import pygame_widgets
def error():
    raise SystemExit(
    "\nCRITICAL_ERROR: Load-Bearing Coconut missing!\n"
    "The universe is collapsing. Please return the coconut to the root directory.\n"
    "Error Code: [DEVS_SCARED_TO_TOUCH_THIS_CODE]"
)
def check():
    try:
        img = pygame.image.load('images/coconut.jpg')
    except:
        error()
    check_points = [
        (50, 80),  
        (112, 112),
        (100, 100),   
        (98, 160)   
    ]
    data=[(109, 60, 45, 255),
    (83, 37, 22, 255),
    (100, 53, 37, 255),
    (38, 15, 9, 255)]
    for num,x in enumerate(check_points):
        try:
            color = img.get_at(x)

            if data[num]!=color:
                error()
        except:
            error()
def checker(file,user,passer):
    try:
        data=helper.csv_get_data(file,{"username":user.getText(),"password":passer.getText()})
        return data
    except:
        return False
    
def main():
    pygame.init()
    data=None
    win=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    check()
    file=helper.csv_file("data_storage.csv")
    usernameb = pygame_widgets.textbox.TextBox(win, 100, 100, 300, 50, fontSize=30,borderColour=(0, 0, 255), textColour=(0, 0, 0),placeholderText="username")
    passwordb = pygame_widgets.textbox.TextBox(win, 100, 160, 300, 50, fontSize=30,borderColour=(0, 0, 255), textColour=(0, 0, 0),placeholderText="password")
    usernameb.onSubmit(checker, (file, usernameb, passwordb))
    passwordb.onSubmit(checker, (file, usernameb, passwordb))
    passwordb.isPassword = True
    return_button=button.button("save and quit",30,30,300,50,(200,200,200),(100,100,200))
    dice_btn=button.button("dice",)
    clock=pygame.Clock()
    moneybox = pygame_widgets.textbox.TextBox(win, 100, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=passing, radius=10, borderThickness=5)
    while True:
        events=pygame.event.get()
        
        for event in events:
            if return_button.is_clicked(event):
                quit()
        win.fill((255, 255, 255))
        if not data:
            data = passwordb.onSubmitExecute
            pygame_widgets.update(events)
        else:
            moneybox.setText(f"money: {data["cash"]}")
        return_button.draw(win)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()















if __name__=="__main__":
    main()