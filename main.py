import pygame
from objects import Test, Tower, Unit
from constants import *


def inside(mouse : tuple, rect : pygame.rect.Rect):
    """Returns true if the mouse is inside of the given rectangle"""
    if mouse[0] >= rect.x and mouse[0] <= rect.x + rect.width:
        if mouse[1] >= rect.y and mouse[1] <= rect.y + rect.height:
            return True
    return False


pygame.init()
clock = pygame.time.Clock()


win = pygame.display.set_mode(size=(WIDTH, HEIGHT))

pixel = pygame.rect.Rect((10,10), (5,5))
pixel = Test(1, PLAYER1, win, pixel, velocity=[100,20])
tower1 = pygame.rect.Rect((300, 500), (TOWER_WIDTH, TOWER_HEIGHT))
tower1 = Tower(100, PLAYER2, win, tower1)
unit1 = pygame.rect.Rect((20, 20), (UNIT_WIDTH, UNIT_HEIGHT))
unit1 = Unit(10, PLAYER1, win, unit1, tower1)

objects = [tower1, unit1]

run = True
while run:

    pos = pygame.mouse.get_pos()

    win.fill((0,0,0))

    for x in objects:
        x.tick(objects)
    #pixel.tick()

    for x in objects:
        if isinstance(x, Unit) and x.hp == 0:
            objects.remove(x)

    pygame.display.flip()

    for event in pygame.event.get(): 

        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            run = False
        
    clock.tick(FPS)