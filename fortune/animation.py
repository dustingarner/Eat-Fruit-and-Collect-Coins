import math
from pathlib import Path
from PIL import Image
import pygame



class AnimInfo:
    def __init__(self, file_name: str, frame_count: tuple):
        self.file = Path("Assets/Images/") / file_name
        self.frame_count = frame_count

class Animation:
    def __init__(self, anim_info):
        self.anim_info = anim_info
        self.image_info = Image.open(self.anim_info.file)
        self.frame_width = math.floor(self.image_info.width / self.anim_info.frame_count[0])
        self.frame_height = math.floor(self.image_info.height / self.anim_info.frame_count[1])
        self.sprite_sheet = pygame.image.load(self.anim_info.file).convert()

    def get_image(self, frame: tuple) -> pygame.Surface:
        rect_location = (self.frame_width * frame[0], self.frame_height * frame[1])
        rect_size = (self.frame_width, self.frame_height)
        image = pygame.Surface(rect_size).convert()
        image.blit(self.sprite_sheet, (0, 0), (rect_location, rect_size))
        image.set_colorkey((0,0,0,0))
        return image

