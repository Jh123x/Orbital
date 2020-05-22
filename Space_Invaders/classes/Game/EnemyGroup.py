import pygame

class EnemyShips(pygame.sprite.Group):
    def __init__(self):
        """The main class for the enemy ships group
            Arguments:
                No arguments
        """
        #Initialise the superclass
        super().__init__()

    def update(self) -> None:
        """Update all the mobs within the group
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #The lower the number of enemies, the greater the speed
        super().update(2 // (len(self) if len(self) > 0 else 1))