import pygame
from image_button import ImageButton

class Menu():
    def __init__(self, screen):
        self.display_surface = screen
        self.buttons = pygame.sprite.Group()
        self.levels = ImageButton((728, 240), "graphics/ui/main_menu/levels.png", hot_key=pygame.K_RETURN)
        self.buttons.add(self.levels)
        self.options = ImageButton((728, 336), "graphics/ui/main_menu/options.png")
        self.buttons.add(self.options)
        self.exit = ImageButton((728, 432), "graphics/ui/main_menu/exit.png", hot_key=pygame.K_ESCAPE)
        self.buttons.add(self.exit)
        self.frame = 0
        self.import_player()

    def import_player(self):
        self.player = pygame.sprite.GroupSingle()
        self.player_icon = ImageButton((248, 264), "graphics/player/spin.png", hot_key=pygame.K_RETURN, frames=5, sizex=32)
        self.player.add(self.player_icon)

    def animate_player(self):
        self.frame -= 0.05
        if self.frame <= -8:
            self.frame = 0
        self.player.sprite.image = self.player.sprite.frames[int(self.frame)]

    def get_status(self):
        if self.levels.get_input():
            return 'levels'
        elif self.options.get_input():
            return 'options'
        elif self.exit.get_input():
            return 'exit'
        else:
            return 'menu'
    def update(self):
        self.display_surface.fill("black")
        self.animate_player()
        self.buttons.draw(self.display_surface)
        self.player.draw(self.display_surface)