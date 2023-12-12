import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, x=10, y=10):
    """это просто что бы дебажить было удобно
    выводит в углу экрана любой текст"""
    display_surf = pygame.display.get_surface()

    text = font.render(str(info), True, "white")
    text_rect = text.get_rect(topleft=(x, y))
    display_surf.blit(text, text_rect)

