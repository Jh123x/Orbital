from . import MovingObject, Bullet
from .. import Direction

class EnemyShip(MovingObject):

    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, lives:int,  game_width:int, game_height:int, switch_direction:Direction, bullet_grp, debug:bool):
        """Constructor for the enemy ship"""

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, self.sprites[lives-1 if lives <= len(self.sprites) else len(self.sprites)-1], debug)

        if self.debug:
            print(switch_direction)

        #Scale the mob to 40 x 40
        self.scale(40,40)

        #Store variables
        self.switch_direction = switch_direction
        self.lives = lives
        self.direction = Direction.RIGHT
        self.points = 10 * self.lives
        self.bullet_grp = bullet_grp

    def set_points(self, points:int) -> None:
        """Set the points for the mob""" 
        self.points = points

    def shoot(self, direction: Direction = Direction.DOWN):
        """Lets the mob shoot"""

        #Add the bullet to the bullet group
        self.bullet_grp.add(Bullet(self.sensitivity * 1.5, self.get_center()[0], self.get_y(), direction, self.game_width, self.game_height, self.debug))

    def get_points(self) -> int:
        """Get the number of points the enemy is worth"""
        return self.points

    def is_destroyed(self) -> bool:
        """Returns whether the enemy is destroyed"""
        return self.get_lives() == 0

    def destroy(self, lives:int = 1) -> None:
        """Destroy n life of the ship"""
        #If the ship is still alive
        if self.lives:

            #Reduce the life of the ship
            if self.lives < lives:
                self.lives = 0
            else:
                self.lives -= lives

            #If the ship still has lives
            if not self.is_destroyed():

                #Update the image to the new image of sprite
                self.image = self.sprites[self.lives-1 if self.lives < len(EnemyShip.sprites) else len(EnemyShip.sprites)-1]

                #Scale the mob to 40 x 40
                self.scale(40,40)

        else:

            #If it ends up here the destroy object is being destroyed somemore
            assert False, "Destroying destroyed object"

    def get_lives(self) -> int: 
        """Gets the number of lives the ship has left"""
        return self.lives

    def change_direction(self) -> None:
        """Change the x direction the enemy is moving"""

        #Swap the Right and the left position
        if self.direction == Direction.RIGHT:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.RIGHT
        else:
            return

    def touch_edge(self) -> bool:
        """Check if the enemy is touching the edge"""
        return self.get_x() >= self.game_width - self.get_width()//2 or self.get_x() < self.get_width()//2

    def update(self, multiplier:int) -> None:
        """Update the movement of the enemies"""

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
            
            #If switch direction is down
            if self.switch_direction == Direction.DOWN:
                
                #Move down
                self.move_down(self.get_height()//4)

            #If switch direction is up
            elif self.switch_direction == Direction.UP:

                #Move up
                self.move_up(self.get_height()//4)

            #Swap direction of x movement
            self.change_direction()

        #Call superclass update
        super().update()

