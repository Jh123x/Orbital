from . import EnemyShip

class Scout(EnemyShip):

    #Store the sprites for the Scout
    sprites = []
    
    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, lives:int,  game_width:int, game_height:int, bullet_grp, debug:bool):
        """Main class for the scout ship"""

        #Call the superclass init with 1.2 times the sensitivity to make it move faster
        super().__init__(sensitivity, initial_x, initial_y, lives,  game_width, game_height, None, bullet_grp, debug)

        #Store the x_velocity and y_velocity (To be fine tuned later)
        self.delta_x = self.sensitivity
        self.delta_y = self.sensitivity//2

        #Set the score for the scout
        self.set_points(500)

    def update(self) -> None:
        """Overridden update class for the scout boss"""

        #If the object has touched the edge
        if self.touch_edge() and len(self.sprites) == 2 :
            
            #Change x direction
            self.delta_x = -self.delta_x

            #Check if it is time to switch direction
            if self.delta_x > 0:

                #Change the image to face the right
                self.image = self.sprites[0]

            else:

                #Change the image to face the left
                self.image = self.sprites[1]

        #Update the position of the ship
        self.move(self.delta_x, self.delta_y)

        #Call the superclass update
        return super().update(1)