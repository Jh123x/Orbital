import pygame
from . import BaseObject
from .. import YELLOW

class Block(BaseObject):
    def __init__(self, initial_x:int, initial_y:int, screen, color:tuple = YELLOW, debug:bool = False):
        """Class for individual blocks in block group"""

        #Call the superclass
        super().__init__(initial_x, initial_y, debug)

        #Dimentions of the block
        self.screen = screen
        self.width = 10
        self.height = 10

        #Create the rect for the block
        self.rect = pygame.Rect(initial_x - self.width//2, initial_y - self.height//2, self.width, self.height)

        #Store color of the block
        self.color = color

        #Draw the image of the block
        self.image = pygame.Surface((self.rect.w, self.rect.h))

        #Set the block to be yellow color
        self.image.fill(YELLOW)

    def get_rect(self) -> pygame.Rect:
        """Get the Rect containing the block"""
        return self.rect

    def destroy(self) -> None:
        """Destroy the block"""
        self.kill()

        
        