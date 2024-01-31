import pygame
import json

from settings import *
from menu import Menu
from levels import Levels
from level import Level
from pause import Pause
from debug import debug

class Manager():
    def __init__(self, screen):
        self.current_scene = 'menu'
        with open('saves.json') as saves:
            data = json.load(saves)
            self.current_level = data["current_level"]
            self.max_level = data["max_level"]
        print(self.max_level, self.current_level)
        self.levels = Levels(screen, self.max_level, self.current_level)
        self.menu = Menu(screen)
        self.pause = Pause(screen)
        self.screen = screen
        self.import_levels()

    def import_levels(self):
        self.loaded_levels = [Level(level_map[0], self.screen),
                            Level(level_map[1], self.screen),
                            Level(level_map[2], self.screen)]

    def save_results(self):
        with open('saves.json') as saves:
            data = json.load(saves)
            data["current_level"] = self.current_level
            data["max_level"] = self.max_level

        with open('saves.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(data)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and self.current_scene == 'game':
            self.current_scene = "pause"

    def restart_level(self):
        self.loaded_levels[self.current_level] = Level(level_map[self.current_level], self.screen)

    def update(self):
        self.input()

        if self.current_scene == 'restart' or self.current_scene == 'level':
            self.restart_level()
            self.current_scene = 'game'

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
        elif self.current_scene == 'pause':
            print(self.pause.get_status())
            self.current_scene = self.pause.get_status()
            self.pause.update()
        debug(self.current_scene)
