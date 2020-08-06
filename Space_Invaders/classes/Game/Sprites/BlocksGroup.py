import pygame
from . import Block

class BlockGroup(pygame.sprite.Group):
    def __init__(self, game_width:int, game_height:int, total_length:int, initial_y:int, screen, number:int, debug:bool = False):
        """The constructor class for the Block group"""

        #Call the superclass
        super().__init__()

        #Create the group of blocks based on x and y and add them to the group
        for k in range(number):
            for i in range(-1,2):
                for j in range(-2,3):
                    self.add(Block(game_width, game_height, int(total_length * (k+1) // (number+1) + 10 * j * game_width/600), int(initial_y + 10 * i * game_height/800), screen, debug))

        
        