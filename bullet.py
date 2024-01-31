import pygame

from support import import_sprite_sheet


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        # загрузка спрайтов
        self.import_bullet_assets()
        self.image = self.animations['player-shoot'][0]

        # настройка квадрата спрайта для того что бы пуля спавнилась там где надо
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += 32
        self.rect.x -= 6

        # настройка анимаций
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'player-shoot'

        # настройка скорости и направления
        self.direction = pygame.math.Vector2(direction, 0)
        self.speed = 8
        
        self.hit_sfx = pygame.mixer.Sound("sfx/hit.wav")

    def import_bullet_assets(self):
        # создание словаря со списками нарезанных по кадрово спрайтами
        character_path = "graphics/player/"
        self.animations = {'player-shoot': [], 'player-shoot-hit': []}

        for animation in self.animations.keys():
            full_path = character_path + animation + ".png"
            self.animations[animation] = import_sprite_sheet(full_path, 16)

    def animate(self):
        # текущая анимация
        animation = self.animations[self.status]

        # смена кадров
        self.frame_index += self.animation_speed

        # если пуля проиграла анимация попадания, то она уничтожается
        if self.frame_index >= len(animation) and self.status == 'player-shoot-hit':
            self.kill()
        # циклическая анимация если пуля летит
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # текуший кадр
        image = animation[int(self.frame_index)]
        # разворот спрайта если пуля летит в лево
        if self.direction.x == 1:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def update(self, x_shift):
        self.animate()
        # движение камеры
        self.rect.x += x_shift

        # если пуля не врезалась то она летит
        if self.status == 'player-shoot':
            self.rect.x += self.direction.x * self.speed
