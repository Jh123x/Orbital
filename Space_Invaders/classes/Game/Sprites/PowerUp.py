from . import ImageObject, BlockGroup, Mothership

def hp_up(screen, player):
    """Increase the hp of the player"""
    player.add_lifes(1)

def bullet_up(screen, player):
    """Increase player bullet reload speed"""
    #If the player is not firing at a higher speed
    if player.maxcooldown > 6:
        player.maxcooldown -= 2

def shield_up(screen, player):
    """Creates a shield for the player"""
    #Spawn the blocks
    screen.blocks = BlockGroup(screen.screen_width, screen.screen_height//1.2, screen.screen, 3, screen.player1.get_height() + 10)

def emp_bomb(screen, player):
    """Destroy lives of all normal enemies by 1"""
    
    #Var to decrease emp bomb dmg
    if screen.wave // 4 > 1:
        health_dec = screen.wave // 4
    else:
        health_dec = 1

    #Iterate through all the sprites
    for sprite in screen.enemies:

        #If the enemy only has 1 life
        if sprite.get_lives() <= health_dec:

            #Kill the sprite
            sprite.kill()

        #Otherwise
        else:

            #Destroy it 1 time
            for _ in range(health_dec):
                sprite.destroy()

def deflector(screen, player):
    """Move all the enemies on screen back"""

    #Iterate through the enemies
    for sprite in screen.enemies:

        #Move the enemy back
        sprite.move(0, -10)

    #Iterate through the other sprites
    for sprite in screen.other_enemies:

        #If it is the mothership ignore it
        if type(sprite) == Mothership:
            continue

        #Otherwise move the sprite back
        sprite.move(0, -10)

def extra_bullet_power(screen, player):
    """Increase the bullet power of the player"""
    #Increase the bullet power of the player
    if player.get_bullet_power() < screen.wave + 2:

        #Increase the damage of the player bullet
        player.increase_bullet_power(1)

def decrease_bullet_power(screen, player):
    """Decrease the bullet power of the player"""

    #If the player bullet power is greater than 1
    if player.get_bullet_power() > 1:

        #Decrease the player bullet power
        player.increase_bullet_power(-1)

class PowerUp(ImageObject):

    #To store the images of the sprites
    sprites = {}

    #To store the powerup functions
    powers = {'bullet_up' : bullet_up, 
                'bullet_attack_up' : extra_bullet_power, 
                "debuff_bullet" : decrease_bullet_power, 
                "deflector" : deflector, 
                "emp" : emp_bomb, 
                "hp_up" : hp_up, 
                "shield_up" : shield_up}

    def __init__(self, initial_x:int, initial_y:int, width:int, height:int, power_type:str, time_to_live:int, debug:bool = False):
        """Constructor for the powerup class"""

        #Call the superclass contructor
        super().__init__(initial_x, initial_y, width, height, PowerUp.sprites[power_type], debug)

        #Store variables
        self.power_type = power_type
        self.ttl = time_to_live

        #Scale the image
        self.scale(30,30)

    @staticmethod
    def get_powerups() -> tuple:
        """Return the total number of powerups"""
        return tuple(PowerUp.powers.keys())

    def get_ability(self):
        """Ability of the power up"""

        #Play the powerup sound
        self.sound.play('powerup')

        #Return the powerup function
        return PowerUp.powers[self.power_type]

    def get_power_type(self) -> str:
        """Get the power type of the power up"""
        return self.power_type

    def update(self) -> None:
        """Update the powerup sprite"""
        
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

