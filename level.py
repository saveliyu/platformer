import pygame

from settings import tile_size, screen_width, scaling
from tiles import Tile, Coin, AnimatedTile, TileEmpty
from enemy import Enemy
from player import Player
from button import Button
from ui import Clue
from gate import Gate
from ui import StatusBar
from particles import ParticleEffect

from debug import debug

class Level:
    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.speed = 0
        self.current_x = 0
        self.invulnerability_timer = 0
        self.import_sounds()

    def import_sounds(self):
        self.collect_sfx = pygame.mixer.Sound("sfx/collect2.wav")
        self.collect_sfx.set_volume(0.5)
        self.death_sfx = pygame.mixer.Sound("sfx/death.wav")
        self.death_sfx.set_volume(0.5)

    def setup_level(self, layout):
        self.is_playing = True

        self.tiles = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.ui = pygame.sprite.Group()
        self.gates = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.constraint = pygame.sprite.Group()

        self.explosion_sprites = pygame.sprite.Group()

        self.end_tile = pygame.sprite.GroupSingle()

        self.statusbar = pygame.sprite.Group()
        statusbar = StatusBar()
        self.statusbar.add(statusbar)

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
                elif cell == "K":
                    tile = Tile((x, y), tile_size, "end")
                    self.end_tile.add(tile)
                elif cell == "G":
                    gate = Gate((x, y))
                    self.gates.add(gate)
                elif cell == "B":
                    button = Button((x, y))
                    self.buttons.add(button)
                elif cell == "P":
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)
                elif cell == "C":
                    tile = Coin(tile_size, (x, y - 20), 'graphics/temp/battery.png', 1)
                    self.coins.add(tile)
                elif cell == "E":
                    tile = Enemy(tile_size,x,y)
                    self.enemy.add(tile)
                elif cell == "O":
                    tile = Tile((x, y), tile_size, "lava")
                    self.constraint.add(tile)


        if self.player.sprite.rect.x >= screen_width:
            self.world_shift_update(-self.player.sprite.rect.x + screen_width // 2)
            self.player.sprite.rect.x += -self.player.sprite.rect.x + screen_width // 2
            self.player.sprite.rect.x += -self.player.sprite.rect.x + screen_width // 2


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width // 4 and direction_x < 0:
            if self.tiles.sprites()[0].rect.x < 0:
                self.world_shift = 3
                player.speed = 0
            else:
                self.world_shift = 0
                player.speed = 3
        elif player_x > screen_width - screen_width // 4 and direction_x > 0:
            if self.tiles.sprites()[-1].rect.x + tile_size > screen_width:
                self.world_shift = -3
                player.speed = 0
            else:
                self.world_shift = 0
                player.speed = 3
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

        # проверка на соударение со стенами
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

        # проверка на соударение с врагами
        for sprite in self.enemy.sprites():
            if sprite.rect.colliderect(player.rect):
                if self.invulnerability_timer <= 0:
                    self.invulnerability_timer = 50
                    player.health_point -= 4

            # ударение пуль
            for bullet in bullets:
                if sprite.rect.colliderect(bullet.rect):
                    bullet.status = 'player-shoot-hit'
                    explosion_sprite = ParticleEffect(sprite.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    self.death_sfx.play()
                    self.enemy.remove(sprite)

        # сбор патронов
        for coin in self.coins.sprites():
            if coin.rect.colliderect(player.rect):
                player.bullets_count += 1
                if player.bullets_count > 17:
                    player.bullets_count = 17
                # print("colide coin", player.bullets_count)
                self.coins.remove(coin)
                self.collect_sfx.play()
                explosion_sprite = ParticleEffect(coin.rect.center, 'pick')
                self.explosion_sprites.add(explosion_sprite)
                    

        flag = False
        for sprite in self.ladders.sprites():
            if sprite.rect.colliderect(player.rect):
                flag = True
        if flag:
            player.on_ladder = True
        else:
            player.on_ladder = False

        for sprite in self.end_tile.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.status != 'eblanit' and player.status != 'spin':
                    player.powerup_sfx.play()
                    player.status = 'spin'

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        sprites = self.tiles.sprites()
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

        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.direction.y = 1
                    player.health_point = 0
                    if not player.is_drowned:
                        player.is_drowned = True
                        player.drown_sfx.play()
                    else:
                        player.drown_timer -= 1
                    if player.drown_timer <= 0:
                        self.is_playing = False


        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def enemy_collision_reverse(self):
        for en in self.enemy.sprites():
            if pygame.sprite.spritecollide(en,self.constraint,False):
                en.reverse()

    def level_end(self):
        if self.player.sprite.status == 'eblanit':
            self.player.sprite.status = 'idle'
            return True
        else:
            return False

    def world_shift_update(self, shift):
        self.tiles.update(shift)
        self.ladders.update(shift)
        self.buttons.update(shift)
        self.ui.update(shift)
        self.gates.update(shift)
        self.traps.update(shift)
        self.coins.update(shift)
        self.end_tile.update(shift)

        self.explosion_sprites.update(shift)
        self.enemy.update(shift)
        self.constraint.update(shift)
        self.enemy_collision_reverse()

    def run(self):
        self.invulnerability_timer -= 1
        if not self.player.sprite.is_drowned and self.player.sprite.health_point <= 0:
            self.is_playing = False

        self.scroll_x()
        self.display_surface.fill('#151123')
        self.world_shift_update(self.world_shift)
        
        # level tiles
        self.tiles.draw(self.display_surface)
        self.ladders.draw(self.display_surface)
        self.buttons.draw(self.display_surface)
        self.ui.draw(self.display_surface)
        self.gates.draw(self.display_surface)
        self.coins.draw(self.display_surface)
        self.end_tile.draw(self.display_surface)
        
        # enemy
        self.enemy.draw(self.display_surface)
        self.explosion_sprites.draw(self.display_surface)

        # player
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.update(0)
        self.player.draw(self.display_surface)

        # traps
        self.traps.draw(self.display_surface)

        self.statusbar.sprites()[0].update_states(self.player.sprite.health_point, self.player.sprite.bullets_count)
        self.statusbar.draw(self.display_surface)

