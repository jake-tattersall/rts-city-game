import pygame

from constants import *


def magnitude(v1, v2) -> float:
    """Returns the magnitude of the hypotenuse"""
    return (v1 ** 2 + v2 ** 2) ** .5


def unit_rect(tower_centerx, tower_centery) -> pygame.rect.Rect:
    """Returns a unit Rect centered on the generating tower"""
    x = pygame.rect.Rect(0, 0, UNIT_WIDTH, UNIT_WIDTH)
    x.center = (tower_centerx, tower_centery)
    return x


def tower_rect(x, y) -> pygame.rect.Rect:
    """Returns a tower Rect generated at the given (x,y) coordinate"""
    return pygame.rect.Rect(x, y, TOWER_WIDTH, TOWER_WIDTH)


def checkDistance(xs, ys):
    """Checks if distance is less than the minimum distance"""
    for i in range(0, len(xs)-1):
        for j in range(i+1, len(xs)):
            mag = magnitude(xs[i] - xs[j], ys[i] - ys[j])
            if mag < MIN_DISTANCE:
                return False
    return True