from . import ImageObject, BlockGroup

def hp_up(screen, player):
    """Increase the hp of the player"""
    player.add_lifes(1)

def bullet_up(screen, player):
    """Increase player bullet reload speed"""
    #If the player is not firing at a higher speed
    if player.maxcooldown > 10:
        player.maxcooldown -= 2

def shield_up(screen, player):
    """Creates a shield for the player"""
    #Spawn the blocks
    screen.blocks = BlockGroup(screen.screen_width, screen.screen_height//1.2, screen.screen, 3, screen.player1.get_height() + 10)

def emp_bomb(screen, player):
    """Destroy lives of all normal enemies by 1"""
    for sprite in screen.enemies:
        sprite.destroy()

def deflector(screen, player):
    """Move all the enemies on screen back"""
    for sprite in screen.enemies:
        sprite.move(0, 10)

def extra_bullet_power(screen, player):
    """Increase the bullet power of the player"""
    #Increase the bullet power of the player
    if player.get_bullet_power() < 5:
        player.increase_bullet_power(1)

def decrease_bullet_power(screen, player):
    """Decrease the bullet power of the player"""

    #If the player bullet power is greater than 1
    if player.get_bullet_power() > 1:

        #Decrease the player bullet power
        player.increase_bullet_power(-1)

class PowerUp(ImageObject):

    #To store the images of the sprites
    sprites = []

    #To store the powerup functions
    powers = [bullet_up, hp_up, shield_up]

    def __init__(self, initial_x:int, initial_y:int, width:int, height:int, power_type:int, time_to_live:int, debug:bool = False):
        """Constructor for the powerup class"""

        #Call the superclass contructor
        super().__init__(initial_x, initial_y, width, height, PowerUp.sprites[power_type], debug)

        #Store variables
        self.power_type = power_type
        self.ttl = time_to_live

        #Scale the image
        self.scale(30,30)

    @staticmethod
    def get_no_powerups() -> int:
        """Return the total number of powerups"""
        return len(PowerUp.powers)

    def get_ability(self):
        """Ability of the power up"""
        self.sound.play('powerup')
        return PowerUp.powers[self.power_type]

    def get_power_type(self) -> str:
        """Get the power type of the power up"""
        return self.power_type

    def update(self) -> None:
        """Update the sprite"""
        
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

