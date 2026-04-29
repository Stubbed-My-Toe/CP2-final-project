#import moduals and init pygame
#setup desplay
#make the slidesr and output
#setup the slider from the pygame wigits
# Link the textbox submission to the update method
#update the slider if changed
#return the val of the slider
# Sync textbox with slider when not typing



import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
#import moduals and init pygame
pygame.init()
#setup desplay
win = pygame.display.set_mode((1000, 600))
#make the slidesr and output

y = pygame.display.set_mode((400, 500))

class vertical_slider1:
    def __init__(self, multiplyer, win, slider1_cords, box_cords):
        self.multiplyer = multiplyer
        #setup the slider1 from the pygame wigits
        self.slider1 = slider1(win, *slider1_cords, min=0, max=100*multiplyer, step=1)
        self.output = TextBox(win, *box_cords, fontSize=20)
        # Link the textbox submission to the update method
        self.output.onSubmit = self.update_slider1
    #update the slider1 if changed
    def update_slider1(self):
        try:
            typed_value = int(self.output.getText())
            if 0 <= typed_value <= 100 * self.multiplyer:
                self.slider1.setValue(typed_value)
        except ValueError:
            pass
    #return the val of the slider1
    def get_val(self):
        return self.slider1.getValue()

    def update_ui(self, events):
        # Sync textbox with slider1 when not typing
        if not self.output.selected:
            self.output.setText(str(self.get_val()))
        pygame_widgets.update(events)
slider1 = vertical_slider1(180, 50, 20, 300, 0, 100)

if "__main__"==__name__:
    # example on how to use
    #make object of class
    my_slider1 = vertical_slider1(2, win, [100, 100, 800, 40], [475, 200, 50, 50])
    #make clock
    clock = pygame.time.Clock()
    run = True
    while run:
        #get pygame events
        events = pygame.event.get()
        #if there is an event to quit then quit
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        win.fill((255, 255, 255))

        # Get the value like this
        current_value = my_slider1.get_val()
        #symple example of useing val
        win.fill((200, 255, current_value))

        # Update and draw widgets
        my_slider1.update_ui(events)
        #update the display and clock tick
        pygame.display.update()
        clock.tick(60)

class slider_class:
    def __init__(self, multiplyer, win, slider_cords, box_cords):
        self.multiplyer = multiplyer
        #setup the slider from the pygame wigits
        self.slider = Slider(win, *slider_cords, min=0, max=100*multiplyer, step=1)
        self.output = TextBox(win, *box_cords, fontSize=20)
        # Link the textbox submission to the update method
        self.output.onSubmit = self.update_slider
    #update the slider if changed
    def update_slider(self):
        try:
            typed_value = int(self.output.getText())
            if 0 <= typed_value <= 100 * self.multiplyer:
                self.slider.setValue(typed_value)
        except ValueError:
            pass
<<<<<<< HEAD
    #return the val of the slider
=======
            
>>>>>>> 7cc971b5b3ee146ce979674775b75b52282d63ea
    def get_val(self):
        return self.slider.getValue()

    def update_ui(self, events):
        # Sync textbox with slider when not typing
        if not self.output.selected:
            self.output.setText(str(self.get_val()))
        pygame_widgets.update(events)

if "__main__"==__name__:
    # example on how to use
    #make object of class
    my_slider = slider_class(2, win, [100, 100, 800, 40], [475, 200, 50, 50])
    #make clock
    clock = pygame.time.Clock()
    run = True
    while run:
        #get pygame events
        events = pygame.event.get()
        #if there is an event to quit then quit
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        win.fill((255, 255, 255))

        # Get the value like this
        current_value = my_slider.get_val()
        #symple example of useing val
        win.fill((200, 255, current_value))

        # Update and draw widgets
        my_slider.update_ui(events)
        #update the display and clock tick
        pygame.display.update()
        clock.tick(60)

    pygame.quit()