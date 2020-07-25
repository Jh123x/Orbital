import random
from . import Scout
from .. import Direction

class Crabs(Scout):

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, lives:int,  game_width:int, game_height:int, bullet_grp, debug:bool):
        """The main class for Crabs"""
        #Call the superclass init with 1.2 times the sensitivity to make it move faster
        super().__init__(sensitivity, initial_x, initial_y, lives,  game_width, game_height, None, bullet_grp, debug)

        #Store the x_velocity and y_velocity (To be fine tuned later)
        self.delta_x = self.sensitivity // 2
        self.delta_y = self.sensitivity // 4

        #Set the score for the scout
        self.set_points(500)

        #Set the lives
        self.lives = 5

    def shoot(self, direction: Direction = None):
        """Lets the mob shoot"""

        #If the direction is not set
        if not direction:

            #Choose a random btm left/ right direction
            direction = random.choice([Direction.BOTTOM_LEFT, Direction.BOTTOM_RIGHT])


        #Add the bullet to the bullet group
        self.bullet_grp.add(Bullet(self.sensitivity * 1.5, self.get_center()[0], self.get_y(), direction, self.game_width, self.game_height, self.debug))
