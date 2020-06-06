import pygame
try:
    from .Object import Object
except ImportError:
    from Object import Object

class ImageObject(Object):
    def __init__(self, initial_x:int, initial_y:int, width:int, height:int, image = None, debug:bool = False):
        """Main class for all objects with images
            Arguments:
                initial_x: initial X position of the MovingObject (int)
                initial_y: initial Y position of the MovingObject (int)
                width: Width of the image in terms of pixels (int)
                height: Height of the image in terms of pixels (int)
                debug: Toggles debug mode (bool)

            Methods:
                load_rect: Load the rectangle of the MovingObject
                rotate: Rotate the sprite
                get_center: Get the center coordinate of the object
                scale: Scale the image of the sprite
                get_height: Get the height of the image
                get_width: Get the width of image
        """
        #Call superclass
        super().__init__(initial_x, initial_y, debug)

        #Get width
        self.width = width
        self.height = height

        #Check if the image path is None
        self.image = image

        #Load the rect
        self.load_rect()

    def load_rect(self) -> None:
        """Load the rectangle for the obj
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #If image exists
        if self.image:
            #Create the rectangle for the ImageObject Object
            self.rect = pygame.Rect(self.image.get_rect().left, self.image.get_rect().top, self.get_width(), self.get_height())

        #If image does not exists
        else:

            #Create custom rect
            self.rect = pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height())

            #Print debug message
            if self.debug:
                print("No image found")

            #Inflate the model to the correct size
            self.rect.inflate(self.get_width()//2,self.get_height()//2)
        
        #Set the center of the rect
        self.rect.center = (self.x,self.y)

        

    def get_center(self) -> tuple:
        """Get the coordinate of the center of the object
            Arguments:
                No arguments
            Returns: 
                Returns the center coordinate of the object
        """
        return self.rect.center

    def rotate(self, angle:int) -> None:
        """Rotate the image by x degrees
            Arguments:
                Angle: Rotate by angle degrees (int)
            Returns: 
                No return
        """
        #If the image exists
        if self.image:

            #Rotate the image
            self.image = pygame.transform.rotate(self.image, angle)
        
        #Otherwise do nothing
        else:
            if self.debug:
                print("There is no image to rotate")

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
        
        #If the image exists
        if self.image:

            #Scale the image to the new width and height defined
            self.image = pygame.transform.scale(self.image, (width, height))

            #Reload the rect
            self.load_rect()

        #Otherwise do nothing
        else:
            if self.debug:
                print("No image to scale")
            

    def get_height(self) -> None:
        """Get the height of the image
            Arguments:
                No arguments
            Returns: 
                Return the height of the image (int)
        """
        return self.image.get_height() if self.image else self.height

    def get_width(self) -> None:
        """Get the width of the image
            Arguments:
                No arguments
            Returns: 
                Return the width of the image (int)
        """
        return self.image.get_width() if self.image else self.width