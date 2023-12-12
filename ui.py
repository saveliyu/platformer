import pygame

from support import load_image


class Clue(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        # загрузка спрайтов
        self.image = load_image("graphics/temp/" + image)

        # настройка квадрата спрайта для того что бы кнопка спавнилась там где надо
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.width += 50

    def update(self, x_shift):
        self.rect.x += x_shift