import pygame
from image_button import ImageButton


class Levels():
    def __init__(self, screen):
        self.max_levels = 5
        self.current_level = 0
        self.display_surface = screen
        self.import_buttons()
        self.import_player()
        self.import_pathes()

    def import_pathes(self):
        self.pathes = pygame.sprite.GroupSingle()
        self.path = ImageButton((0, 0), "graphics/ui/levels/pathes.png", frames=5, sizex=213)
        self.path.image = self.path.frames[self.max_levels - 1]
        self.pathes.add(self.path)

    def import_player(self):
        pos = (self.buttons.sprites()[self.current_level].rect.x + 78, self.buttons.sprites()[self.current_level].rect.y - 30)
        self.player = pygame.sprite.GroupSingle()
        self.player_icon = ImageButton(pos, "graphics/ui/levels/player.png")
        self.player.add(self.player_icon)

    def import_buttons(self):
        self.buttons = pygame.sprite.Group()
        self.level_1 = ImageButton((210, 138), "graphics/ui/levels/buttons.png", hot_key=pygame.K_RETURN, frames=5,sizex=13)
        self.buttons.add(self.level_1)
        self.level_2 = ImageButton((210, 462), "graphics/ui/levels/buttons.png", hot_key=pygame.K_RETURN, frames=5,sizex=13)
        self.level_2.image = self.level_2.frames[1]
        self.buttons.add(self.level_2)
        self.level_3 = ImageButton((600, 462), "graphics/ui/levels/buttons.png", hot_key=pygame.K_RETURN, frames=5,sizex=13)
        self.level_3.image = self.level_3.frames[2]
        self.buttons.add(self.level_3)
        self.level_4 = ImageButton((600, 282), "graphics/ui/levels/buttons.png", hot_key=pygame.K_RETURN, frames=5,sizex=13)
        self.level_4.image = self.level_4.frames[3]
        self.buttons.add(self.level_4)
        self.level_5 = ImageButton((978, 282), "graphics/ui/levels/buttons.png", hot_key=pygame.K_RETURN, frames=5,sizex=13)
        self.level_5.image = self.level_5.frames[4]
        self.buttons.add(self.level_5)
        self.arrow_button = ImageButton((24, 24), "graphics/ui/levels/arrow.png", hot_key=pygame.K_ESCAPE)
        self.buttons.add(self.arrow_button)

    def choose_level(self):
        keys = pygame.key.get_pressed()
        if self.current_level == 0:
            if keys[pygame.K_s] and self.max_levels > 1:
                self.current_level = 1
        elif self.current_level == 1:
            if keys[pygame.K_d] and self.max_levels > 2:
                self.current_level = 2
            elif keys[pygame.K_w]:
                self.current_level = 0
        elif self.current_level == 2:
            if keys[pygame.K_w] and self.max_levels > 3:
                self.current_level = 3
            elif keys[pygame.K_a]:
                self.current_level = 1
        elif self.current_level == 3:
            if keys[pygame.K_d] and self.max_levels > 4:
                self.current_level = 4
            elif keys[pygame.K_s]:
                self.current_level = 2
        elif self.current_level == 4:
            if keys[pygame.K_a]:
                self.current_level = 3

    def get_status(self):
        if self.buttons.sprites()[self.current_level].get_input():
            return 'game', self.current_level
        elif self.buttons.sprites()[-1].get_input():
            return 'menu', self.current_level
        return "levels", self.current_level

    def update(self):
        self.display_surface.fill("black")
        self.choose_level()
        pos = (self.buttons.sprites()[self.current_level].rect.x + 78, self.buttons.sprites()[self.current_level].rect.y - 30)
        self.player.sprite.rect.topleft = pos
        self.buttons.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.pathes.draw(self.display_surface)