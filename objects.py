import pygame
import math
from abc import ABC, abstractmethod

from constants import *

pygame.init()
towerFont = pygame.font.SysFont('Arial', 20)
unitFont = pygame.font.SysFont('Arial', 10)


class Object(ABC):
    """Parent class for all pieces"""

    hp = None
    owner = None
    win = None
    rect = None


    @abstractmethod
    def tick(self, items : list):
        """"""


    @abstractmethod
    def draw(self):
        """"""


class Test(Object):
    """"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, velocity=[0,0], target=None):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.velocity : list = velocity
        self.target : pygame.rect.Rect = target


    def tick(self, items : list):
        """"""
        mag = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** .5
        if mag != 0 and mag != 5:
            self.velocity[0] *= (4/mag)
            self.velocity[1] *= (4/mag)

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= WIDTH:
            self.velocity[0] = -self.velocity[0]

        if self.rect.y <= 0 or self.rect.y + self.rect.height >= HEIGHT:
            self.velocity[1] = -self.velocity[1]

        for x in items:
            if isinstance(x, Tower) and self.rect.colliderect(x):
                x.damage(self)

        self.draw()


    def draw(self):
        """"""
        if self.hp > 0:
            if self.owner == PLAYER1:
                pygame.draw.rect(self.win, BLUE, self.rect)
            elif self.owner == PLAYER2:
                pygame.draw.rect(self.win, RED, self.rect)
            else:
                pygame.draw.rect(self.win, GREY, self.rect)

    
class Tower(Object):
    """"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.ticks : int = 0


    def tick(self, items : list):
        """"""
        self.ticks += 1
        if self.ticks == FPS * 2:
            self.hp += 1
            self.ticks = 0

        self.draw()


    def draw(self):
        """"""
        if self.owner == PLAYER1:
            pygame.draw.rect(self.win, BLUE, self.rect)
        elif self.owner == PLAYER2:
            pygame.draw.rect(self.win, RED, self.rect)
        else:
            pygame.draw.rect(self.win, GREY, self.rect)

        text = towerFont.render(str(self.hp), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.win.blit(text, text_rect)
        

    
    def damage(self, obj : Object):
        """Take damage. If loses all hp, change sides"""
        self.hp -= obj.hp
        if self.hp <= 0:
            self.owner = obj.owner
            if self.hp < 0:
                self.hp = -self.hp



class Unit(Object):
    """"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, target=None):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.target : Tower = target


    def tick(self, items : list):
        """"""
        velocity = [self.target.rect.centerx - self.rect.centerx, self.target.rect.centery - self.rect.centery]

        mag = (velocity[0] ** 2 + velocity[1] ** 2) ** .5
        if mag != 0 and mag != 5:
            velocity[0] *= (4/mag)
            velocity[1] *= (4/mag)

        self.rect.x += velocity[0]
        self.rect.y += velocity[1]

        for x in items:
            if isinstance(x, Tower) and self.rect.colliderect(x):
                x.damage(self)
                self.hp = 0

        self.draw()


    def draw(self):
        """"""
        if self.hp > 0:
            if self.owner == PLAYER1:
                pygame.draw.rect(self.win, BLUE, self.rect)
            elif self.owner == PLAYER2:
                pygame.draw.rect(self.win, RED, self.rect)
            else:
                pygame.draw.rect(self.win, GREY, self.rect)

            text = unitFont.render(str(self.hp), True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = self.rect.center
            text_rect.centery += text_rect.height
            self.win.blit(text, text_rect)