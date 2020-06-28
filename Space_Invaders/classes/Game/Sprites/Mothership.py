from . import MovingObject

class MotherShip(MovingObject):
    sprites = []
    def __init__(self, initial_x:int, initial_y:int, game_width:int, game_height:int, points:int, debug:bool = False):
        """Main constructor for the mothership"""
        #Call the superclass
        super().__init__(5, initial_x, initial_y, 100, 50, MotherShip.sprites[0], debug, (100,50))

        #Store the points
        self.points = points

    def update(self, *args) -> None:
        """Update movement of the mothership"""

        #Move the mothership to the right
        self.move_right()

        #Call the superclass update
        return super().update()

    def get_points(self) -> int:
        """Get the points for the mothership"""
        return self.points