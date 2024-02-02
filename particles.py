import pygame
from support import import_folder, import_sprite_sheet

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self, pos, type):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 0.5
		# if type == 'jump':
		# 	self.frames = import_folder('../graphics/character/dust_particles/jump')
		# if type == 'land':
		# 	self.frames = import_folder('../graphics/character/dust_particles/land')
		if type == 'explosion':
			self.frames = import_sprite_sheet('graphics/temp/pick2.png', 16)
			pos = (list(pos)[0], list(pos)[1] + 16)
			self.animation_speed = 0.2
		if type == 'pick':
			self.frames = import_sprite_sheet('graphics/temp/pick.png', 16)
			self.animation_speed = 0.15
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center=pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift
