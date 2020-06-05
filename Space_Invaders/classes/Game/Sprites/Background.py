import pygame
try:
    from .ImageObject import ImageObject
except ImportError:
    from ImageObject import ImageObject

class Background(ImageObject):
    #To store the background sprites
    sprites = []

    def __init__(self, bg_no:int, game_width:int, game_height:int, limit:int, debug:bool = False):
        """Constructor for the background class
            Arguments:
                bg_no: Background number to be used (int)
                game_width: Width of the game in pixels (int)
                game_height: Height of the game in pixels (int)

            Methods:
                is_present: Checks if any backgrounds are present
                update: Update the background
            
        """
        #Check if the background number is valid
        if bg_no < len(Background.sprites):

            #Set image to the correct background image
            image = Background.sprites[bg_no - 1]

        #Otherwise set background to default
        else:

            #Set the image to none
            image = False

        #Calls the superclass
        super().__init__(0, 0, game_width, game_height, image, debug)

        #Store variables
        self.game_width = game_width
        self.game_height = game_height
        self.bg_limit = limit

        #Gets the background image if any
        self.rect = None
        self.bg_no = bg_no

        #Generate the rect
        self.generate_rect()

    def cycle(self) -> None:
        """Cycle to the next background"""
        #Check if the bg is under the limit
        if self.bg_no < self.bg_limit:
            
            #If so add 1 to the current number to cycle the background
            self.bg_no += 1
        else:

            #Other wise go back to the first one
            self.bg_no = 1

        self.choose(self.bg_no)
        
    def is_present(self) -> bool:
        """Check if there is a valid background
            Arguments:
                No arguments
            Returns: 
                Returns a boolean showing if an image is available
        """
        return True if self.image else False

    def generate_rect(self) -> None:
        """Generate the rectangle"""

        #Scale the image to the correct size
        self.image = pygame.transform.scale(self.image, (self.game_width, self.game_height))

        #Get the rect
        self.rect = self.image.get_rect()

        #Set the top left of rect to top left of the game
        self.rect.left, self.rect.top = 0,0

    def get_bg_no(self) -> int:
        """Get the background number"""
        return self.bg_no

    def choose(self, bg_no:int) -> None:
        """Choose a background"""

        #If an image exists before
        if not self.image:
            return None

        #Get the sprite for new background
        self.image = Background.sprites[bg_no - 1]

        #Save the bg number
        self.bg_no = bg_no

        #Generate rect
        self.generate_rect()

    def update(self, screen) -> None:
        """Blit the background to the screen
            Arguments:
                screen: Screen to draw the background onto (pygame.Surface)
            Returns: 
                No return
        """
        screen.blit(self.image, self.rect)