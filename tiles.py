import pygame
from support import load_image


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        # загружает изображение тайла в зависимости от символа в level_map
        if type == "block":
            self.image = load_image("graphics/temp/block.png")
        elif type == "ladder":
            self.image = load_image("graphics/temp/ladder.png")
        elif type == "lava":
            self.image = load_image("graphics/temp/lava.png")

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        # реализация "камеры"
        self.rect.x += x_shift
