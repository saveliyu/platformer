import pygame
import sys

from settings import *
# from level import Level
from level1 import Level1
from game_data import level_1

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# level = Level(level_map, screen)
level1 = Level1(level_1, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('#151123')
    level1.run()

    pygame.display.update()
    clock.tick(60)
