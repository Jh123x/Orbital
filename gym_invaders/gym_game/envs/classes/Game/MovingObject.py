import pygame

class MovingObject(pygame.sprite.Sprite):
    """Main class for all objects that move"""
    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, game_width:int, game_height:int, debug:bool):
        """Constructor class for the moving object
            Arguments:
                sensitivity: Sensitivity of the moving object (int)
                initial_x: initial X position of the MovingObject (int)
                initial_y: initial Y position of the MovingObject (int)
                game_width: Width of the game in terms of pixels (int)
                game_height: Height of the game in terms of pixels (int)
                debug: Toggles debug mode (bool)

            Methods:
                load_rect: Load the rectangle of the MovingObject
                move: Move the object by (x,y)
                rotate: Rotate the sprite
                move_up: Make the sprite move up
                move_down: Make the sprite move down
                move_left: Make the sprite move left
                move_right: Make the sprite move right
                get_x: Get the x coordinate of the object
                get_y: Get the y coordinate of the object
                get_center: Get the center coordinate of the object
                update: Update the moving object
                scale: Scale the image of the sprite
                get_height: Get the height of the image
                get_width: Get the width of image
        """
        #Call the superclass init method
        super().__init__()

        #Storing the variables
        self.x = initial_x
        self.y = initial_y
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.game_width = game_width
        self.game_height = game_height
        self.debug = debug
        self.sensitivity = sensitivity
        self.changed = True

        #Load the rect
        self.load_rect()

    def load_rect(self) -> None:
        """Load the rectangle for the obj
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #Create the rectangle for the MovingObject Object
        self.rect = pygame.Rect(self.image.get_rect().left, self.image.get_rect().top, self.get_width(), self.get_height())
        self.rect.center=(self.x,self.y)

        #Inflate the model to the correct size
        self.rect.inflate(self.get_width()//2,self.get_height()//2)

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

    def get_coord(self) -> tuple:
        """Get the coordinates of the object"""
        return (self.x, self.y)

    def rotate(self, angle:int) -> None:
        """Rotate the image by x degrees
            Arguments:
                Angle: Rotate by angle degrees (int)
            Returns: 
                No return
        """
        self.image = pygame.transform.rotate(self.image, angle)

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

    def get_x(self) -> int:
        """Get the x coord of the obj
            Arguments:
                No arguments
            Returns: 
                Returns the x coordinate of the mob
        """
        return self.x

    def get_center(self) -> tuple:
        """Get the coordinate of the center of the object
            Arguments:
                No arguments
            Returns: 
                Returns the center coordinate of the object
        """
        return self.rect.center

    def get_y(self) -> int:
        """Get the y coord of the obj
            Arguments:
                No arguments
            Returns: 
                Returns the y coordinate of the mob
        """
        return self.y

    def update(self) -> None:
        """Update the object rect position
            Arguments:
                No arguments
            Returns: 
                No return
        """

        #Set the position of the rect if it has changed from before
        if self.changed:

            #Load the rectangle of the object again
            self.load_rect()

            #Set the changed variable to False
            self.changed = False

    def scale(self, width:int, height:int) -> None:
        """Scale the image
            Arguments:
                No arguments
            Returns: 
                No return
        """
        
        #Scale the image to the new width and height defined
        self.image = pygame.transform.scale(self.image, (width, height))

        #Reload the rect
        self.load_rect()

    def get_height(self) -> None:
        """Get the height of the image
            Arguments:
                No arguments
            Returns: 
                Return the height of the image (int)
        """
        return self.image.get_height()

    def get_width(self) -> None:
        """Get the width of the image
            Arguments:
                No arguments
            Returns: 
                Return the width of the image (int)
        """
        return self.image.get_width()