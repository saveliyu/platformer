import pygame

from settings import tile_size, screen_width
from tiles import Tile
from player import Player
from button import Button
from ui import Clue
from gate import Gate

class Level:
    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.speed = 0
        self.current_x = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.ui = pygame.sprite.Group()
        self.gates = pygame.sprite.Group()


        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "X":
                    tile = Tile((x, y), tile_size, "block")
                    self.tiles.add(tile)
                elif cell == "L":
                    tile = Tile((x, y), tile_size, "ladder")
                    self.ladders.add(tile)
                elif cell == "T":
                    tile = Tile((x, y), tile_size, "lava")
                    self.traps.add(tile)
                elif cell == "G":
                    gate = Gate((x, y))
                    self.gates.add(gate)
                elif cell == "B":
                    button = Button((x, y))
                    self.buttons.add(button)
                elif cell == "P":
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width // 4 and direction_x < 0:
            self.world_shift = 3
            player.speed = 0
        elif player_x > screen_width - screen_width // 4 and direction_x > 0:
            self.world_shift = -3
            player.speed = 0
        else:
            self.counter = 0
            self.world_shift = 0
            player.speed = 3

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        bullets = player.bullets.sprites()
        self.ui = pygame.sprite.Group()

        for sprite in self.buttons.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.enable:
                but_e = Clue((sprite.rect.x + 30, sprite.rect.y - 50), "e_button.png")
                if player.button_press():
                    for gate in self.gates.sprites():
                        gate.openning = True
                    sprite.turn_on()
                self.ui.add(but_e)


        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
            for bullet in bullets:
                if sprite.rect.colliderect(bullet.rect):
                    bullet.status = 'player-shoot-hit'
                    bullet.hit_sfx.play()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
            for bullet in bullets:
                if sprite.rect.colliderect(bullet.rect):
                    bullet.status = 'player-shoot-hit'
        flag = False
        for sprite in self.ladders.sprites():
            if sprite.rect.colliderect(player.rect):
                flag = True
        if flag:
            player.on_ladder = True
        else:
            player.on_ladder = False

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        sprites = [*self.tiles.sprites(), *self.traps.sprites()]
        for sprite in sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.ladders.update(self.world_shift)
        self.ladders.draw(self.display_surface)
        self.traps.update(self.world_shift)
        self.traps.draw(self.display_surface)
        self.buttons.update(self.world_shift)
        self.buttons.draw(self.display_surface)
        self.ui.update(self.world_shift)
        self.ui.draw(self.display_surface)
        self.gates.update(self.world_shift)
        self.gates.draw(self.display_surface)
        self.scroll_x()

        # player
        self.horizontal_movement_collision()
        self.vertical_movement_collision( )
        self.player.update(self.world_shift)
        self.player.draw(self.display_surface)
