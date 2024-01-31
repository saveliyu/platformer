import pygame
import json

from settings import *
from menu import Menu
from levels import Levels
from level import Level

class Manager():
    def __init__(self, screen):
        self.current_scene = 'menu'
        with open('saves.json') as saves:
            data = json.load(saves)
            self.current_level = data["current_level"]
            self.max_level = data["max_level"]
        print(self.max_level, self.current_level)
        self.levels = Levels(screen, self.max_level, self.current_level)
        self.import_levels(screen)
        self.menu = Menu(screen)

    def import_levels(self, screen):
        self.loaded_levels = [Level(level_map[0], screen),
                            Level(level_map[1], screen),
                            Level(level_map[2], screen)]

    def save_results(self):
        with open('saves.json') as saves:
            data = json.load(saves)
            data["current_level"] = self.current_level
            data["max_level"] = self.max_level

        with open('saves.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(data)

    def update(self):
        if self.current_scene == 'menu':
            self.current_scene = self.menu.get_status()
            self.menu.update()
        elif self.current_scene == 'levels':
            self.current_scene, self.current_level = self.levels.get_status()
            self.levels.update()
        elif self.current_scene == 'game':
            if self.loaded_levels[self.current_level].level_end():
                self.current_level += 1
                if self.max_level <= self.current_level:
                    self.max_level = self.current_level + 1
                self.save_results()
            self.loaded_levels[self.current_level].run()
            # x = (screen_width - game_over.get_width()) // 2
            # y = (screen_height - game_over.get_height()) // 2
            # screen.blit(game_over, (x, y))
