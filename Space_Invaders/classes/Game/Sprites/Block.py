import pygame
from ..Colors import *
from . import *

class Block(Object):
    def __init__(self, initial_x:int, initial_y:int, screen, color:tuple = YELLOW, debug:bool = False):
        """Blocks"""

        #Call the superclass
        super().__init__(initial_x, initial_y, debug)

        #Dimentions of the block
        self.screen = screen
        self.width = 10
        self.height = 10

        #Create the rect for the block
        self.rect = pygame.Rect(initial_x - self.width//2, initial_y - self.height//2, self.width, self.height)
        self.color = color
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(YELLOW)

    def get_rect(self) -> pygame.Rect:
        """Get the Rect containing the block"""
        return self.rect

    def destroy(self) -> None:
        """Destroy the block"""
        self.kill()

        
        