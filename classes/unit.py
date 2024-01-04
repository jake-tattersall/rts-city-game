import pygame

from constants import *
from functions.utility import magnitude

from .gameobject import GameObject


class Unit(GameObject):
    """Units"""


    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, target=None):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.priority = 2
        self.target = target


    def tick(self, items : list):
        """Moves the unit, then checks if it needs to perform damage calculation"""
        velocity = [self.target.rect.centerx - self.rect.centerx, self.target.rect.centery - self.rect.centery]

        mag = magnitude(velocity[0], velocity[1])
        if mag != 0 and mag != 5:
            velocity[0] *= (4/mag)
            velocity[1] *= (4/mag)

        self.rect.x += velocity[0]
        self.rect.y += velocity[1]

        for x in items:
            if x == self.target and self.rect.colliderect(x):
                x.damage(self)
                self.hp = 0

        self.draw()


    def draw(self):
        """Draws the unit, then draws its value underneath"""
        if self.hp > 0:
            if self.owner == PLAYER1:
                pygame.draw.rect(self.win, BLUE, self.rect)
            elif self.owner == PLAYER2:
                pygame.draw.rect(self.win, RED, self.rect)
            else:
                pygame.draw.rect(self.win, GREY, self.rect)

            text = UNITFONT.render(str(self.hp), True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = self.rect.center
            text_rect.centery += text_rect.height
            self.win.blit(text, text_rect)