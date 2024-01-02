import pygame
from pygame.locals import *

from constants import *
from generate import generate5, generateSpeedTower
from methods import inside
from objects import Tower, Unit

pygame.init()
clock = pygame.time.Clock()


win = pygame.display.set_mode(size=(WIDTH, HEIGHT))
selected : Tower = None

objects = []
objects.extend(generate5(win))
objects.append(generateSpeedTower(win, objects))

run = True
while run:
    # Towers should tick first
    objects = sorted(objects)

    # Mouse
    pos = pygame.mouse.get_pos()

    # Fill black background
    win.fill((0,0,0))

    player1Alive = False
    player2Alive = False
    neutralAlive = False
    for x in objects:
        # Normal tick
        x.tick(objects)

        # Show highlight on tower
        if x == selected:
            x.hover()

        # Check if players need to be marked alive
        if x.owner == PLAYER1:
            player1Alive = True
        elif x.owner == PLAYER2:
            player2Alive = True
        elif x.owner == NEUTRAL:
            neutralAlive = True

        # Remove dead units and show highlight if hovering
        if isinstance(x, Unit) and x.hp == 0:
            objects.remove(x)
        elif isinstance(x, Tower) and inside(pos, x.rect):
            x.hover()
    
    # End game if only 1 player left
    if (not player1Alive or not player2Alive) and not neutralAlive:
        break

    # Show objects
    pygame.display.flip()

    for event in pygame.event.get(): 
        # Send units
        if event.type == MOUSEBUTTONDOWN:
            change = True
            for x in objects:
                if isinstance(x, Tower) and inside(pos, x.rect):
                    if selected:
                        selected.prep_troops(x)
                    else:
                        if x.owner == PLAYER1:
                            selected = x
                            change = False
                    break
            if change:
                selected = None

            
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            run = False


    clock.tick(FPS)


player1Alive = False
player2Alive = False
for x in objects:
    if x.owner == PLAYER1:
        print("Player 1 Wins!")
        break
    elif x.owner == PLAYER2:
        print("Player 2 Wins!")
        break
