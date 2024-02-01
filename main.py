import pygame
import sys

from settings import *

from support import load_image

from level_manager import Manager

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
load = load_image('graphics/ui/load/load.png', scaling=6)
screen.blit(load, (0, 0))
pygame.display.update()
level = Manager(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    level.update()

    pygame.display.update()
    clock.tick(60)
