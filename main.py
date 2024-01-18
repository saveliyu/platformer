import pygame
import sys

from settings import *
from level import Level
from support import load_image

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)
game_over = load_image("graphics/ui/game_over.png", scaling=6)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if level.is_playing :
        level.run()
    else:
        x = (screen_width - game_over.get_width()) // 2
        y = (screen_height - game_over.get_height()) // 2
        screen.blit(game_over, (x, y))

    pygame.display.update()
    clock.tick(60)
