from classes.tower import Tower
from classes.unit import Unit
from constants import PLAYER2


def get_optimal_tower() -> Tower:
    """"""


def get_precise_data(objects : list = None):
    """"""
    # First, check if action must happen
    no_player2_towers_units = all(item.owner != PLAYER2 for item in objects)
    if no_player2_towers_units:
        return

    player2_towers = [x for x in objects if isinstance(x, Tower) and x.owner == PLAYER2]
    estimated_data = {}
    real_data = {}

    # Fill data dict with the Towers in play
    for x in objects:
        if isinstance(x, Unit):
            break
        estimated_data.update(x, x.hp - x.queue)
        real_data.update(x, x.hp)



    # Estimate the total value of towers
    # See if friendly troops are adding to the value or if enemy troops are subtracting
    for x in objects:
        if isinstance(x, Unit):
            if x.target.owner == x.owner:
                estimated_data[x.target] += x.hp
            else:
                estimated_data[x.target] -= x.hp
        elif isinstance(x, Tower) and x.target != None:
            if x.target.owner == x.owner:
                estimated_data[x.target] += x.queue
            else:
                estimated_data[x.target] -= x.queue

    necessity = []
    hvts = []
    trouble = []
    orders = {}


    for tower, estimated_hp in estimated_data.items():
        if tower.owner == PLAYER2:
            pass