from pathlib import Path
from enum import Enum
import random
import math
import pygame
import fortune.collision as collision
import fortune.player as player
import fortune.items as items
import fortune.utils as utils
import fortune.animation as animation
import fortune.audio as audio


#Yellow: FFBE0B
#Orange: FB5607
#Pink: FF006E
#Purple: 8338EC
#Blue: 3A86FF
#https://coolors.co/palette/ffbe0b-fb5607-ff006e-8338ec-3a86ff



class AllSounds(Enum):
    COIN_COLLECT = 0

class AllAnims(Enum):
    CHARACTER = 0
    



anim_dict = {
    AllAnims.CHARACTER: animation.AnimInfo("Character.png", (11, 1)),
    
}

sound_dict = {
    AllSounds.COIN_COLLECT: "CoinCollect.wav"
    }



class GameLoop:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.player = player.Player()
        self.coin_adder = items.ItemAdder(item_type = items.Coin, frequency_range = (1, 3), \
                screen = self.screen, screen_size = self.screen_size)
        self.fruit_adder = items.ItemAdder(item_type = items.Fruit, frequency_range = (1, 3), \
                screen = self.screen, screen_size = self.screen_size)

    def process(self, delta):
        self.screen.fill("black")

        self.coin_adder.process(delta)
        self.fruit_adder.process(delta)

        self.move_coins(delta)
        self.move_fruits(delta)
        self.move_player(delta)
        self.draw_player()
        pygame.display.flip()
    

    def reset_counter(self, frame_count):
        self.coin_adder.reset_counter(frame_count)
        self.fruit_adder.reset_counter(frame_count)


    def attempt_add_coin(self, frame_count):
        if not self.coin_adder.can_add(frame_count):
            return
        self.coins.append(items.Coin(self.screen_size))

    def move_coins(self, delta):
        for coin in self.coins.copy():
            if coin.off_screen(self.screen_size):
                self.remove_coin(coin)
                continue
            if self.player.attempt_collect(coin):
                self.remove_coin(coin)
                sound = audio.create_sound(sound_dict[AllSounds.COIN_COLLECT])
                sound.play()
                continue
            
    def remove_coin(self, coin):
        self.coins.remove(coin)
        del coin

    def move_fruits(self, delta):
        for fruit in self.fruits.copy():
            self.screen.blit(pygame.transform.scale(fruit.animate(delta), (128, 128)), fruit.center)
    
    

    def move_player(self, delta):
        self.player.move(delta)
    
    def draw_player(self):
        self.player.draw_player(self.screen)



def main():
    pygame.init()
    screen_size = pygame.Vector2(800, 600)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    delta = 0

    running = True

    game_loop = GameLoop(screen, screen_size)

    counter = 0
    max_frames = 500000
    while running:
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if counter >= max_frames:
            game_loop.reset_counter(counter)
            counter -= max_frames

        game_loop.process(counter, delta)
        delta = clock.tick(60) / 1000
    pygame.quit()




if __name__ == "__main__":
    main()

