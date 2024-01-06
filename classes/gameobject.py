from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """Parent class for all pieces"""

    def __init__(self, hp, owner, win, rect):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.priority : int = None
        self.target = None


    @abstractmethod
    def tick(self, items : list):
        """"""


    @abstractmethod
    def draw(self):
        """"""
        

    def __lt__(self, other):
        return self.priority - other.priority