from math import floor
from random import randint

from classes.tower import Tower
from constants import *
from functions.utility import checkDistance, tower_rect


def generate5(win) -> list:
    """Create 5 towers in a partitioned field. Make sure none are within MIN_DISTANCE pixels"""
    towers = []
    while True:
        # Top left
        x1 = randint(BUFFER, floor(WIDTH / 3))
        y1 = randint(BUFFER, HEIGHT / 2)

        # Top middle
        x2 = randint(floor(WIDTH / 3), floor(2 * WIDTH / 3))
        y2 = randint(BUFFER, HEIGHT / 2)

        # Top right
        x3 = randint(floor(2 * WIDTH / 3), WIDTH - TOWER_WIDTH - BUFFER)
        y3 = randint(BUFFER, HEIGHT / 2)

        # Bottom left
        x4 = randint(BUFFER, WIDTH / 2)
        y4 = randint(HEIGHT / 2, HEIGHT - TOWER_WIDTH - BUFFER)

        # Bottom right
        x5 = randint(WIDTH / 2, WIDTH - TOWER_WIDTH - BUFFER)
        y5 = randint(HEIGHT / 2, HEIGHT - TOWER_WIDTH - BUFFER)

        xs = (x1, x2, x3, x4, x5)
        ys = (y1, y2, y3, y4, y5)

        if checkDistance(xs, ys):
            break

    while True:
        player1Tower = randint(0, 4)
        player2Tower = randint(0, 4)
        if player1Tower != player2Tower:
            break

    for i in range(0, len(xs)):
        if i == player1Tower:
            towers.append(Tower(PLAYER_TOWER_HP, PLAYER1, win, tower_rect(xs[i], ys[i])))
        elif i == player2Tower:
            towers.append(Tower(PLAYER_TOWER_HP, PLAYER2, win, tower_rect(xs[i], ys[i])))
        else:
            towers.append(Tower(NEUTRAL_TOWER_HP, NEUTRAL, win, tower_rect(xs[i], ys[i])))

    return towers


def generateSpeedTower(win, towers : list) -> Tower:
    """Creates a speed tower somewhere on the map"""
    xs = [i.rect.x for i in towers]
    ys = [i.rect.y for i in towers]

    while True:
        x = randint(BUFFER, WIDTH - BUFFER - TOWER_WIDTH)
        y = randint(BUFFER, HEIGHT - BUFFER - TOWER_WIDTH)

        if checkDistance((*xs, x), (*ys, y)):
            break

    return Tower(SPEED_TOWER_HP, NEUTRAL, win, tower_rect(x, y), True)

    

