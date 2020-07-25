from . import EnemyShip

class Brute(EnemyShip):

    #Store the sprite for the Brute
    sprites = []

    #Store the number of times the brute spawned
    spawn_count = 0

    @staticmethod
    def reset():
        """Reset method for the brute class to reset count"""
        Brute.spawn_count = 0

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int,  game_width:int, game_height:int, bullet_grp, debug:bool):
        """Constructor class for the Brute boss"""

        #Increment spawn count
        self.spawn_count += 1

        #Call the superclass constructer
        super().__init__(sensitivity, initial_x, initial_y, self.spawn_count,  game_width, game_height, None, bullet_grp, debug)

        #Set direction to none
        self.direction = None

        #Set the points
        self.set_points(self.spawn_count * 50)

        #Set the delta x for the brute
        self.delta_y = sensitivity // 3 # It moves slower than the mobs

    def update(self) -> None:
        """Overridden update class for the scout boss"""

        #Update the position of the ship
        self.move(0, self.delta_y)

        #Call the superclass update
        return super().update(1)

        