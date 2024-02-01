import pygame
from random import randint
from support import load_image, import_folder, import_sprite_sheet


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        # загружает изображение тайла в зависимости от символа в level_map
        if type == "block":
            self.image = load_image("graphics/temp/block.png")
        elif type == "ladder":
            self.image = load_image("graphics/temp/ladder.png")
        elif type == "lava":
            if list(pos)[1] == 672:
                self.image = load_image("graphics/temp/lava2.png")
            else:
                self.image = load_image("graphics/temp/lava.png")
        elif type == "end":
            self.image = load_image("graphics/temp/end.png")

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        # реализация "камеры"
        self.rect.x += x_shift


class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, size, x, y, path):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Coin(pygame.sprite.Sprite):
    def __init__(self, size, pos, path, value):
        super().__init__()
        self.frames = import_sprite_sheet(path, 14)
        self.current_frame = randint(0, 10)

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.value = value

    def animate(self):
        self.current_frame += 0.1
        if self.current_frame > 20:
            self.current_frame = 0
        if self.current_frame < 11:
            self.image = self.frames[int(self.current_frame)]
        else:
            self.image = self.frames[0]
    def update(self, shift):
        self.animate()
        self.rect.x += shift


class TileEmpty(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift
