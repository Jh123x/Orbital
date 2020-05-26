import pygame
try:
    from .ImageObject import ImageObject
except ImportError:
    from ImageObject import ImageObject

class Explosion(ImageObject):

    #To store the sprites for the explosions
    sprites = []

    def __init__(self, tick_life:int, initial_x:int, initial_y:int, game_width:int, game_height:int, image_no:int = 0, debug:bool = False):
        """The main class for the explosion
            Arguments:
                tick_life: How long the sprite is lasting in terms of ticks (int)
                initial_x: Initial x position of the explosion (int)
                initial_y: Initial y position of the explosion (int)
                game_width: Width of the game in pixels (int)
                game_height: Height of the game in pixels (int)
                image_no: Which explosion image to use (int): default = 0
                debug: Toggle debug mode (bool): default = False

            Methods:
                update: Update the position of the sprite
        """

        #Get the correct image of the explosion
        if image_no < len(Explosion.sprites):
            image = Explosion.sprites[image_no]
        else:
            image = Explosion.sprites[0]

        #Call the superclass method
        super().__init__(initial_x, initial_y, game_width, game_height, image, debug)

        #Set the time to live for the explosion
        self.tts = tick_life


    def update(self):
        """Update the explosion
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #If the explosion still has time to live
        if self.tts:
            self.tts -= 1
        
        #Otherwise kill it
        else:
            self.kill()

        #Call the superclass update method
        super().update()