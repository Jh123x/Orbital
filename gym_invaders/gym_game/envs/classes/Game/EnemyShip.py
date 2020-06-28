try:
    from .MovingObject import MovingObject
    from .Enums import Direction
except ImportError:
    from MovingObject import MovingObject
    from Enums import Direction

class EnemyShip(MovingObject):

    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, lives:int,  game_width:int, game_height:int, debug:bool):
        """Constructor for the enemy object
            Arguments:
                sensitivity: Sensitivity of the enemy ship (int)
                initial_x: Get the initial x coordinate for the ship (int)
                initial_y: Get the initial y coordinate for the ship (int)
                lives: get the number of lives that the ship has left (int)
                game_width: Width of the game in pixels (int)
                game_height: Height of the game in pixels (int)
                debug: Toggles debug mode (bool)

            Methods:
                get_points: Returns the points of that the mob is worth
                is_destroyed: Returns whether the ship is destroyed
                destroy: Kill the mob 1 time
                get_lives: Get the number of lives that the mob has left
                change_direction: Change the direction that the mob is moving
                update: Update the position of the mob
        """

        #Load the correct image
        self.image = self.sprites[lives-1 if lives < len(EnemyShip.sprites) else len(EnemyShip.sprites)-1]

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, debug)

        #Store variables
        self.lives = lives
        self.direction = Direction.RIGHT
        self.points = 10 * self.lives

    def get_points(self) -> int:
        """Get the number of points the mob is worth
            Arguments:
                No arguments:
            Returns: 
                Returns the number of points the mob is worth (int)
        """
        return self.points

    def is_destroyed(self) -> bool:
        """Returns whether the ship is destroyed
            Arguments:
                No arguments:
            Returns: 
                Returns if the mob is destroyed
        """
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroy 1 life of the ship
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        #If the ship is still alive
        if self.lives:

            #Reduce the life of the ship
            self.lives -= 1

            #If the ship still has lives
            if not self.is_destroyed():

                #Update the image to the new image of sprite
                self.image = self.sprites[self.lives-1 if self.lives < len(EnemyShip.sprites) else len(EnemyShip.sprites)-1]
        else:
            #If it ends up here the destroy object is being destroyed somemore
            assert False, "Destroying destroyed object"

    def get_lives(self) -> int: 
        """Gets the number of lives the ship has left
            Arguments:
                No arguments:
            Returns: 
                Returns the number of lives the mob have left (int)
        """
        return self.lives

    def change_direction(self) -> None:
        """Change the x direction the enemy is moving
            Arguments:
                No arguments:
            Returns: 
                No return
        """

        #Swap the Right and the left position
        if self.direction == Direction.RIGHT:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.RIGHT
        else:
            assert False, "Enemy ship direction is invalid"

    def update(self, multiplier:int) -> None:
        """Update the movement of the enemies
            Arguments:
                No arguments:
            Returns: 
                No return
        """

        #If enemyship is moving to the right and is not at the edge
        if self.direction == Direction.RIGHT and self.get_x() < self.game_width:

            #Move it to the right
            self.move_right(self.sensitivity*multiplier//1)

        #If it is moving to the left and is not at the edge
        elif self.direction == Direction.LEFT and self.get_x() > 0:

            #Move it to the left
            self.move_left(self.sensitivity*multiplier//1)

        #If it is at the edge
        else:
            #Move down
            self.move_down(self.get_height()//4)

            #Swap direction of x movement
            self.change_direction()

        #Call superclass update
        super().update()
