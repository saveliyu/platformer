import pygame
from support import load_image, import_folder



class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        # загружает изображение тайла в зависимости от символа в level_map
        if type == "block":
            self.image = load_image("graphics/temp/block.png")
        elif type == "ladder":
            self.image = load_image("graphics/temp/ladder.png")
        elif type == "lava":
            self.image = load_image("graphics/temp/lava.png")

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        # реализация "камеры"
        self.rect.x += x_shift

class AnimatedTile(pygame.sprite.Sprite):
	def __init__(self,size,x,y,path):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))
		
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.animate()
		self.rect.x += shift
            
class Coin(AnimatedTile):
	def __init__(self,size,x,y,path,value):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value
		
class TileEmpty(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,shift):
		self.rect.x += shift