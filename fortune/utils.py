import pygame

def hex_to_color(hex: str) -> pygame.Color:
    return pygame.Color(tuple(int(hex[x:x+2], 16) for x in range(0, 6, 2)))