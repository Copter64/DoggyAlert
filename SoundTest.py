import pygame
pygame.mixer.init()
pygame.mixer.music.load("PottyMsg.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue