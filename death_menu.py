import pygame
from image_button import ImageButton

class Death():
    def __init__(self, screen):
        self.display_surface = screen
        self.buttons = pygame.sprite.Group()
        self.restart = ImageButton((571, 414), "graphics/ui/level_transition/restart.png", hot_key=pygame.K_RETURN)
        self.buttons.add(self.restart)
        self.menu = ImageButton((452, 438), "graphics/ui/level_transition/menu.png")
        self.buttons.add(self.menu)
        self.label = ImageButton((463, 228), "graphics/ui/level_transition/try_again.png")
        self.buttons.add(self.label)

    def get_status(self):
        if self.menu.get_input():
            return 'levels'
        elif self.restart.get_input():
            return 'restart'
        else:
            return 'death'
    def update(self):
        self.display_surface.fill((0, 0, 0, 150))
        self.buttons.draw(self.display_surface)