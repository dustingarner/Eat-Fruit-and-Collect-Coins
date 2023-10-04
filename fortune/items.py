import random
import pygame
import fortune.collision as collision
import fortune.animation as animation
import fortune.utils as utils

class ItemAdder:
    def __init__(self, frequency_range: tuple):
        self.prev_added = 0
        self.frequency_range = frequency_range
        self.next_add = self.compute_next_add()
    
    def can_add(self, frame_count) -> bool:
        if not (frame_count - self.prev_added) % self.next_add == 0:
            return False
        self.prev_added = frame_count
        self.next_add = self.compute_next_add()
        return True

    def compute_next_add(self) -> int:
        random.seed()
        return random.randint(self.frequency_range[0], self.frequency_range[1])
    
    def reset_counter(self, frame_count):
        self.prev_added -= frame_count
        self.next_add -= frame_count

class Coin:
    def __init__(self, screen_size):
        self.color = utils.hex_to_color("FFBE0B")
        self.boundary = 50
        self.radius = 6
        
        self.position = self.randomize_position(screen_size)
        self.direction = self.randomize_direction(screen_size)
        self.speed = self.randomize_speed()
        self.hitcircle = collision.Hitcircle(self.position, self.radius)
    
    def randomize_position(self, screen_size) -> pygame.Vector2:
        random.seed()
        position = pygame.Vector2()
        position.x = random.randint(self.boundary, screen_size.x - self.boundary)
        position.y = random.randint(self.boundary, screen_size.y - self.boundary)
        return position

    def randomize_direction(self, screen_size) -> pygame.Vector2:
        random.seed()
        direction = pygame.Vector2()
        if self.position.x > screen_size.x / 2:
            direction.x = 1
        else:
            direction.x = -1
        if self.position.y > screen_size.y / 2:
            direction.y = 1
        else:
            direction.y = -1
        direction = direction.normalize()
        offset = random.randint(-45, 45)
        direction = direction.rotate(offset)
        return direction

    def randomize_speed(self) -> int:
        random.seed()
        return random.randint(50, 100)

    def off_screen(self, screen_size) -> bool:
        if self.position.x - self.radius > screen_size.x:
            return True
        elif self.position.x + self.radius < 0:
            return True
        elif self.position.y - self.radius > screen_size.y:
            return True
        elif self.position.y + self.radius < 0:
            return True
        return False

    def move(self, delta):
        self.position += self.direction * self.speed * delta
        self.hitcircle.update_circle(self.position, self.radius)

    def draw_coin(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
    
    def __del__(self):
        pass


class Fruit:
    def __init__(self, fruit, screen_size):
        self.animation = animation.Animation(fruit)
        self.boundary = 50
        self.counter = 0
        self.frame = 0
        self.position = self.randomize_position(screen_size)
        self.center = pygame.Vector2(self.position.x + 32, self.position.y + 32)

    def randomize_position(self, screen_size) -> pygame.Vector2:
        random.seed()
        position = pygame.Vector2()
        position.x = random.randint(self.boundary, screen_size.x - self.boundary)
        position.y = random.randint(self.boundary, screen_size.y - self.boundary)
        return position

    def animate(self, delta: float) -> pygame.Surface:
        image = self.animation.get_image((self.frame, 0))

        if self.counter * delta > 0.05:
            self.counter = 0
            self.frame += 1
        if self.frame >= self.animation.anim_info.frame_count[0]:
            self.frame = 0
        self.counter += 1
        return image