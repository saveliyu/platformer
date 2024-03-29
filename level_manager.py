import pygame
import json

from settings import *
from menu import Menu
from levels import Levels
from level import Level
from pause import Pause
from debug import debug
from death_menu import Death
from titry import Titry
from options import Options
from level_transition import Transition

class Manager():
    def __init__(self, screen):
        screen.fill('red')
        self.current_scene = 'menu'
        self.load_results()
        if self.current_level >= self.max_level:
            self.current_level = self.max_level - 1
        self.levels = Levels(screen, self.max_level, self.current_level)
        self.menu = Menu(screen)
        self.pause = Pause(screen)
        self.trans = Transition(screen)
        self.death = Death(screen)
        self.titry = Titry(screen)
        self.options = Options(screen, self.music_volume, self.sfx_volume)
        self.screen = screen
        self.import_levels()



        self.sound_track = pygame.mixer.Sound("sfx/sound_track.wav")
        self.sound_track.set_volume(self.music_volume)
        self.sound_track.play(loops=True)

    def import_levels(self):
        self.loaded_levels = [Level(level_map[0], self.screen, self.sfx_volume),
                            Level(level_map[1], self.screen, self.sfx_volume),
                            Level(level_map[2], self.screen, self.sfx_volume),
                            Level(level_map[3], self.screen, self.sfx_volume),
                            Level(level_map[4], self.screen, self.sfx_volume)]

    def load_results(self):
        with open('saves.json') as saves:
            data = json.load(saves)
            self.current_level = data["current_level"]
            self.max_level = data["max_level"]
            self.watched_titry = data["watched_titry"]
            self.music_volume = data["music_volume"]
            self.sfx_volume = data["sfx_volume"]

    def save_results(self):
        with open('saves.json') as saves:
            data = json.load(saves)
            data["current_level"] = self.current_level
            data["max_level"] = self.max_level
            data["watched_titry"] = self.watched_titry
            if self.watched_titry:
                data["max_level"] = 5
                self.max_level = 5
            data['music_volume'] = self.music_volume
            data['sfx_volume'] = self.sfx_volume
        with open('saves.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and self.current_scene == 'game':
            self.current_scene = "pause"

    def restart_level(self):
        self.loaded_levels[self.current_level] = Level(level_map[self.current_level], self.screen, self.sfx_volume)

    def update(self):
        if self.current_level >= self.max_level:
            self.current_level = self.max_level - 1
        self.input()

        if self.current_scene == 'restart' or self.current_scene == 'level':
            self.restart_level()
            self.current_scene = 'game'

        if self.loaded_levels[self.current_level].level_end() and self.current_scene == 'game':
            self.current_level += 1
            if self.max_level <= self.current_level:
                self.max_level = self.current_level + 1
            self.save_results()
            self.levels.max_levels = self.max_level
            if self.max_level > len(self.loaded_levels):
                self.max_level = len(self.loaded_levels) - 1
                self.current_level = 0
                if not self.watched_titry:
                    self.current_scene = 'titry'
            else:
                self.current_scene = 'trans'

        if self.current_scene == 'menu':
            self.current_scene = self.menu.get_status()
            self.menu.update()
        elif self.current_scene == 'levels':
            if self.watched_titry:
                self.levels.max_levels = 5
            else:
                self.levels.max_levels = self.max_level
            self.current_scene, self.current_level = self.levels.get_status()
            if self.current_scene == 'game':
                self.restart_level()
            self.levels.update()
        elif self.current_scene == 'game':
            self.loaded_levels[self.current_level].update_volume()
            self.loaded_levels[self.current_level].player.sprite.update_volume()
            self.loaded_levels[self.current_level].run()
            if not self.loaded_levels[self.current_level].is_playing:
                self.current_scene = 'death'
        elif self.current_scene == 'trans':
            self.current_scene = self.trans.get_status()
            if self.current_level == 'levels':
                self.restart_level()
            self.trans.update()
        elif self.current_scene == 'pause':
            self.current_scene = self.pause.get_status()
            self.pause.update()
        elif self.current_scene == 'death':
            self.current_scene = self.death.get_status()
            self.death.update()
        elif self.current_scene == 'titry':
            self.current_scene = self.titry.get_end()
            if self.current_scene == 'menu':
                self.watched_titry = 1
                self.save_results()
            self.titry.update()
        elif self.current_scene == 'options':
            self.current_scene = self.options.get_status()
            self.music_volume, self.sfx_volume = self.options.get_velocity(self.music_volume, self.sfx_volume)
            if self.current_scene == 'restart':
                self.load_results()
                self.save_results()
                self.levels.current_level = self.current_level
                self.current_scene = 'options'
            self.sound_track.set_volume(self.music_volume)
            self.loaded_levels[self.current_level].volume = self.sfx_volume
            self.loaded_levels[self.current_level].player.sprite.volume = self.sfx_volume
            self.options.update()


