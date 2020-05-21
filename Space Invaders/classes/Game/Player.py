from .MovingObject import MovingObject

class Player(MovingObject):
    """Player class"""
    #Static method to store sprites
    sprites = []

    def __init__(self, sensitivity:int, game_width:int, game_height:int, init_life:int, fps:int, debug:bool = False, AI:bool = False):
        """Constructor for the player"""
        #Store the items
        self.AI = AI

        #Load the image based on his health
        self.image = Player.sprites[-1]
        
        #Call the superclass
        super().__init__(sensitivity, game_width//2, game_height, game_width, game_height, debug)

        #Invicibility when it just spawned
        self.invincible = fps

        #If the life is not valid set it to 3 by default
        if init_life > 0:
            init_life = 3

        #Initial position
        self.init_x = game_width//2
        self.init_y = game_height

        #Initial amount of life
        self.init_life = init_life

        #Current life
        self.life = init_life

        #Store game variables
        self.fps = fps

        #Re-render the character
        self.changed = True

    def isAI(self) -> bool:
        """Check if it is an ai instance of the Player"""
        return self.AI

    def move_up(self) -> None:
        """Do not allow the player to move up"""
        pass

    def move_down(self) -> None:
        """Do not allow the player to move down"""
        pass

    def move_left(self) -> None:
        """Move the player left"""
        #If the player is not at the leftmost part of the screen allow the player to move left
        if self.x > self.image.get_width()//8:
            super().move_left()
        elif self.debug:
            print("Hit left most")

    def move_right(self) -> None:
        """Move the player right"""
        #If the player is not at the right most allow the player to move right
        if self.x <= self.game_width:
            super().move_right()
        elif self.debug:
            print("Hit right most")

    def is_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroys the ship 1 time"""
        if not self.invincible:
            #Reduce the life of the player
            self.life -= 1 

            #Make the player invincible for 1 second
            self.invincible = self.fps

    def get_lives(self) -> int:
        """Get the number of lives left"""
        return self.life

    def reset(self) -> None:
        """Reset the player stats"""
        #Reset life
        self.life = self.init_life

        #Reset position
        self.x = self.init_x
        self.y = self.init_y

        #Rerender rect
        self.changed = True

        #Give player 1s invisibility
        self.invincible = self.fps

    def update(self) -> None:
        """Update the position of the player"""
        #Reduce invincibility amount
        if self.invincible:
            self.invincible -= 1

        #Load the Image of the player based on his life
        self.image = Player.sprites[self.get_lives()-1]

        #Call the super update
        return super().update()