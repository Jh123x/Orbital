from . import ImageObject, BlockGroup

def hp_up(screen, player):
    """Increase the hp of the player"""
    player.add_lifes(1)
    return

def bullet_up(screen, player):
    """Increase player bullet reload speed"""
    #If the player is not firing at a higher speed
    if player.maxcooldown > 20:
        player.maxcooldown -= 10
    else:
        pass
    return

def shield_up(screen, player):
    """Creates a shield for the player"""
    #Spawn the blocks
    screen.blocks = BlockGroup(screen.screen_width, screen.screen_height//1.2, screen.screen, 3, screen.player.get_height() + 10)
    return 

class PowerUp(ImageObject):
    sprites = []
    powers = [bullet_up, hp_up, shield_up]
    def __init__(self, initial_x:int, initial_y:int, width:int, height:int, power_type:int, time_to_live:int, debug:bool = False):
        """Constructor for the powerup class"""

        #Call the superclass contructor
        super().__init__(initial_x, initial_y, width, height, PowerUp.sprites[power_type], debug)

        #Store variables
        self.power_type = power_type
        self.ttl = time_to_live

    @staticmethod
    def get_no_powerups() -> int:
        """Return the total number of powerups"""
        return len(PowerUp.powers)

    def get_ability(self):
        """Ability of the power up"""
        return PowerUp.powers[self.power_type]

    def get_power_type(self) -> str:
        """Get the power type of the power up"""
        return self.power_type

    def update(self) -> None:
        """Update the sprite"""
        print(f"Time to live: {self.ttl}")
        #If time to live is 0
        if self.ttl == 0:

            #Kill itself
            self.kill()
            return

        #Otherwise
        else:

            #Reduce time to live
            self.ttl -= 1

            #Call superclass update
            return super().update()

