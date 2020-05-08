#!/usr/bin/env python

import pygame
import sys
from pygame.locals import *
from random import choice

#Define the COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)

class GameWindow():
    """The main game window for Space invaders"""
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_path:str, enemy_img_path:str, bullet_img_path:str, debug:bool = False):
        """The constructor for the main window"""

        #Storing the variables
        self.fps = maxfps
        self.debug = debug
        self.score = 0
        self.game_width = game_width
        self.game_height = game_height

        #Initialise pygame
        pygame.init()
        pygame.font.init()

        #Set the dimensions
        self.screen = pygame.display.set_mode((game_height,game_width))

        #Set the title
        pygame.display.set_caption("Space Invaders")

        #Load the Icon
        icon = pygame.image.load(icon_img_path)
        pygame.display.set_icon(icon)

        #Initialise the pygame window
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((game_width,game_height))

        #Create the main groups
        self.bullets = Bullets()
        self.enemies = EnemyShips()

        #Create the main sprites
        self.player = Player(player_img_path, sensitivity, game_width, game_height, 3)

        #Other sprites
        self.font = pygame.font.Font(pygame.font.get_default_font(),game_width//40)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(),game_width//20)

    def update_keypresses(self) -> None:
        """Update the map based on what the player has pressed"""
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #If the player has click 'Left' or 'a' move the player to the left
        if keys[K_a] or keys[K_LEFT]: 
            self.player.move_left()

        #If the player has click 'right' or 'd' move the player to the right
        if keys[K_d] or keys[K_RIGHT]:
            self.player.move_right()

        #Move the player down
        if keys[K_s] or keys[K_DOWN]:
            self.player.move_down()
        
        #Move the player up
        if keys[K_w] or keys[K_UP]:
            self.player.move_up()

        #Check Debug keypresses
        if self.debug:

            #Deduct the life of the player
            if keys[K_q]:
                self.player.destroy()

    def end_update_keypresses(self) -> bool:
        """Check if player wants to stay"""
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #Check for y key
        if keys[K_y]:
            return True

        #Check for n key
        elif keys[K_n]:
            return False
        
        else:
            return None

    def update(self) -> None:
        """Update the player obj onto the screen"""

        #Update the player position
        self.player.update()

        #Update the enemy group TODO

        #Update the bullets position TODO

        #Remove all bullets which are out of screen TODO

        #Draw the bullet TODO

        #Draw the enemy TODO

        #Draw player object
        self.screen.blit(self.player.img, self.player.rect)

    def mainloop(self) -> None:
        """The mainloop to run the game"""

        #If debugging
        if self.debug:
            print("Running the main loop")

        #Loop variables
        running = True
        stay = None
        
        #Mainloop for pygame GUI
        while running:
            
            #Set the FPS
            self.clock.tick(self.fps)

            #Fill the background to black before updating the screen
            self.screen.fill(BLACK)

            #If the player is alive
            if not self.player.get_destroyed():

                #Update the score
                score = self.font.render("Score : " + str(self.score), True, WHITE)
                self.screen.blit(score, (10, 10))

                #Draw the lives
                lives = self.font.render("Lives : " + str(self.player.get_lives()), True, WHITE)
                self.screen.blit(lives, (self.game_width - self.game_height//12,10))

                #Check all the events
                for event in pygame.event.get():

                    #If the player wants to quit exit the window
                    if event.type == pygame.QUIT:
                        running = False

                #Update the keypress of the player
                self.update_keypresses()

                #Update the objs
                self.update()
            
            #if the player is dead
            else:
                #Check all the events
                for event in pygame.event.get():

                    #If the player wants to quit exit the window
                    if event.type == pygame.QUIT:
                        running = False

                #Check if the player wants to leave
                if stay == True:
                    running = True
                    stay = None
                    self.score = 0
                    self.player.reset()

                #If player wants to quit
                elif stay == False:
                    running = False

                #Load the game over screen
                else:

                    #Draw the words for gameover
                    gameover = self.end_font.render("Game Over", True, WHITE)
                    self.screen.blit(gameover, (self.game_width // 2 - self.game_width // 7, self.game_height // 2 - self.game_height//12))

                    #Draw the score
                    score = self.end_font.render("Score : " + str(self.score), True, WHITE)
                    self.screen.blit(score, (self.game_width // 2 - self.game_width // 7, self.game_height // 2))

                    #Prompt player to update
                    score = self.end_font.render("Press Y to continue and N to quit", True, WHITE)
                    self.screen.blit(score, (self.game_height//12, self.game_height // 2 + self.game_height//12))

                    #Update the stay status
                    stay = self.end_update_keypresses()

            #Update the display with the screen
            pygame.display.update()

        #Close the window
        self.__del__()


    def __del__(self) -> None:
        """Destructor for the game window"""
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()

class MovingObject(pygame.sprite.Sprite):
    """Main class for all objects that move"""
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int):
        """Constructor class for the moving object"""
        #Initialise the sprite
        pygame.sprite.Sprite.__init__(self)

        #Storing the variables
        self.x = initial_x
        self.y = initial_y
        self.sensitivity = sensitivity

        #Load the image model
        self.img = pygame.image.load(obj_path)

    def move(self,x,y) -> None:
        """Main Move Method"""
        #Add the values to x and y to change position
        self.x += x
        self.y += y
        print(f"Coord: {self.x},{self.y}")

    def move_up(self) -> None:
        """Move the player up"""
        self.move(0,-self.sensitivity)

    def move_down(self) -> None:
        """Move the player down"""
        self.move(0,self.sensitivity)

    def move_left(self) -> None:
        """Move the player right"""
        self.move(-self.sensitivity,0)

    def move_right(self) -> None:
        """Move the player right"""
        self.move(self.sensitivity,0)

    def update(self) -> None:
        """Update the object rect position"""
        self.rect = self.img.convert().get_rect(center=(self.x,self.y))

    def scale(self, width, height) -> None:
        """Scale the image"""
        self.img = pygame.transform.scale(self.img,(width,height))

    def get_height(self) -> None:
        return self.img.get_height()

    def get_width(self) -> None:
        return self.img.get_width()

class Bullet(MovingObject):
    """Bullet class for the space invaders game"""
    
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int):
        """The constructor for the bullet class"""
        
        #Call the superclass
        super().__init__(obj_path,sensitivity,initial_x, initial_y)

    def move(self) -> None:
        """Move the bullet"""
        pass

class Bullets(pygame.sprite.Group):
    def __init__(self):
        """Constructor for the bullet group"""
        #Initialise the group
        pygame.sprite.Group.__init__(self)

class EnemyShip(MovingObject):
    """Enemyship obj"""
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int):
        """Constructor for the enemy object"""

        #Call the superclass
        super().__init__(obj_path,sensitivity,initial_x, initial_y)

class EnemyShips(pygame.sprite.Group):
    """The main class for the enemy ship"""
    def __init__(self):
        """The constructor for the EnemyShip class"""
        #Initialize the group
        pygame.sprite.Group.__init__(self)

class Player(MovingObject):
    """Player class"""
    def __init__(self, obj_path:str, sensitivity:int, game_width:int, game_height:int, init_life:int):
        """Constructor for the player"""
        #Call the superclass
        super().__init__(obj_path, sensitivity, game_width//2, game_height)

        #Scale the player
        self.scale(self.get_width()*2, self.get_height()*2)

        #If the life is not value set it to 3
        if init_life > 0:
            init_life = 3

        #Creating the variables
        self.init_life = init_life
        self.life = init_life
        self.game_width = game_width
        self.game_height = game_height

    def move_up(self) -> None:
        """Move the player up"""
        #If the position is not at the max position allow the player to move up
        if self.y > self.img.get_height()//8:
            super().move_up()

    def move_down(self) -> None:
        """Move the player down"""
        if self.y <= self.game_height:
            super().move_down()

    def move_left(self) -> None:
        """Move the player right"""
        if self.x > self.img.get_width()//8:
            super().move_left()

    def move_right(self) -> None:
        """Move the player right"""
        if self.x <= self.game_width:
            super().move_right()

    def get_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.life == 0

    def destroy(self) -> None:
        """Destroys the ship"""
        self.life -= 1 

    def get_lives(self) -> int:
        """Get the number of lives left"""
        return self.life

    def reset(self) -> None:
        """Reset the player stats"""
        self.life = self.init_life

def main() -> None:
    """The main function for the file"""
    pass

#Run the main function if this file is main
if __name__ == "__main__":
    main()