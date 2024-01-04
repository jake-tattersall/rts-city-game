from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """Parent class for all pieces"""

    hp : int = None
    owner : str = None
    win : pygame.surface.Surface = None
    rect : pygame.rect.Rect = None
    priority : int = None


    @abstractmethod
    def tick(self, items : list):
        """"""


    @abstractmethod
    def draw(self):
        """"""


    def __lt__(self, other):
        return self.priority - other.priority