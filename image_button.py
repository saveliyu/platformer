import pygame
from support import load_image, import_sprite_sheet


class ImageButton(pygame.sprite.Sprite):

    def __init__(self, pos, path, hot_key=None, frames=1, sizex=0):
        super().__init__()
        self.hot_key = hot_key
        if frames == 1:
            self.image = load_image(path, scaling=6)
        else:
            for i in range(frames):
                self.frames = import_sprite_sheet(path, sizex, scaling=6)
            self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)

    def get_input(self):
        keys = pygame.key.get_pressed()
        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image.set_alpha(180)
        else:
            self.image.set_alpha(255)
        if self.hot_key:
            if keys[self.hot_key]:
                return True
            elif pressed[0] and self.rect.collidepoint(pos):
                return True
        elif pressed[0] and self.rect.collidepoint(pos):
            return True
        else:
            return False

