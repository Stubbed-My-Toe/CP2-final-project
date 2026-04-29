import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
#import moduals and init pygame
pygame.init()
#setup desplay
win = pygame.display.set_mode((1000, 600))
#make the slidesr and output
class slider_class:
    def __init__(self, multiplyer, win, slider_cords, box_cords):
        self.multiplyer = multiplyer
        self.slider = Slider(win, *slider_cords, min=0, max=100*multiplyer, step=1)
        self.output = TextBox(win, *box_cords, fontSize=20)
        # Link the textbox submission to the update method
        self.output.onSubmit = self.update_slider

    def update_slider(self):
        try:
            typed_value = int(self.output.getText())
            if 0 <= typed_value <= 100 * self.multiplyer:
                self.slider.setValue(typed_value)
        except ValueError:
            pass
            
    def get_val(self):
        return self.slider.getValue()

    def update_ui(self, events):
        # Sync textbox with slider when not typing
        if not self.output.selected:
            self.output.setText(str(self.get_val()))
        pygame_widgets.update(events)
if "__main__"==__name__:
    # example on how to use
    my_slider = slider_class(2, win, [100, 100, 800, 40], [475, 200, 50, 50])
    clock = pygame.time.Clock()
    run = True
    while run:
        events = pygame.event.get()
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
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()