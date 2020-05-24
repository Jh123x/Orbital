import pygame
try:
    from .ImageObject import ImageObject
except ImportError:
    from ImageObject import ImageObject

class MovingObject(ImageObject):
    """Main class for all objects that move"""
    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, game_width:int, game_height:int, image_path:str, debug:bool):
        """Constructor class for the moving object
            Arguments:
                sensitivity: Sensitivity of the moving object (int)
                initial_x: initial X position of the MovingObject (int)
                initial_y: initial Y position of the MovingObject (int)
                game_width: Width of the game in terms of pixels (int)
                game_height: Height of the game in terms of pixels (int)
                debug: Toggles debug mode (bool)

            Methods:
                move: Move the object by (x,y)
                move_up: Make the sprite move up
                move_down: Make the sprite move down
                move_left: Make the sprite move left
                move_right: Make the sprite move right
                update: Update the moving object

        """
        #Call the superclass init method (Sprites set to 50x50)
        super().__init__(initial_x, initial_y, 50, 50, image_path, debug)

        #Storing the variables
        self.game_width = game_width
        self.game_height = game_height
        self.sensitivity = sensitivity
        self.changed = True

    def move(self, x:int, y:int) -> None:
        """Main Move Method
            Arguments:
                x: move x by this amount (int)
                y: move y by this amount (int)
            Returns: 
                No return
        """
        #Add the values to x and y to change position
        self.x += x
        self.y += y

        #Informed that rect has changed
        self.changed = True

    def move_up(self, length:int = None) -> None:
        """Move the object up
            Arguments:
                length (optional): Move up by x pixels or sensitivity is used if not specified
            Returns: 
                No return
        """
        return self.move(0,-length if length else -self.sensitivity)

    def move_down(self, length:int = None) -> None:
        """Move the object down
            Arguments:
                length (optional): Move down by x pixels or sensitivity is used if not specified
            Returns: 
                No return
        """
        return self.move(0,length if length else self.sensitivity)

    def move_left(self, length:int = None) -> None:
        """Move the object right
            Arguments:
                length (optional): Move left by x pixels or sensitivity is used if not specified
            Returns: 
                No return
        """
        return self.move(-length if length else -self.sensitivity,0)

    def move_right(self, length:int = None) -> None:
        """Move the object right
            Arguments:
                length (optional): Move right by x pixels or sensitivity is used if not specified
            Returns: 
                No return
        """
        return self.move(length if length else self.sensitivity,0)
