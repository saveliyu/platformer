import pygame
from image_button import ImageButton

class Transition():
    def __init__(self, screen):
        self.display_surface = screen
        self.buttons = pygame.sprite.Group()
        self.play = ImageButton((571, 414), "graphics/ui/level_transition/next_lvl.png", hot_key=pygame.K_RETURN)
        self.buttons.add(self.play)
        self.menu = ImageButton((452, 438), "graphics/ui/level_transition/menu.png")
        self.buttons.add(self.menu)
        self.restart = ImageButton((739, 438), "graphics/ui/level_transition/small_restart.png", hot_key=pygame.K_ESCAPE)
        self.buttons.add(self.restart)
        self.label = ImageButton((463, 228), "graphics/ui/level_transition/good_job.png")
        self.buttons.add(self.label)

    def get_status(self):
        if self.play.get_input():
            return 'game'
        elif self.menu.get_input():
            return 'levels'
        elif self.restart.get_input():
            return 'restart'
        else:
            return 'trans'
    def update(self):
        self.display_surface.fill((0, 0, 0, 150))
        self.buttons.draw(self.display_surface)