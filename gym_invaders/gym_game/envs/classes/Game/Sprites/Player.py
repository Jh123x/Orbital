import pygame
from . import MovingObject, Bullet
from .. import Direction

class Player(MovingObject):
    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, game_width:int, game_height:int, initial_x:int, initial_y:int, init_life:int, 
                fps:int, bullet_grp:pygame.sprite.Group(), bullet_direction:Direction, 
                debug:bool = False, isAI:bool = False):
        """Constructor for the player
            Arguments:
                sensitivity: Sensitivity of the player controls (int)
                game_width: Width of the game in pixels (int)
                game_height: Height of the game in pixels (int)
                init_life: Initial life of the player (int)
                fps: FPS of the game (int)
                bullet_grp: Bullet group of the player (pygame.sprite.Group)
                debug: Toggles debug mode (bool): Default = False
                isAI: Boolean to see if the player is an AI instance (bool): Default = False

            Methods:
                isAI: Returns a boolean indicating if the player is an AI
                on_cooldown: Checks if player gun is on cooldown
                shoot: Allows the player to shoot a bullet
                move_up: Method to disable upward movement on player
                move_down: Method to disable downward movement on player
                move_left: Handles the moving left of the player
                move_right: Handles right movement of the player
                is_destroyed: Checks if the player is destroyed
                destroy: Destroy the player 1 time
                get_lives: Get the number of lives the player has left
                reset: Reset the position of the player
                update: Update the position of the player
        """
        #Store the items
        self.is_AI = isAI
        self.bullet_direction = bullet_direction
        
        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, Player.sprites[-1], debug)

        #Scale the image to 50x50
        self.scale(50,50)

        #Invicibility when it just spawned
        self.invincible = fps

        #Player bullet group
        self.bullet_grp = bullet_grp

        #Set player max cooldown
        self.maxcooldown = fps // (3 * 0.95)

        #Keep track of bullet cooldown
        self.cooldown = 0

        #If the life is not valid set it to 3 by default
        if init_life > 0:
            init_life = 3

        #Initial amount of life
        self.init_life = init_life

        #Current life
        self.life = init_life

        #Store game variables
        self.fps = fps

        #Re-render the character
        self.changed = True

    def isInvincible(self) -> bool:
        """Check if the player is invincible"""
        return self.invincible > 0

    def add_lifes(self, no:int) -> None:
        """Adds life to the player"""
        assert no > 0
        self.life += no

    def isAI(self) -> bool:
        """Check if it is an ai instance of the Player
            Arguments:
                No arguments
            Returns: 
                Returns True if player is an ai otherwise false (bool)
        """
        return self.is_AI

    def on_cooldown(self) -> bool:
        """Check if shooting is on cooldown
            Arguments:
                No arguments
            Returns:
                Returns True if the guns are on cooldown (bool)
        """
        return self.cooldown > 0

    def shoot(self) -> bool:
        """Lets the player shoot a bullet
            Arguments:
                No arguments:
            Returns: 
                No return
        """

        #If the player is not on cooldown 
        if not self.on_cooldown():

            #Add the bullet to the bullet group
            self.bullet_grp.add(Bullet(self.sensitivity * 1.5, self.get_center()[0], self.get_y(), self.bullet_direction, self.game_width, self.game_height, self.debug))

            #Reset the cooldown
            self.cooldown = self.maxcooldown

            #Return True if the player has shot
            return True

        #Return false if player fails to shoot
        return False

    def move_up(self) -> None:
        """Do not allow the player to move up
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        pass

    def move_down(self) -> None:
        """Do not allow the player to move down
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        pass

    def move_left(self) -> None:
        """Move the player left
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        #If the player is not at the leftmost part of the screen 
        if self.x > self.image.get_width()//8:

            #allow the player to move left
            super().move_left()

        #Otherwise print debug message
        elif self.debug:
            print("Hit left most")

    def move_right(self) -> None:
        """Move the player right
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        #If the player is not at the right most 
        if self.x <= self.game_width:

            #allow the player to move right
            super().move_right()

        #Otherwise print debug message
        elif self.debug:
            print("Hit right most")

    def is_destroyed(self) -> bool:
        """Returns whether the ship is destroyed
            Arguments:
                No arguments:
            Returns: 
                Returns true if the player has no lives left otherwise false (bool)
        """
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroys the ship 1 time
            Arguments:
                No arguments:
            Returns: 
                No return
        """

        #If the player is no invincible
        if not self.invincible:

            #Reduce the life of the player
            self.life -= 1

            #Make the player invincible for 1 second
            self.invincible = self.fps

    def get_lives(self) -> int:
        """Get the number of lives left
            Arguments:
                No arguments:
            Returns: 
                returns the number of lives the player has left (int)
        """
        return self.life

    def reset(self) -> None:
        """Reset the player stats
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        #Reset life
        self.life = self.init_life

        #Reset shooting cooldown
        self.maxcooldown = self.fps // (3 * 0.95)

        #Reset position
        self.x = self.initial_x
        self.y = self.initial_y

        #Rerender rect
        self.changed = True

        #Give player 1s invisibility
        self.invincible = self.fps

    def update(self) -> None:
        """Update the position of the player
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        
        #If the player is invincible
        if self.invincible > 0:

            #Reduce invincibility amount
            self.invincible -= 1

        #If the player gun is on cooldown
        if self.cooldown > 0:

            #Reduce cooldown
            self.cooldown -= 1

        #Load the Image of the player based on his life
        self.image = Player.sprites[self.get_lives()-1 if self.get_lives() < len(Player.sprites) else len(Player.sprites) - 1]

        #Call the super update
        return super().update()