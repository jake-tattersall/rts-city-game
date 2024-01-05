import pygame
from pygame.locals import *

from classes.tower import Tower
from classes.unit import Unit
from constants import *
from functions.generation import generate5, generateSpeedTower
from functions.npc import ai_decision

pygame.init()
clock = pygame.time.Clock()


win = pygame.display.set_mode((0,0))
selected : Tower = None

objects = []
objects.extend(generate5(win))
objects.append(generateSpeedTower(win, objects))

def sorting_key(item):
    """Sort items by their priority. Closer to 0 means up front"""
    return item.priority

run = True
while run:
    # Towers should tick first
    objects = sorted(objects, key=sorting_key)

    # Mouse
    pos = pygame.mouse.get_pos()

    # Fill black background
    win.fill(BLACK)

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
        elif isinstance(x, Tower) and x.rect.collidepoint(pos):
            x.hover()

    # End game if only 1 player left and no neutrals
    if (not player1Alive or not player2Alive) and not neutralAlive:
        break

    ai_decision(objects)

    # Show objects
    pygame.display.flip()

    for event in pygame.event.get(): 
        # Send units
        if event.type == MOUSEBUTTONDOWN:
            change = True
            for x in objects:
                if isinstance(x, Tower) and x.rect.collidepoint(pos):
                    if selected and x != selected:
                        selected.prep_troops(x)
                    else:
                        if x.owner == PLAYER1:
                            selected = x
                            change = False
                    break
            if change:
                selected = None

        # Pause
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                paused = True
                inner_run = True

                pauseFont = pygame.font.SysFont('Arial', 30)

                win.fill(BLACK)

                resume = pygame.rect.Rect(0,0,PAUSE_WIDTH,PAUSE_HEIGHT)
                resume.center = (WIDTH / 3, HEIGHT / 2)
                resume_text = pauseFont.render("Resume", True, WHITE)
                resume_text_rect = resume_text.get_rect()
                resume_text_rect.center = resume.center

                end = pygame.rect.Rect(0,0,PAUSE_WIDTH,PAUSE_HEIGHT)
                end.center = (2 * WIDTH / 3, HEIGHT / 2)
                end_text = pauseFont.render("Exit", True, WHITE)
                end_text_rect = end_text.get_rect()
                end_text_rect.center = end.center

                pygame.draw.rect(win, BLUE, resume)
                pygame.draw.rect(win, RED, end)
                win.blit(resume_text, resume_text_rect)
                win.blit(end_text, end_text_rect)

                pygame.display.flip()

                while inner_run:
                    
                    pos = pygame.mouse.get_pos()

                    for event in pygame.event.get(): 
                        if event.type == MOUSEBUTTONDOWN:
                            if resume.collidepoint(pos):
                                inner_run = False
                            elif end.collidepoint(pos):
                                exit(1)

                    clock.tick(FPS)


        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            run = False


    clock.tick(FPS)


#print(pygame.surfarray.array2d(win))

player1Alive = False
player2Alive = False
for x in objects:
    if x.owner == PLAYER1:
        print("Player 1 Wins!")
        break
    elif x.owner == PLAYER2:
        print("Player 2 Wins!")
        break

