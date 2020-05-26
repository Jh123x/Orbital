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
        if len(tuple(filter(lambda x: x.touch_edge(), self.sprites()))):
            for i in self.sprites():
                i.move_down(i.get_height()//4)
                i.change_direction()
            

        #The lower the number of enemies, the greater the speed
        super().update(2 // (len(self) if len(self) > 0 else 1))