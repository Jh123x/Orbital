from .MovingObject import MovingObject
from .Enums import Direction

class Bullet(MovingObject):
    """Bullet class for the space invaders game"""

    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, direction:Direction, game_width:int, game_height:int, debug:bool):
        """The constructor for the bullet class"""
        #Load the image 
        self.image = self.sprites[0]

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
            assert False, "Direction of bullet is invalid"

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, debug)

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