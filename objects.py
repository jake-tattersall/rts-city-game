from abc import ABC, abstractmethod

import pygame

from constants import *
from methods import magnitude, unit_rect

pygame.init()
towerFont = pygame.font.SysFont('Arial', 20)
unitFont = pygame.font.SysFont('Arial', 10)


class GameObject(ABC):
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

    
class Tower(GameObject):
    """Towers"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, speed=False):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.speed : bool = speed
        self.__ticks : int = 0
        self.__marker : int = 0
        self.__target = None
        self.__queue : int = 0

    
    def __lt__(self, other):
        return isinstance(other, Unit)


    def tick(self, items : list):
        """
        Every 60 ticks (2 seconds), gain a unit. 
        If has a queue, create troops when necessary.
        Draw tower
        """
        if self.owner != NEUTRAL:
            self.__ticks += 1
            if self.speed:
                timer = FPS * GROW_MOD * .5
            else:
                timer = FPS * GROW_MOD
            if self.__ticks == timer:
                self.hp += 1
                self.__ticks = 0

        if self.__queue and (self.__ticks - self.__marker) % SPAWN_DELAY == 0:
            items.append(self.__generate_troop())

        if self.__queue < 0:
            self.__queue = 0

        self.draw()


    def draw(self):
        """Draw the tower"""
        if self.owner == PLAYER1:
            pygame.draw.rect(self.win, BLUE, self.rect)
        elif self.owner == PLAYER2:
            pygame.draw.rect(self.win, RED, self.rect)
        else:
            pygame.draw.rect(self.win, GREY, self.rect)

        # If speed tower, give hat
        if self.speed:
            vertices = [(self.rect.x, self.rect.y), 
                        (self.rect.x + self.rect.width - 1, self.rect.y), 
                        (self.rect.x + (TOWER_WIDTH / 2), self.rect.y - (TOWER_WIDTH / 2))]
            if self.owner == PLAYER1:
                pygame.draw.polygon(self.win, BLUE, vertices)
            elif self.owner == PLAYER2:
                pygame.draw.polygon(self.win, RED, vertices)
            else:
                pygame.draw.polygon(self.win, GREY, vertices)

        text = towerFont.render(str(self.hp), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.win.blit(text, text_rect)
        

    def hover(self):
        """Highlights the tower when hovered over"""

        if self.speed:
            highlight_poly = [(self.rect.x - OUTLINE_WIDTH, self.rect.y), 
                        (self.rect.x + (TOWER_WIDTH / 2), self.rect.y - (TOWER_WIDTH / 2)),
                        (self.rect.x + self.rect.width, self.rect.y), 
                        (self.rect.x + TOWER_WIDTH, self.rect.y + TOWER_WIDTH),
                        (self.rect.x - OUTLINE_WIDTH, self.rect.y + TOWER_WIDTH),
                        ]
            

            pygame.draw.polygon(self.win, YELLOW, highlight_poly, OUTLINE_WIDTH)
        else:
            hightlight_rect = pygame.rect.Rect((self.rect.x - OUTLINE_WIDTH, self.rect.y - OUTLINE_WIDTH, \
                                                self.rect.width + 2 * OUTLINE_WIDTH, self.rect.height + 2 * OUTLINE_WIDTH))
            pygame.draw.rect(self.win, YELLOW, hightlight_rect, OUTLINE_WIDTH)


    def damage(self, obj : GameObject):
        """Take damage. If hp goes negative, change sides. Called from the unit's tick function"""
        if obj.owner != self.owner:
            self.hp -= obj.hp
            if self.__queue:
                self.__queue -= obj.hp
            if self.hp < 0:
                self.owner = obj.owner
                self.hp = -self.hp
        else:
            self.hp += obj.hp


    def prep_troops(self, target):
        """Generate queue, marker, and declare target"""
        self.__queue = self.hp
        self.__marker = self.__ticks
        self.__target = target


    def __generate_troop(self):
        """Spawn a troop"""
        if self.__queue >= UNIT_HP_MAX:
            hp = UNIT_HP_MAX
        else:
            hp = self.__queue
            self.__queue = 0
        self.__queue -= hp
        self.hp -= hp
        return Unit(hp, self.owner, self.win, unit_rect(self.rect.centerx, self.rect.centery), self.__target)


class Unit(GameObject):
    """Units"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, target=None):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.target : Tower = target


    def __lt__(self, other):
        return not isinstance(other, Unit)


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

            text = unitFont.render(str(self.hp), True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = self.rect.center
            text_rect.centery += text_rect.height
            self.win.blit(text, text_rect)
