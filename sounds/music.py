import pygame
import time

pygame.init()
pygame.display.set_mode((1, 1))
pygame.mixer.init()
pygame.mixer.music.load("sounds/bowser's fortified fortress.mp3")
pygame.mixer.music.play(loops=-1)
try:
    while True:
        pygame.event.pump()
        time.sleep(0.1)
except KeyboardInterrupt:
    pygame.mixer.music.stop()
    pygame.quit()