import pygame
from . import ImageObject


class MovingObject(ImageObject):
    """Main class for all objects that move"""
    
    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, game_width:int, game_height:int, image, debug:bool , sprite_size:tuple = (50,50)):
        """Constructor class for the moving object"""

        #Call the superclass init method (Sprites set to 50x50)
        super().__init__(initial_x, initial_y, *sprite_size, image, debug)

        #Storing the variables
        self.game_width = game_width
        self.game_height = game_height
        self.sensitivity = sensitivity
        self.changed = True

    def move(self, x:int, y:int) -> None:
        """Main Move Method"""
        #Add the values to x and y to change position
        self.x += x
        self.y += y

        #Informed that rect has changed
        self.changed = True

    def move_up(self, length:int = None) -> None:
        """Move the object up"""
        return self.move(0,-length if length else -self.sensitivity)

    def move_down(self, length:int = None) -> None:
        """Move the object down"""
        return self.move(0,length if length else self.sensitivity)

    def move_left(self, length:int = None) -> None:
        """Move the object right"""
        return self.move(-length if length else -self.sensitivity,0)

    def move_right(self, length:int = None) -> None:
        """Move the object right"""
        return self.move(length if length else self.sensitivity,0)
