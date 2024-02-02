import pygame

from debug import debug
from support import load_image
from bullet import Bullet


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, string):
        super().__init__()
        self.numbers = [load_image('graphics/ui/numbers/0.png', scaling=6),
                        load_image('graphics/ui/numbers/1.png', scaling=6),
                        load_image('graphics/ui/numbers/2.png', scaling=6),
                        load_image('graphics/ui/numbers/3.png', scaling=6),
                        load_image('graphics/ui/numbers/4.png', scaling=6),
                        load_image('graphics/ui/numbers/5.png', scaling=6),
                        load_image('graphics/ui/numbers/6.png', scaling=6),
                        load_image('graphics/ui/numbers/7.png', scaling=6),
                        load_image('graphics/ui/numbers/8.png', scaling=6),
                        load_image('graphics/ui/numbers/9.png', scaling=6)]
        self.surface = pygame.Surface(8 * 6 * len(string), 8 * 6)
        for num in enumerstring:
            self. = self.numbers[num]


    def update(self, world_shift):
        pass

