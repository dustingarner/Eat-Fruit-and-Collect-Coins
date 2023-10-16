import random
from enum import Enum
import pygame
import fortune.collision as collision
import fortune.animation as animation
import fortune.utils as utils
import fortune.observer as observer



class ItemAdder:    
    def __init__(self, item_type, frequency_range: tuple, screen, screen_size):
        self.item_type = item_type
        self.item_list = []
        self.frequency_range = frequency_range
        self.screen = screen
        self.screen_size = screen_size

        self.WAIT_SPEED = 200
        self.wait_counter = 0
        self.wait_time = 0
        self.reset_wait()

        self.remover = observer.Observer(self.remove_item)


    def reset_wait(self) -> int:
        self.wait_counter = 0
        random.seed()
        self.wait_time = random.randint(self.frequency_range[0], self.frequency_range[1])
    
    def add_item(self):
        new_item = self.item_type(self.screen, self.screen_size)
        self.item_list.append(new_item)
        new_item.remove_subject.add_observer(self)
        self.reset_wait()

    def can_add(self) -> bool:
        return self.wait_counter >= self.wait_time

    def remove_item(self, item):
        if item in self.item_list:
            self.item_list.remove(item)
        del item

    def process(self, delta) -> bool:
        if self.can_add():
            self.add_item()
            return
        self.wait_counter += self.WAIT_SPEED * delta



class MovementDirection:
    def __init__(self, position, screen_size):
        self.position = position
        self.direction = self.make_direction(screen_size)
    
    def make_direction(self, screen_size) -> pygame.Vector2:
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



class Coin:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.color = utils.hex_to_color("FFBE0B")
        self.boundary = 50
        self.radius = 6
        
        self.position = self.randomize_position(screen_size)
        self.direction = MovementDirection(position = self.position, screen_size = self.screen_size)
        self.speed = self.randomize_speed()
        self.hitcircle = collision.Hitcircle(self.position, self.radius)

        self.remove_subject = observer.Subject()
    
    def randomize_position(self) -> pygame.Vector2:
        random.seed()
        position = pygame.Vector2()
        position.x = random.randint(self.boundary, self.screen_size.x - self.boundary)
        position.y = random.randint(self.boundary, self.screen_size.y - self.boundary)
        return position

    def randomize_speed(self) -> int:
        random.seed()
        return random.randint(50, 100)

    def remove_self(self):
        self.remove_subject.notify(self)


    def off_screen(self) -> bool:
        if self.position.x - self.radius > self.screen_size.x:
            return True
        elif self.position.x + self.radius < 0:
            return True
        elif self.position.y - self.radius > self.screen_size.y:
            return True
        elif self.position.y + self.radius < 0:
            return True
        return False

    def move(self, delta):
        self.position += self.direction.direction * self.speed * delta
        self.hitcircle.update_circle(self.position, self.radius)

    def draw_coin(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.radius)
    
    def process(self, delta):
        self.move(delta)
        self.draw_coin()



class FruitTypes(Enum):
    APPLE = 0
    BANANA = 1
    CHERRY = 2
    KIWI = 3
    MELON = 4
    ORANGE = 5
    PINEAPPLE = 6

class Fruit:
    def __init__(self, screen, screen_size):
        self.animation = self.make_animation()
        self.boundary = 50
        self.position = self.randomize_position(screen_size)
        self.center = pygame.Vector2(self.position.x + 32, self.position.y + 32)

    def randomize_position(self, screen_size) -> pygame.Vector2:
        random.seed()
        position = pygame.Vector2()
        position.x = random.randint(self.boundary, screen_size.x - self.boundary)
        position.y = random.randint(self.boundary, screen_size.y - self.boundary)
        return position
    
    def animate(self, delta) -> pygame.Surface:
        return self.animation.animate(delta)
    
    def make_animation(self) -> animation.Animation:
        animations = {
        FruitTypes.APPLE: animation.AnimInfo("Apple.png", (17, 1)),
        FruitTypes.BANANA: animation.AnimInfo("Bananas.png", (17, 1)),
        FruitTypes.CHERRY: animation.AnimInfo("Cherries.png", (17, 1)),
        FruitTypes.KIWI: animation.AnimInfo("Kiwi.png", (17, 1)),
        FruitTypes.MELON: animation.AnimInfo("Melon.png", (17, 1)),
        FruitTypes.ORANGE: animation.AnimInfo("Orange.png", (17, 1)),
        FruitTypes.PINEAPPLE: animation.AnimInfo("Pineapple.png", (17, 1))
        }
        random.seed()
        fruit = random.randint(0, 6)
        anim_info = animations[FruitTypes(fruit)]
        return animation.Animation(anim_info = anim_info)
    


#FruitTypes.COLLECTED: animation.AnimInfo("Collected.png", (6, 1))
