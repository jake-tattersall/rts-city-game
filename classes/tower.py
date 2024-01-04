import pygame

from classes.unit import Unit
from constants import *
from functions.utility import unit_rect

from .gameobject import GameObject


class Tower(GameObject):
    """Towers"""

    def __init__(self, hp=0, owner=NEUTRAL, win=None, rect=None, speed=False):
        self.hp : int = hp
        self.owner : str = owner
        self.win : pygame.surface.Surface = win
        self.rect : pygame.rect.Rect = rect
        self.priority = 1
        self.speed : bool = speed
        self.__ticks : int = 0
        self.__marker : int = 0
        self.queue : int = 0


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

        if self.queue and (self.__ticks - self.__marker) % SPAWN_DELAY == 0:
            items.append(self.__generate_troop())

        if self.queue < 0:
            self.queue = 0

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

        text = TOWERFONT.render(str(self.hp), True, WHITE)
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
            if self.queue:
                self.queue -= obj.hp
            if self.hp < 0:
                self.owner = obj.owner
                self.hp = -self.hp
        else:
            self.hp += obj.hp


    def prep_troops(self, target):
        """Generate queue, marker, and declare target"""
        self.queue = self.hp
        self.__marker = self.__ticks
        self.target = target


    def __generate_troop(self):
        """Spawn a troop"""
        if self.queue >= UNIT_HP_MAX:
            hp = UNIT_HP_MAX
        else:
            hp = self.queue
            self.queue = 0
        self.queue -= hp
        self.hp -= hp
        return Unit(hp, self.owner, self.win, unit_rect(self.rect.centerx, self.rect.centery), self.target)