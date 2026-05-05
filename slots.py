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

# 1 & 2: Load and optimize the image
# Use convert_alpha() for PNGs with transparency
my_image = Sprite(win,"inages",0,100,100,(100,100))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((0, 0, 0)) # Clear screen
    
    # 3: Draw (blit) image at coordinates (x, y)
    my_image.render()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        my_image.costume(1)
    # 4: Update display
    pygame.display.flip()

pygame.quit()



        