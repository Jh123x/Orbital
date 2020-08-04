import random
from . import EnemyShip, Bullet
from .. import Direction

class Crabs(EnemyShip):

    #Sprites for the Crabs
    sprites = []

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, lives:int,  game_width:int, game_height:int, bullet_grp, debug:bool):
        """The main class for Crabs"""
        #Call the superclass init with 1.2 times the sensitivity to make it move faster
        super().__init__(sensitivity, initial_x, initial_y, lives,  game_width, game_height, None, bullet_grp, debug)

        #Scale according to the fps
        self.scale(50 * game_width // 600, 50 * game_height // 800)

        #Store the x_velocity and y_velocity (To be fine tuned later)
        self.delta_x = self.sensitivity // 4
        self.delta_y = self.sensitivity // 4

        #Set the score for the crabs
        self.set_points(200 * lives)

    def shoot(self, direction: Direction = None):
        """Lets the mob shoot"""

        #If the direction is not set
        if not direction:

            #Choose a random btm left/ right direction
            direction = random.choice([Direction.BOTTOM_LEFT, Direction.BOTTOM_RIGHT])

        #Add the bullet to the bullet group
        self.bullet_grp.add(Bullet(self.sensitivity * 1.5, self.get_center()[0], self.get_y(), direction, self.game_width, self.game_height, self.debug))

    def update(self) -> None:
        """Overridden update class for the scout boss"""

        #If the object has touched the edge
        if self.touch_edge():
            
            #Change x direction
            self.delta_x = -self.delta_x

        #Update the position of the ship
        self.move(self.delta_x, self.delta_y)

        #Call the superclass update
        return super().update(1)
