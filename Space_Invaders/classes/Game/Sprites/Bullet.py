from . import MovingObject
from .. import *

class Bullet(MovingObject):

    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, direction:Direction, game_width:int, game_height:int, debug:bool = False):
        """The constructor for the bullet class
            Arguments:
                sensitivity: Sensitivity of the bullets (int)
                initial_x: Initial x position of the bullet (int)
                initial_y: Initial y position of the bullet (int)
                direction: Direction of bullet (Direction)
                game_width: Width of the game in pixels (int)
                game_height: Height of the game in pixels (int)
                debug: Toggles debug mode (bool): default = False

            Methods:
                update: Update the position of the bullet
            
        """
        #Play the shoot sound
        self.sound.play('shooting')

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height,self.sprites[0], debug)

        #Store the direction, move up it the enum is move up, else move it down
        if direction == Direction.UP:
            self.direction = self.move_up
        elif direction == Direction.DOWN:

            #If there is another sprite, use that sprite for down instead
            if len(Bullet.sprites) >= 2:
                self.image = self.sprites[1]
            
            #Set the direction to down
            self.direction = self.move_down

        else:

            #Otherwise it is invalid
            assert False, "Direction of bullet is invalid"

       
    def update(self) -> None:
        """Update the path of the bullet
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #Move the bullet
        self.direction()

        #Kill itself if the bullet is out of screen
        if self.y > self.game_height or self.y < 0:

            #Kill the object
            self.kill()

            #Do not continue to update position
            return

        #Update its coordinates
        return super().update()