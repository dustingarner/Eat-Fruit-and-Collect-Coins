from pathlib import Path
import pygame

def create_sound(file_name: str) -> pygame.mixer.Sound:
    data_folder = Path("Assets/Sounds/")
    sound_file = data_folder / file_name
    return pygame.mixer.Sound(sound_file)