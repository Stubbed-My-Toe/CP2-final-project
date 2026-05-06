import pygame
import time

pygame.init()
pygame.display.set_mode((1, 1))
pygame.mixer.init()
t=[]

t.append(pygame.mixer.Sound("sounds/bowser's fortified fortress.mp3"))


try:
    for x in range(2):
        t[0].play()
        time.sleep(1)
while True:
    pygame.event.pump()
except KeyboardInterrupt:
    pygame.mixer.music.stop()
    pygame.quit()