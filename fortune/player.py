import pygame
import fortune.collision as collision
import fortune.items as items
import fortune.utils as utils

class Player:
    def __init__(self):
        self.position = pygame.Vector2(400, 300)
        self.scale = pygame.Vector2(48, 48)
        self.hitbox = collision.Hitbox(self.position, self.scale)
        self.color = utils.hex_to_color("8338EC")
        self.speed = 300
    
    def move(self, delta):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2()
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if not direction == pygame.Vector2(0, 0):
            direction = direction.normalize()
        velocity = direction * self.speed * delta
        self.position += velocity
        self.hitbox.update_rectangle(self.position, self.scale)

    def rect_dimensions(self) -> pygame.Rect:
        return pygame.Rect(self.position, self.scale)

    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect_dimensions())

    def within_bounds(self, position: pygame.Vector2) -> bool:
        rect = self.rect_dimensions()
        x_in_bound = (position.x < rect.right) and \
                (position.x > rect.left)
        y_in_bound = (position.y < rect.bottom) and \
                (position.y > rect.top)
        return x_in_bound and y_in_bound

    def attempt_collect(self, coin: items.Coin) -> bool:
        return self.hitbox.collides_circle(coin.hitcircle)


