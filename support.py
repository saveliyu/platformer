import os
import sys

import pygame
from settings import scaling

def load_image(filename, scaling=scaling):
    # проверка на наличие файла
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    sheet = pygame.image.load(filename).convert_alpha()
    # увеличение изображение в х раз что бы не было слишком мелко
    sheet = pygame.transform.scale(sheet, (sheet.get_width() * scaling, sheet.get_height() * scaling))
    return sheet

def import_sprite_sheet(path, sizex, scaling=scaling):
    sizex *= scaling

    sheet = load_image(path, scaling=scaling)

    # по кадровое "вырезание" из спрайтщита
    rect = pygame.Rect(0, 0, sizex, sheet.get_height())
    frames = []
    for i in range(sheet.get_width() // sizex):
        frame_location = (rect.w * i, 0)
        frames.append(sheet.subsurface(pygame.Rect(
            frame_location, rect.size)))
    return frames


