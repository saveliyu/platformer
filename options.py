import pygame
import webbrowser
import json
from image_button import ImageButton

class Options():
    def __init__(self, screen, music_volume, sfx_volume):
        self.sfx_volume = sfx_volume
        self.music_volume = music_volume

        self.display_surface = screen
        self.buttons = pygame.sprite.Group()
        self.labels = ImageButton((0, 0), "graphics/ui/options/labels.png")
        self.buttons.add(self.labels)
        self.restart = ImageButton((144, 504), "graphics/ui/options/restart.png")
        self.buttons.add(self.restart)
        self.web_page = ImageButton((798, 504), "graphics/ui/options/web_page.png")
        self.buttons.add(self.web_page)
        self.arrow_button = ImageButton((24, 24), "graphics/ui/options/arrow.png", hot_key=pygame.K_ESCAPE)
        self.buttons.add(self.arrow_button)

        self.music_bar = ImageButton((120, 336), "graphics/ui/options/bar.png")
        self.buttons.add(self.music_bar)
        self.music_slider = ImageButton((450, 330), "graphics/ui/options/slider.png")
        self.buttons.add(self.music_slider)
        self.music_filler = pygame.Rect((120, 336, 330, 18))

        self.sfx_bar = ImageButton((792, 336), "graphics/ui/options/bar.png")
        self.buttons.add(self.sfx_bar)
        self.sfx_slider = ImageButton((792 + 330, 330), "graphics/ui/options/slider.png")
        self.buttons.add(self.sfx_slider)
        self.sfx_filler = pygame.Rect((792, 336, 330, 18))

        self.set_velocity()


    def get_status(self):
        if self.web_page.get_input():
            webbrowser.open('https://itch.io/', new=1)
            return 'options'
        elif self.arrow_button.get_input():
            return "menu"
        elif self.restart.get_input():
            with open('saves.json') as saves:
                data = json.load(saves)
                data["current_level"] = 0
                data["max_level"] = 1
                data["watched_titry"] = 0
                data["music_volume"] = self.music_volume
                data["sfx_volume"] = self.sfx_volume
            with open('saves.json', 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return 'restart'
        else:
            return 'options'


    def set_velocity(self):
        self.sfx_slider.rect.x = self.sfx_volume * 330 + 792
        self.sfx_filler.width = self.sfx_slider.rect.x - 792
        self.music_slider.rect.x = self.music_volume * 330 + 120
        self.music_filler.width = self.music_slider.rect.x - 120
    def get_velocity(self, music_volume, sfx_volume):
        m_pos = self.music_bar.input_slider()
        s_pos = self.sfx_bar.input_slider()
        music_volume, sfx_volume = music_volume, sfx_volume
        if m_pos:
            self.music_slider.rect.x = list(m_pos)[0]
            if self.music_slider.rect.x > 450:
                self.music_slider.rect.x = 450
            music_volume = round((self.music_slider.rect.x - 120) / 330, 2)
            self.music_filler.width = self.music_slider.rect.x - 120
        if s_pos:
            self.sfx_slider.rect.x = list(s_pos)[0]
            if self.sfx_slider.rect.x > 792 + 330:
                self.sfx_slider.rect.x = 792 + 330
            sfx_volume = round((self.sfx_slider.rect.x - 792) / 330, 2)
            self.sfx_filler.width = self.sfx_slider.rect.x - 792
        return music_volume, sfx_volume

    def update(self):
        self.display_surface.fill("black")
        pygame.draw.rect(self.display_surface, 'white', self.music_filler)
        pygame.draw.rect(self.display_surface, 'white', self.sfx_filler)
        self.buttons.draw(self.display_surface)