from . import EnemyShip

class MotherShip(EnemyShip):
    sprites = []
    def __init__(self, initial_x:int, initial_y:int, game_width:int, game_height:int, points:int, debug:bool = False):
        """Main constructor for the mothership"""
        #Call the superclass
        super().__init__(5, initial_x, initial_y, 1, game_width, game_height, None, None, debug)

        #Scale the mothership
        self.scale(100,50)

        #Store the points
        self.set_points(points)

    def update(self) -> None:
        """Update movement of the mothership"""

        #Move the mothership to the right
        self.move_right()

        #Check if mothership touched the edge
        if self.get_x() > self.game_width:

            #If so remove the mothership
            self.kill()

            #Do nothing afther that
            return

        #Call the superclass update
        return super().update(1)