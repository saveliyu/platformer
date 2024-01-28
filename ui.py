import pygame

from support import load_image, import_sprite_sheet
from settings import screen_width

class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # загрузка спрайтов
        self.pos = (10, 10)
        self.import_states()
        self.image = self.health_states[0]
        self.energy_bar = self.energy_states[0]
        self.image.blit(self.energy_bar, (0, 44))
        self.rect = self.image.get_rect(topleft=self.pos)

    def import_states(self):
        self.health_states = import_sprite_sheet("graphics/ui/health_bar.png", 32, scaling=4)
        self.energy_states = import_sprite_sheet("graphics/ui/energy_bar.png", 32, scaling=4)

    def update_states(self, health, bullets):
        health = int(health * 3)
        bullets = int(bullets)
        self.image = self.health_states[len(self.health_states) - health - 1]
        self.energy_bar = self.energy_states[len(self.energy_states) - bullets - 1]
        self.image.blit(self.energy_bar, (0, 44))
        self.rect = self.image.get_rect(topleft=self.pos)

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