import pygame
try:
    from .MovingObject import MovingObject
except ImportError:
    from MovingObject import MovingObject

class Explosion(MovingObject):

    #To store the sprites for the explosions
    sprites = []

    def __init__(self, sprite:pygame.sprite.Sprite, tick_life:int, initial_x:int, initial_y:int, game_width:int, game_height:int, image_no:int = 0, debug:bool = False):
        """The main class for the explosion"""

        #Set the time to live for the explosion
        self.tts = tick_life

        #Get the correct image of the explosion
        if image_no < len(Explosion.sprites):
            self.image = Explosion.sprites[image_no]
        else:
            self.image = Explosion.sprites[0]

        #Call the superclass method
        super().__init__(0, initial_x, initial_y, game_width, game_height, debug)


    def update(self):
        """Update the explosion"""
        #If the explosion still has TTS
        if self.tts:
            self.tts -= 1
        
        #Otherwise kill it
        else:
            self.kill()

        #Call the superclass update method
        super().update()