import pygame

from support import load_image
from debug import debug


class Gate(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # загрузка спрайтов
        self.image = load_image("graphics/temp/gate.png")

        # настройка квадрата спрайта для того что бы пуля спавнилась там где надо
        self.rect = self.image.get_rect(topleft=pos)
        self.first_pos = self.rect.y

        self.openning = False

        self.speed = 1

    def open(self):
        if self.openning and self.first_pos != self.rect.y + self.rect.height:
            self.openning = True
        else:
            self.openning = False

    def animate(self):
        if self.openning:

            self.rect.y -= self.speed

    def update(self, x_shift):
        debug(str(self.openning) + str(self.first_pos) + str(self.rect.y + self.rect.height))
        # движение камеры
        self.rect.x += x_shift
        self.open()
        self.animate()


