import pygame

class BaseObject(pygame.sprite.Sprite):
    def __init__(self, initial_x:int, initial_y:int, debug:bool = False):
        """Constructor for the object class in the game"""

        #Store the coordinates
        self.x = initial_x
        self.y = initial_y
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.changed = True
        self.debug = debug

        #Call the superclass
        super().__init__()

    def get_coord(self) -> tuple:
        """Get the coordinates of the object"""
        return (self.x, self.y)

    def get_x(self) -> int:
        """Get the x coord of the obj"""
        return self.x

    def get_y(self) -> int:
        """Get the y coord of the obj"""
        return self.y

    def set_coord(self,position):
        """Set the coordinates of the base object"""
        self.x = position[0]
        self.y = position[1]