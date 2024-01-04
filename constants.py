import pygame

pygame.init()

info = pygame.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h
BUFFER = 50
MIN_DISTANCE = 250

TOWER_WIDTH = 30
UNIT_WIDTH = 5
OUTLINE_WIDTH = 2

PAUSE_WIDTH = 300
PAUSE_HEIGHT = 200

FPS = 30

PLAYER1 = "1"
PLAYER2 = "2"
NEUTRAL = "3"

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (220,20,60)
GREY = (169,169,169)
BLUE = (100,149,237)
YELLOW = (255,255,102)

PLAYER_TOWER_HP = 25
NEUTRAL_TOWER_HP = 40
SPEED_TOWER_HP = 15
UNIT_HP_MAX = 5
SPAWN_DELAY = FPS / 2
GROW_MOD = 1.4

TOWERFONT = pygame.font.SysFont('Arial', 20)
UNITFONT = pygame.font.SysFont('Arial', 10)