import os
import sys
from csv import reader
import pygame
from settings import scaling, tile_size
from os import walk

def import_folder(path):
	surface_list = []

	for _,__,image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def load_image(filename):
    # проверка на наличие файла
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    sheet = pygame.image.load(filename).convert_alpha()
    # увеличение изображение в х раз что бы не было слишком мелко
    sheet = pygame.transform.scale(sheet, (sheet.get_width() * scaling, sheet.get_height() * scaling))
    return sheet

def import_sprite_sheet(path, sizex):
    sizex *= scaling

    sheet = load_image(path)

    # по кадровое "вырезание" из спрайтщита
    rect = pygame.Rect(0, 0, sizex, sheet.get_height())
    frames = []
    for i in range(sheet.get_width() // sizex):
        frame_location = (rect.w * i, 0)
        frames.append(sheet.subsurface(pygame.Rect(
            frame_location, rect.size)))
    return frames

def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_cut_graphics(path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / (tile_size * scaling))
	tile_num_y = int(surface.get_size()[1] / (tile_size * scaling))

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * (tile_size * scaling)
			y = row * (tile_size * scaling)
			new_surf = pygame.Surface(((tile_size * scaling),(tile_size * scaling)),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,(tile_size * scaling),(tile_size * scaling)))
			cut_tiles.append(new_surf)

	return cut_tiles

