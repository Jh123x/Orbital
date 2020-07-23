from . import MovingObject
from .. import Direction

class Bullet(MovingObject):

    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, direction:Direction, game_width:int, game_height:int, debug:bool = False):
        """The constructor for the bullet class"""

        #Play the shoot sound
        self.sound.play('shooting')

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height,self.sprites[0], debug)

        #Store bullet direction
        self.direction = direction.value
       
    def update(self) -> None:
        """Update the path of the bullet"""
        #Move the bullet
        self.move(self.direction[0] * self.sensitivity, self.direction[1] * self.sensitivity)

        #Kill itself if the bullet is out of screen
        if self.y > self.game_height or self.y < 0:

            #Kill the object
            self.kill()

            #Do not continue to update position
            return

        #Make the bullet able to bounce along the x axis
        elif self.x <= 0 or self.x >= self.game_width:

            #Set the bullet direction to opposite in x axis
            self.direction = tuple(map(lambda x: x*self.sensitivity, self.direction))
            

        #Update its coordinates
        return super().update()