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

        #If the bullet is suppose to move up
        if direction == Direction.UP:

            #Store the direction as up
            self.direction = self.move_up

        #If it is suppose to move down
        elif direction == Direction.DOWN:
            
            #If there is another sprite, use that sprite for down instead
            if len(Bullet.sprites) >= 2:
                self.image = self.sprites[1]
            
            #Set the direction to down
            self.direction = self.move_down
       
    def update(self) -> None:
        """Update the path of the bullet"""
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