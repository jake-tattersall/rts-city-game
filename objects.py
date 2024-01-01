import pygame
import math
from abc import ABC, abstractmethod

from constants import *

class Object(ABC):
    """Parent class for all pieces"""

    hp = None
    owner = None
    win = None
    rect = None


    @abstractmethod
    def tick(self):
        """"""


    @abstractmethod
    def draw(self):
        """"""


class Test(Object):
    """"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, velocity=[0,0]):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.velocity : list = velocity


    def tick(self):
        """"""
        mag = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** .5
        if mag != 0 and mag != 5:
            self.velocity[0] *= (5/mag)
            self.velocity[1] *= (5/mag)

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= WIDTH:
            self.velocity[0] = -self.velocity[0]

        if self.rect.y <= 0 or self.rect.y + self.rect.height >= HEIGHT:
            self.velocity[1] = -self.velocity[1]

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
        self.hp = hp
        self.owner = owner
        self.win = win
        self.rect = rect


    def tick(self):
        """"""


    def draw(self):
        """"""



class Unit(Object):
    """"""

    def __init__(self, hp=0, owner=None, win=None, rect=None):
        self.hp = hp
        self.owner = owner
        self.win = win
        self.rect = rect


    def tick(self):
        """"""


    def draw(self):
        """"""