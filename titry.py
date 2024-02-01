import pygame
from image_button import ImageButton
from debug import debug

class Titry():
    def __init__(self, screen):
        self.display_surface = screen

        self.speed = 1
        self.timer = 300

        self.titry = pygame.sprite.GroupSingle()
        self.words = ImageButton((0, 0), "graphics/ui/titry.png")
        self.titry.add(self.words)

    def get_end(self):
        if self.timer <= 0:
            return 'menu'
        else:
            return 'titry'

    def update(self):
        self.titry.update(self.speed)
        self.display_surface.fill((0, 0, 0, 150))
        self.titry.draw(self.display_surface)
        if self.titry.sprite.rect.y < -3050:
            self.timer -= 1
            self.speed = 0


