import pygame

#Init pygame
pygame.init()

class Object(pygame.sprite.Sprite):
    def __init__(self, initial_x:int, initial_y:int, debug:bool = False):
        """Constructor for the object class in the game
            Arguments:
                initial_x: Initial x position of object (int)
                initial_y: Initial y position of object(int)
                debug: Toggles debug mode (bool): default = False
            Methods:
                get_x: Get the x coordinate of the object
                get_y: Get the y coordinate of the object
                get_coord: Get the coordinates of object in x and y
        """

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
        """Get the coordinates of the object
            Arguments:
                No arguments
            Returns: 
                Returns the x,y coordinate of the object
        """
        return (self.x, self.y)

    def get_x(self) -> int:
        """Get the x coord of the obj
            Arguments:
                No arguments
            Returns: 
                Returns the x coordinate of the object
        """
        return self.x

    def get_y(self) -> int:
        """Get the y coord of the obj
            Arguments:
                No arguments
            Returns: 
                Returns the y coordinate of the mob
        """
        return self.y