from classes.tower import Tower
from classes.unit import Unit
from constants import PLAYER1, PLAYER2, ATTACK, DEFEND, AI_ATTACK_MAX


player2_towers = []
estimated_data = {}


def get_optimal_tower(target : Tower, action : str) -> list:
    """"""

    towers = []

    if action == ATTACK:
        # Sort PLAYER2 towers. Lower hp up front
        sorted_player2_towers = sorted(player2_towers, key=lambda x: x.hp)

        # Find tower with lowest amt marginally
        for tower in sorted_player2_towers:
            if tower.hp > target.hp + AI_ATTACK_MAX and estimated_data[tower] >= tower.hp:
                return [tower]
        
        # If no single tower could attack safely, find towers that can add together
        sorted_player2_towers.reverse()
        troops = 0
        for i in range(0, len(sorted_player2_towers)):
            troops += sorted_player2_towers[i].hp
            towers.append(player2_towers[i])
            if troops > target.hp + AI_ATTACK_MAX:
                return towers
    
    elif action == DEFEND:
        # Sort towers to get lowest estimated hp first
        sorted_player2_towers = sorted(player2_towers, key=lambda x: estimated_data[x])

        # Find tower with the lowest amt marginally
        for tower in sorted_player2_towers:
            if tower == target:
                continue
            if tower.hp + estimated_data[target] >= 0:
                return [tower]

        # If no single tower could defend, find towers that can add together
        sorted_player2_towers.reverse()
        troops = 0
        for i in range(0, len(sorted_player2_towers)):
            troops += sorted_player2_towers[i].hp
            towers.append(player2_towers[i])
            if troops + estimated_data[target] >= 0:
                return towers

    # Default decision
    return None



def ai_decision(objects : list = None):
    """"""
    global player2_towers
    
    # First, check if action must happen
    no_player2_towers_units = all(item.owner != PLAYER2 for item in objects)
    if no_player2_towers_units:
        return

    # Fix player2_towers to have only towers without an activity and owned by PLAYER2
    player2_towers = [x for x in objects if isinstance(x, Tower) and x.owner == PLAYER2 and not x.target]
    estimated_data.clear()

    # Fill data dict with the Towers in play
    for x in objects:
        if isinstance(x, Unit):
            break
        estimated_data.update({x: x.hp - x.queue})


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


    # Make decision to attack or defend
    for tower, estimated_hp in estimated_data.items():
        if tower.owner != PLAYER2:
            attacker = get_optimal_tower(tower, ATTACK)
            # If a tower(s) should attack, make it/them attack
            if attacker:
                for x in attacker:
                    x.prep_troops(tower)

        else:
            if estimated_hp < 0:
                defender = get_optimal_tower(tower, DEFEND)
                # If a tower(s) should defend, make it/them defend
                if defender:
                    for x in defender:
                        x.prep_troops(tower)


