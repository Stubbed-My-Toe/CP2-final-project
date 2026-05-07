import pygame
import time

pygame.init()
pygame.display.set_mode((1, 1))
pygame.mixer.init()
t=[]

t=pygame.mixer.Sound("sounds/bowser's fortified fortress.mp3")
tim=t.get_length()



while True:
    for x in range(2):
        t.play()
        time.sleep(.01)
    time.sleep(tim)
