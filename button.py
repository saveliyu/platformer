import pygame

from support import import_sprite_sheet


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, enable=True):
        super().__init__()

        self.enable = enable

        # загрузка спрайтов
        self.import_button_assets()
        self.image = self.animation[0]

        # настройка квадрата спрайта для того что бы пуля спавнилась там где надо
        self.rect = self.image.get_rect(topleft=pos)
        self.press_sfx = pygame.mixer.Sound("sfx/buttonpress.wav")

    def import_button_assets(self):
        # создание словаря со списками нарезанных по кадрово спрайтами
        character_path = "graphics/temp/button.png"
        self.animation = import_sprite_sheet(character_path, 16)

    def turn_on(self):
        self.enable = False
        self.press_sfx.play()

    def update(self, x_shift):
        if self.enable:
            self.image = self.animation[0]
        else:
            self.image = self.animation[1]
        # движение камеры
        self.rect.x += x_shift

