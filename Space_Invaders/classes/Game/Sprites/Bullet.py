from . import MovingObject
from .. import Direction


class Bullet(MovingObject):
    # Static method to store sprites
    sprites = []

    def __init__(self, sensitivity: int, initial_x: int, initial_y: int, direction: Direction, game_width: int,
                 game_height: int, debug: bool = False):
        """The constructor for the bullet class"""

        # Play the shoot sound
        self.sound.play('shooting')

        # Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, self.sprites[0], debug)

        # Scale to the correct size
        self.scale(11 * game_width // 600, 11 * game_height // 800)

        # Store bullet direction
        self.direction = direction.value

        # Set the bullet sprite based on direction
        if self.direction[1] < 0 and len(self.sprites) >= 2:
            self.image = self.sprites[1]
        else:
            self.image = self.sprites[0]

    def touch_edge(self):
        """Check if the bullet touched the edge of the screen"""
        return self.get_x() <= 0 or self.get_x() > self.game_width

    def update(self) -> None:
        """Update the path of the bullet"""
        # Move the bullet
        self.move(self.direction[0] * self.sensitivity, self.direction[1] * self.sensitivity)

        # Kill itself if the bullet is out of screen
        if self.y > self.game_height or self.y < 0:

            # Kill the object
            self.kill()

            # Do not continue to update position
            return

        # Make the bullet able to bounce along the x axis
        elif self.touch_edge():

            # Set the bullet direction to opposite in x axis
            if self.direction == Direction.BOTTOM_LEFT.value:
                self.direction = Direction.BOTTOM_RIGHT.value
            elif self.direction == Direction.BOTTOM_RIGHT.value:
                self.direction = Direction.BOTTOM_LEFT.value

        # Update its coordinates
        return super().update()
