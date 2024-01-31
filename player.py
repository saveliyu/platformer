import pygame

from debug import debug
from support import import_sprite_sheet
from bullet import Bullet


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.import_character_assets()
        self.display_surface = screen
        self.frame_index = 0
        self.last_frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        # player movment
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 0.65
        self.jump_speed = -7

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.on_ladder = False
        self.is_shooting = False

        # bullets
        self.bullets = pygame.sprite.Group()

    def import_character_assets(self):
        character_path = "graphics/player/"
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [],
                        'ladder': [], 'damage': [], 'shoot': [], 'run-shoot': []}

        for animation in self.animations.keys():
            full_path = character_path + animation + ".png"
            self.animations[animation] = import_sprite_sheet(full_path, 32)

    def button_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            return True
        return False

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed

        if self.status == 'run-shoot' and int(abs(self.frame_index - self.maxindex)) == 0:
            self.shoot()
            self.is_shooting = False
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'run-shoot':
                self.maxindex -= 6
            elif self.status == 'shoot':
                self.shoot()
                self.is_shooting = False

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def shoot(self):
        if self.facing_right:
            bullet = Bullet(self.rect.topright, 1)
        else:
            bullet = Bullet(self.rect.topleft, -1)
        self.bullets.add(bullet)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.on_ladder:
            self.direction.y = -2
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if list(pygame.mouse.get_pressed())[0] and not self.is_shooting:
            self.is_shooting = True
            if self.direction.x == 0:
                self.frame_index = 0
            self.maxindex = self.frame_index + 5

        if keys[pygame.K_SPACE]:
            self.frame_index = 0
            if self.on_ground:
                self.jump()

    def get_status(self):
        if self.is_shooting and self.direction:
            self.status = "run-shoot"
        elif self.is_shooting:
            self.status = "shoot"
        elif self.on_ladder and self.direction.y < 0:
            self.status = "ladder"
        elif self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 0:
            self.status = "fall"
        elif self.direction.x != 0:
            self.status = "run"
        else:
            self.status = "idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self, world_shift):
        self.bullets.draw(self.display_surface)
        self.bullets.update(world_shift)
        self.get_input()
        self.get_status()
        self.animate()
