import pygame
from . import MovingObject, Bullet
from .. import Direction

class Player(MovingObject):

    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, game_width:int, game_height:int, initial_x:int, initial_y:int, init_life:int, 
                fps:int, bullet_grp:pygame.sprite.Group(), bullet_direction:Direction, 
                debug:bool = False, isAI:bool = False):
        """Main class for the player object"""
        #Store the items
        self.is_AI = isAI
        self.bullet_direction = bullet_direction
        
        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, Player.sprites[-1], debug)

        #Scale the image to 50x50
        self.scale(50 * game_width // 600, 50 * game_height // 800)

        #Invicibility when it just spawned
        self.invincible = fps

        #Player bullet group
        self.bullet_grp = bullet_grp

        #If the life is not valid set it to 3 by default
        if init_life <= 0:
            init_life = 3

        #Initial amount of life
        self.init_life = init_life

        #Set rotation to None
        self.rotation = 0

        #Store game variables
        self.fps = fps

        #Reset player character
        self.reset()

    def reset(self) -> None:
        """Reset the player stats to original stats"""
        
        #Reset life
        self.life = self.init_life

        #Reset shooting cooldown
        self.maxcooldown = self.fps // 2.5

        #Keep track of bullet cooldown
        self.cooldown = 0

        #Reset position
        self.x = self.initial_x
        self.y = self.initial_y

        #Reset the bullet power
        self.bullet_power = 1

        #Rerender rect
        self.changed = True

        #Give player 1s invisibility
        self.invincible = self.fps

    def isInvincible(self) -> bool:
        """Check if the player is invincible"""
        return self.invincible > 0

    def increase_bullet_power(self, inc:int):
        """Increase the player bullet power by inc"""
        self.bullet_power += inc

    def get_bullet_power(self) -> int:
        """Return the bullet power of the player"""
        return self.bullet_power

    def add_lifes(self, no:int) -> None:
        """Adds life to the player"""
        assert no > 0
        self.life += no

    def isAI(self) -> bool:
        """Check if it is an ai instance of the Player"""
        return self.is_AI

    def on_cooldown(self) -> bool:
        """Check if shooting is on cooldown"""
        return self.cooldown > 0

    def shoot(self) -> bool:
        """Lets the player shoot a bullet if the player is not on cooldown"""

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
        """Do not allow the player to move up"""
        pass

    def move_down(self) -> None:
        """Do not allow the player to move down"""
        pass

    def move_left(self) -> None:
        """Move the player to the left"""
        #If the player is not at the leftmost part of the screen 
        if self.x > self.image.get_width()//8:

            #allow the player to move left
            super().move_left()

        #Otherwise print debug message
        elif self.debug:
            print("Hit left most")

    def move_right(self) -> None:
        """Move the player right"""
        #If the player is not at the right most 
        if self.x <= self.game_width:

            #allow the player to move right
            super().move_right()

        #Otherwise print debug message
        elif self.debug:
            print("Hit right most")

    def is_destroyed(self) -> bool:
        """Returns whether the player is destroyed"""
        return self.get_lives() == 0

    def destroy(self, lives:int = 1) -> None:
        """Destroys the ship 1 time"""

        #If the player is no invincible
        if not self.invincible:

            #Reduce the life of the player
            if self.life < lives:
                self.life = 0
            else:
                self.life -= lives

            #Make the player invincible for 1 second
            self.invincible = self.fps

    def get_lives(self) -> int:
        """Get the number of lives left"""
        return self.life

    def rotate(self, angle:int):
        """Store the rotation to be updated when sprite changes"""
        #Store the angle rotation
        self.rotation = angle

        #Call the super rotate class method
        return super().rotate(self.rotation)

    def update(self) -> None:
        """Update the position of the player"""
        
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
        
        #Rotate the corresponding image
        self.rotate(self.rotation)

        #Call the super update
        return super().update()