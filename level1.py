import pygame

from settings import tile_size, screen_width
from player import Player
from button import Button
from ui import Clue
from gate import Gate
from support import import_csv_layout
from tiles import StaticTile, Tile, AnimatedTile
from support import import_cut_graphics
from player import Player
from enemy import Enemy

class Level1:
    def __init__(self, level_data, surface):
        # level setup
         # level setup
        self.display_surface = surface
        self.world_shift = 0
        self.speed = 0
        self.current_x = 0

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #stairs setup 
        stairs_layout = import_csv_layout(level_data['stairs'])
        self.stairs_sprites = self.create_tile_group(stairs_layout, 'stairs')

        # player 
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # ciuns
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")

        # enemy
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")

        # constraint 
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')


    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/temp/Terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'stairs':
                        stairs_tile_list = import_cut_graphics('graphics/temp/Terrain_tiles.png')
                        tile_surface = stairs_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    if type == 'coins':
                        sprite = AnimatedTile(tile_size,x,y,'graphics/coins')
                    
                    if type == "enemies":
                        sprite = Enemy(tile_size,x,y)

                    if type == "constraint":
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group    
    
    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)
                    
                if val == '1':
                    hat_surface = pygame.image.load('graphics/player/idle.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        bullets = player.bullets.sprites()
        self.ui = pygame.sprite.Group()

        ladders = self.stairs_sprites.sprites()
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                but_e = Clue((sprite.rect.x + 30, sprite.rect.y - 50), "e_button.png")
                if player.button_press():
                    for gate in self.gates.sprites():
                        gate.openning = True
                    sprite.turn_on()
                self.ui.add(but_e)

        for sprite in collidable_sprites:
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

        for sprite in collidable_sprites:
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
        for sprite in ladders:
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

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()
        
        for sprite in collidable_sprites:
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

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def run(self):
        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # stairs
        self.stairs_sprites.update(self.world_shift)
        self.stairs_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)    
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface) 
        

        # player
        self.player.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.scroll_x()