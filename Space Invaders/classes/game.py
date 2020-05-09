#!/usr/bin/env python
import pygame
import pygame.freetype
import enum
import sys
from pygame.locals import * 

#Define the COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,128,0)
LIME = (0,255,0)
YELLOW = (255,255,0)

class State(enum.Enum):
    MENU = 1
    PLAY = 2
    GAMEOVER = 3
    QUIT = -1

class GameWindow(object):
    """The main game window for Space invaders"""
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_path:str, enemy_img_path:str, bullet_img_path:str, wave:int = 1, debug:bool = False):
        """The constructor for the main window"""

        #Storing the variables
        self.fps = maxfps
        self.debug = debug
        self.score = 0
        self.game_width = game_width
        self.game_height = game_height
        self.wave = wave

        #Store the different states the menu has
        self.states = {
            State.MENU:self.handle_menu,
            State.PLAY:self.handle_play,
            State.GAMEOVER:self.handle_gameover,
            State.QUIT:self.__del__
        }

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
        self.bullets = Bullets(debug)
        self.enemies = EnemyShips(debug)

        #Create the main sprites
        self.player = Player(player_img_path, sensitivity, game_width, game_height, 3, debug)

        #Other sprites
        self.font = pygame.font.Font(pygame.font.get_default_font(),game_width//40)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(),game_width//20)
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), game_width // 10)

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

        #Check for debug keypresses
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
        
        #Otherwise return None for it to be asked in the next iteration
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

    def spawn_bullets(self):
        """Spawn the bullets for each of the entities"""
        #TODO
        pass

    def check_mouse_pos(self, rect_play, rect_end):
        """Check the position of the mouse on the menu to see what the player clicked"""
        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)

        #Set click to false
        click = False

        #Print out what buttons are pressed
        if self.debug:
            print(pygame.mouse.get_pressed())

        #If player pressed the button
        if pygame.mouse.get_pressed()[0]:
            if self.debug:
                print("Mouse clicked")
            click = True

        #If mousedown and position colide with play
        if rect_play.collidepoint(mouse_pos) and click:
            if self.debug:
                print("Mouse clicked play")
            return State.PLAY

        #If mousedown and position colide with quit
        elif rect_end.collidepoint(mouse_pos) and click:
            if self.debug:
                print("Mouse clicked quit")
            return State.QUIT

        #Otherwise the player has not decided
        else:
            #Return menu state
            if self.debug:
                print("Mouse moving")
            return State.MENU

    def handle_menu(self) -> State:
        """Handles the drawing of the menu"""

        #Draw the title
        title = self.title_font.render("Space Invaders", True, WHITE)
        rect_title = title.get_rect(center=(self.game_width/2, self.game_height//5))
        self.screen.blit(title, rect_title)

        #Draw the Play button
        play = self.end_font.render("Play",True, WHITE)
        rect_play = play.get_rect(center=(self.game_width/2, self.game_height//2))
        self.screen.blit(play, rect_play)

        #Draw the quit button
        end = self.end_font.render("Quit",True, WHITE)
        rect_end = play.get_rect(center=(self.game_width/2, self.game_height//15+self.game_height//2))
        self.screen.blit(end, rect_end)

        #Check the position of the mouse to return the state
        return self.check_mouse_pos(rect_play, rect_end)

    def handle_play(self) -> State:
        """Handles the drawing of the play string"""

        #If player is destroyed, go to gameover state
        if self.player.get_destroyed():
            return State.GAMEOVER

        #Draw the score
        score = self.font.render("Score : " + str(self.score), True, WHITE)
        self.screen.blit(score, (10, 10))

        #Draw the live count
        lives = self.font.render("Lives : " + str(self.player.get_lives()), True, WHITE)
        self.screen.blit(lives, (self.game_width - self.game_height//12,10))

        #Update the keypress of the player
        self.update_keypresses()

        #Update the objs
        self.update()

        #Return play state
        return State.PLAY

    def handle_gameover(self) -> State:
        """Handles drawing of the gameover screen"""

        #Update the stay status
        stay = self.end_update_keypresses()

        #If the player wants to stay
        if stay:
            running = True
            self.score = 0
            self.player.reset()
            return State.MENU
        
        #If the player does not want to stay
        elif stay == False:
            return State.QUIT

        #Otherwise keep on drawing
        else:

            #Draw the words for gameover
            gameover = self.end_font.render("Game Over", True, WHITE)
            self.screen.blit(gameover, (self.game_width // 2 - self.game_width // 7, self.game_height // 2 - self.game_height//12))

            #Draw the score
            score = self.end_font.render("Score : " + str(self.score), True, WHITE)
            self.screen.blit(score, (self.game_width // 2 - self.game_width // 7, self.game_height // 2))

            #Prompt player to update
            score = self.end_font.render("Press Y to go back and N to quit", True, WHITE)
            self.screen.blit(score, (self.game_height//12, self.game_height // 2 + self.game_height//12))
            
            #Return the gameover state
            return State.GAMEOVER


    def mainloop(self) -> None:
        """The mainloop to run the game"""

        #If debugging
        if self.debug:
            print("Running the main loop")

        #Loop variables
        running = True
        state = State.MENU
        
        #Mainloop for pygame GUI
        while running:
            
            #Set the FPS
            self.clock.tick(self.fps)

            #Fill the background to black before updating the screen
            self.screen.fill(BLACK)

            #If the player wants to quit exit the window
            if pygame.QUIT in map(lambda x: x.type, pygame.event.get()):
                break
                
            #Load the screen based on the state
            state = self.states[state]()

            #Update the display with the screen
            pygame.display.update()

            #If the state is quit break the loop
            if state == State.QUIT:
                running = False

        #Close the window
        self.__del__()

    def __del__(self) -> None:
        """Destructor for the game window"""
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()

class MovingObject(pygame.sprite.Sprite):
    """Main class for all objects that move"""
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int, debug:bool):
        """Constructor class for the moving object"""
        #Call the superclass init method
        super().__init__()

        #Storing the variables
        self.init_x = initial_x
        self.init_y = initial_y
        self.x = initial_x
        self.y = initial_y
        self.debug = debug
        self.sensitivity = sensitivity

        #Load the image model
        self.img = pygame.image.load(obj_path)



    def move(self,x,y) -> None:
        """Main Move Method"""
        #Add the values to x and y to change position
        self.x += x
        self.y += y
        if self.debug:
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

        #Set the position of the rect
        self.rect = self.img.convert().get_rect(center=(self.x,self.y))

    def scale(self, width, height) -> None:
        """Scale the image"""
        
        #Scale the image to the new width and height defined
        self.img = pygame.transform.scale(self.img,(width,height))

    def get_height(self) -> None:
        """Get the height of the image"""
        return self.img.get_height()

    def get_width(self) -> None:
        """Get the width of the image"""
        return self.img.get_width()

class Direction(enum.Enum):
    """Direction enum to store where objects are moving"""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Bullet(MovingObject):
    """Bullet class for the space invaders game"""
    
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int, direction:Direction, debug:bool):
        """The constructor for the bullet class"""

        #Call the superclass
        super().__init__(obj_path,sensitivity,initial_x, initial_y,debug)

        #Store the direction
        self.direction = direction

    def move(self) -> None:
        """Move the bullet"""

        #If the bullet is moving up
        if self.direction == Direction.UP:
            self.y -= self.sensitivity

        #If the bullet is moving down
        elif self.direction == Direction.DOWN:
            self.y += self.sensitivity

        #Otherwise there is an error
        else:
            assert False, "Direction is invalid"

class Bullets(pygame.sprite.Group):
    def __init__(self, debug:bool):
        """Constructor for the bullet group"""
        #Initialise the group
        super().__init__(self)

        #Store variables
        self.debug = debug

class EnemyShip(MovingObject):
    """Enemyship obj"""
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int, lives:int, points:int, debug:bool):
        """Constructor for the enemy object"""

        #Call the superclass
        super().__init__(obj_path,sensitivity,initial_x, initial_y,debug)

        #Store variables
        self.debug = debug
        self.lives = lives
        self.points = points


    def get_points(self) -> int:
        """Get the number of points the mob is worth"""
        return self.points

    def is_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.get_lives() == 0

    def get_lives(self) -> int: 
        """Gets the number of lives the ship has left"""
        return self.lives
        

class EnemyShips(pygame.sprite.Group):
    """The main class for the enemy ship"""
    def __init__(self, debug:bool):
        """The constructor for the EnemyShip class"""
        #Initialize the group
        super().__init__(self)

        #Store variables
        self.debug = debug

class Player(MovingObject):
    """Player class"""
    def __init__(self, obj_path:str, sensitivity:int, game_width:int, game_height:int, init_life:int, debug:bool):
        """Constructor for the player"""
        #Call the superclass
        super().__init__(obj_path, sensitivity, game_width//2, game_height,debug)

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
        self.debug = debug

    def move_up(self) -> None:
        """Move the player up"""
        #If the position is not at the max position allow the player to move up
        if self.y > self.img.get_height()//8:
            super().move_up()
        elif self.debug:
            print("Hit Top most")

    def move_down(self) -> None:
        """Move the player down"""
        if self.y <= self.game_height:
            super().move_down()
        elif self.debug:
            print("Hit Bottom most")

    def move_left(self) -> None:
        """Move the player right"""
        if self.x > self.img.get_width()//8:
            super().move_left()
        elif self.debug:
            print("Hit left most")

    def move_right(self) -> None:
        """Move the player right"""
        if self.x <= self.game_width:
            super().move_right()
        elif self.debug:
            print("Hit right most")

    def get_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroys the ship"""
        self.life -= 1 

    def get_lives(self) -> int:
        """Get the number of lives left"""
        return self.life

    def reset(self) -> None:
        """Reset the player stats"""
        self.life = self.init_life
        self.x = self.init_x
        self.y = self.init_y

def main() -> None:
    """The main function for the file"""
    pass

#Run the main function if this file is main
if __name__ == "__main__":
    main()