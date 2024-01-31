import pygame
from image_button import ImageButton

class Pause():
    def __init__(self, screen):
        self.display_surface = screen
        self.buttons = pygame.sprite.Group()
        self.play = ImageButton((571, 293), "graphics/ui/level_transition/next_lvl.png")
        self.buttons.add(self.play)
        self.menu = ImageButton((452, 317), "graphics/ui/level_transition/menu.png")
        self.buttons.add(self.menu)
        self.restart = ImageButton((739, 317), "graphics/ui/level_transition/small_restart.png")
        self.buttons.add(self.restart)

    def get_status(self):
        if self.play.get_input():
            return 'game'
        elif self.menu.get_input():
            return 'levels'
        elif self.restart.get_input():
            return 'restart'
        else:
            return 'pause'

    def update(self):
        self.display_surface.fill("black")
        self.buttons.draw(self.display_surface)