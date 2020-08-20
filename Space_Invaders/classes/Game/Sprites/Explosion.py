import pygame

from . import ImageObject


class Explosion(ImageObject):
    # Init for the sound
    sound = None

    # To store the sprites for the explosions
    sprites = []

    def __init__(self, tick_life: int, initial_x: int, initial_y: int, game_width: int, game_height: int,
                 image_no: int = 0, debug: bool = False):
        """The main class for the explosion"""

        # Get the correct image of the explosion
        if image_no < len(Explosion.sprites):
            image = Explosion.sprites[image_no]
        else:
            image = Explosion.sprites[0]

        # Call the superclass method
        super().__init__(initial_x, initial_y, game_width, game_height, image, debug)

        # Play it
        self.sound.play('explosion')

        # Set the time to live for the explosion
        self.tts = tick_life

    def update(self):
        """Update the explosion"""

        # If the explosion still has time to live
        if self.tts:

            # Decrease time to live
            self.tts -= 1

        # Otherwise kill it
        else:
            self.kill()

        # Call the superclass update method
        super().update()
