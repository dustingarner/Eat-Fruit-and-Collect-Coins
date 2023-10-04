import math
import pygame

class Hitbox:
    def __init__(self, location: pygame.Vector2, size: pygame.Vector2):
        self.rectangle = pygame.Rect(location, size)
        self.center = pygame.Vector2(location.x + (size.x / 2), location.y + (size.y / 2))
    
    def update_rectangle(self, location: pygame.Vector2, size: pygame.Vector2):
        self.rectangle = pygame.Rect(location, size)
        self.center = pygame.Vector2(location.x + (size.x / 2), location.y + (size.y / 2))
        
    def collides_box(self, other_box) -> bool:
        return self.rectangle.colliderect(other_box.rectangle)

    def collides_circle(self, other_circle) -> bool:
        point_on_circle = other_circle.closest_point(pygame.Vector2(self.rectangle.center))
        clip = self.rectangle.clipline(other_circle.position, point_on_circle)
        return len(clip) > 0


class Hitcircle:
    def __init__(self, position: pygame.Vector2, radius: int):
        self.position = position
        self.radius = radius

    def update_circle(self, position: pygame.Vector2, radius: int):
        self.position = position
        self.radius = radius
    
    def closest_point(self, point: pygame.Vector2) -> pygame.Vector2:
        angle = math.atan2(point.x - self.position.x, point.y - self.position.y)
        cosine, sine = math.cos(angle), math.sin(angle)
        x, y = cosine * self.radius, sine * self.radius
        point = pygame.Vector2(x + self.position.x, y + self.position.y)
        return point

    def collides_box(self, other_box) -> bool:
        return other_box.collides_circle(self)
