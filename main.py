import pygame
from objects import Test
from constants import *

pygame.init()


clock = pygame.time.Clock()


win = pygame.display.set_mode(size=(WIDTH, HEIGHT))

pixel = pygame.rect.Rect((10,10), (5,5))
pixel = Test(10, PLAYER1, win, pixel)

run = True
while run:
    win.fill((0,0,0))

    pixel.tick()


    pygame.display.flip()

    for event in pygame.event.get(): 

        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            run = False
        
    clock.tick(144)