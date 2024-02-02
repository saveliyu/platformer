import pygame 
from tiles import AnimatedTile
from random import randint
from bullet import Bullet, BulletEnemy

class Enemy(AnimatedTile):
	def __init__(self,size,x,y, style):
		self.style = style
		if style == "skelet":
			self.speed = -(randint(20,30) / 10)
			self.path = "graphics/enemies/skeleton/skeleton-walk"
			super().__init__(size, x, y, self.path)
			self.rect.y += size - self.image.get_size()[1]
		elif style == "bat":
			self.speed = -(randint(30,40) / 10)
			self.path = "graphics/enemies/bat"
			super().__init__(size, x, y, self.path)
			self.rect.y += size - self.image.get_size()[1] + 30




	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed < 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()

class EnemyDragonеTurret(AnimatedTile):
	def __init__(self,size,x,y,dir,screen):
		super().__init__(size,x,y,'graphics/enemies/lizard-shoot')
		self.rect.y += size - self.image.get_size()[1]
		self.display_surface = screen
		self.bullets = pygame.sprite.Group()
		self.shoot_flag = False
		self.dir = dir

		self.is_shooting = True
		

	def reverse_image(self):
		if self.dir == 1:
			self.image = pygame.transform.flip(self.image,True,False)

	def shoot(self):
		if self.frame_index == 11.100000000000016:
			bullet = BulletEnemy((self.rect.x, self.rect.y + 16), self.dir)
			self.bullets.add(bullet)
		
	def update(self,shift):
		self.rect.x += shift
		
		self.shoot()
		self.bullets.draw(self.display_surface)
		self.bullets.update(shift)
		self.animate()
		self.reverse_image()