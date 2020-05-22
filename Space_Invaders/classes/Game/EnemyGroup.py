import pygame

class EnemyShips(pygame.sprite.Group):
    def __init__(self):
        """The main class for the enemy ships group"""
        #Initialise the superclass
        super().__init__()

    def update(self) -> None:
        """The update function of the group"""
        #The lower the number of enemies, the greater the speed
        super().update(2 // (len(self) if len(self) > 0 else 1))