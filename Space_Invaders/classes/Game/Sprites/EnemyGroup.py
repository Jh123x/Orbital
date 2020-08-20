import pygame

from .. import State


class EnemyShips(pygame.sprite.Group):
    def __init__(self, state: State):
        """The main class for the enemy ships group
            Arguments:
                No arguments
        """
        # Initialise the superclass
        super().__init__()

        # Store the state of the game the enemyship is in
        self.state = state

    def set_state(self, state: State) -> None:
        """Set the state for the enemy ship"""
        self.state = state

    def update(self) -> None:
        """Update all the mobs within the group"""

        # Check if any of the mobs touched the edige
        if len(tuple(filter(lambda x: x.touch_edge(), self.sprites()))):

            # For all sprites
            for i in self.sprites():

                # Move the sprite down if it is not in VS mode
                if self.state not in [State.PVP, State.AI_VS]:
                    i.move_down(i.get_height() // 4)

                # Change the direction of the sprite
                i.change_direction()

        # The lower the number of enemies, the greater the speed of the enemy
        super().update(2 // (len(self) if len(self) > 0 else 1))
