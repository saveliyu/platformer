import pygame
import sys

from settings import *

from support import load_image

from level_manager import Manager

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game_over = load_image("graphics/ui/game_over.png", scaling=6)
level = Manager(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    level.update()
    pygame.display.update()
    clock.tick(60)
