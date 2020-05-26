import pygame
from .. import State

class EnemyShips(pygame.sprite.Group):
    def __init__(self, state: State):
        """The main class for the enemy ships group
            Arguments:
                No arguments
        """
        #Initialise the superclass
        super().__init__()

        self.state = state

    def update(self) -> None:
        """Update all the mobs within the group
            Arguments:
                No arguments
            Returns: 
                No return
        """
        if len(tuple(filter(lambda x: x.touch_edge(), self.sprites()))):
            for i in self.sprites():
                if self.state != State.PVP:
                    i.move_down(i.get_height()//4)
                i.change_direction()
            

        #The lower the number of enemies, the greater the speed
        super().update(2 // (len(self) if len(self) > 0 else 1))