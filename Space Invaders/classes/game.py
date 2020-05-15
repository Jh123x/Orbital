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
        self.state = State.MENU
        self.sensitivity = sensitivity
        self.bullet_cooldown = 0
        self.spawn_state = 0

        #Store path to image files to be used when spawning enemies
        self.enemy_img_path = enemy_img_path
        self.bullet_img_path = bullet_img_path

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
        self.up_bullets = pygame.sprite.Group() #Bullets from player
        self.down_bullets = pygame.sprite.Group() #Bullets from mobs
        self.enemies = EnemyShips(4) #Enemies

        #Create the main sprites
        self.player = Player(player_img_path, sensitivity, game_width, game_height, 3, maxfps, debug)

        #Other sprites
        self.font = pygame.font.Font(pygame.font.get_default_font(),game_width//40)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(),game_width//20)
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), game_width // 10)

    def get_state(self) -> State:
        """Return the state the game is in"""
        return self.state

    def update_keypresses(self) -> None:
        """Update the map based on what the player has pressed"""
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #Continue cooldown if bullet is not on cooldown
        if self.bullet_cooldown:
            self.bullet_cooldown -= 1

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

        #Check if the player pressed spacebar to spawn a bullet
        if keys[K_SPACE] and self.bullet_cooldown == 0:

            #Spawn a bullet
            self.spawn_bullets()

            #Set the bullet on cooldown
            self.bullet_cooldown = self.fps//2

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

    def spawn_aliens(self, number:int) -> None:
        """Spawn aliens into the game"""

        #Adding sprites
        self.enemies.add([EnemyShip(self.enemy_img_path, self.sensitivity, self.game_width//4 + i*self.game_width//20, self.game_height//20, 1, 10, self.game_width, self.game_height, self.debug) for i in range(number)])
            
    def check_collisions(self) -> int:
        """Check the objects which collided"""
        #Check if player has collided with bullets
        bullet_collide = pygame.sprite.spritecollide(self.player, self.down_bullets, True)
        
        #If the set is not empty reduce player life
        if len(bullet_collide) > 0:
            self.player.destroy()

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.up_bullets, self.down_bullets, True, True)

        #Get ships destroyed
        ships = list(pygame.sprite.groupcollide(self.up_bullets, self.enemies, True, False).values())

        if self.debug:
            print(ships)

        if ships:
        #Destroy the ship in the list
            ships = ships[0]
            for ship in ships:
                ship.destroy()
                if self.debug:
                    print(f"Ship destroyed")
        
            #Get all ships with 0 lives
            destroyed_ships = list(filter(lambda x: x.get_lives() == 0, ships))

            #Remove the sprite from the group
            self.enemies.remove(*destroyed_ships)

            #Remove sprites that collide with bullets and return the sum of all the scores
            return sum(map(lambda x: x.get_points(), destroyed_ships),0)

        else:
            return 0

    def update(self) -> None:
        """Update the player obj onto the screen"""

        #Update the player position
        self.player.update()

        #Update the enemy group
        self.enemies.update()

        #Update the bullets positions
        self.up_bullets.update()
        self.down_bullets.update()
        self.up_bullets.draw(self.screen)
        self.down_bullets.draw(self.screen)
        if self.debug:
            print(f"Number of player bullets: {len(self.up_bullets)}")

        #Draw the enemy TODO
        self.enemies.draw(self.screen)
        if self.debug:
            print(f"Number of enemies: {len(self.enemies)}")

        #Draw player object
        self.screen.blit(self.player.image, self.player.rect)

    def spawn_bullets(self):
        """Spawn the bullets for each of the entities"""

        #Spawn bullet for the player
        #Create the bullet object
        bullet = Bullet(self.bullet_img_path, self.sensitivity * 1.5, self.player.x, self.player.y - 10, Direction.UP, self.game_width, self.game_height, self.debug)

        #Add the bullet to the bullet group
        self.up_bullets.add(bullet)

        #Spawn bullets for the rest of the entities TODO
        

    def check_mouse_pos(self, rect_play, rect_end):
        """Check the position of the mouse on the menu to see what the player clicked"""
        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)

        #Set click to false
        click = False

        #If player pressed the button
        if pygame.mouse.get_pressed()[0]:
            if self.debug:
                print(f"Mouse clicked {pygame.mouse.get_pressed()}")
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
        rect_title = title.get_rect(center=(self.game_width//2, self.game_height//5))
        self.screen.blit(title, rect_title)

        #Draw the Play button
        play = self.end_font.render("Play", True, WHITE)
        rect_play = play.get_rect(center=(self.game_width//2, self.game_height//2))
        self.screen.blit(play, rect_play)

        #Draw the quit button
        end = self.end_font.render("Quit", True, WHITE)
        rect_end = end.get_rect(center=(self.game_width//2, self.game_height//15 + self.game_height//2))
        self.screen.blit(end, rect_end)

        #Draw the instructions
        inst1 = self.end_font.render("Use WASD or arrow keys to move", True, WHITE)
        rect_inst1 = inst1.get_rect(center=(self.game_width//2, self.game_height//1.5))
        self.screen.blit(inst1, rect_inst1)

        inst2 = self.end_font.render("Press Spacebar to shoot", True, WHITE)
        rect_inst2 = inst2.get_rect(center=(self.game_width//2, self.game_height//1.5 + self.game_height//15))
        self.screen.blit(inst2, rect_inst2)

        #Check the position of the mouse to return the state
        return self.check_mouse_pos(rect_play, rect_end)

    def handle_play(self) -> State:
        """Handles the drawing of the play string"""

        #If player is destroyed, go to gameover state
        if self.player.get_destroyed():
            return State.GAMEOVER

        #Check if any of the enemies touched the bottom of the screen
        if [x for x in self.enemies if x.get_y() > self.game_height - self.player.get_height()]:
            if self.debug:
                print("Alien hit the player")

            #If so it is gameover for the player
            return State.GAMEOVER

        #Spawn Enemies
        if len(self.enemies) == 0:
            self.spawn_aliens(11)

        #Draw the score
        score = self.font.render("Score : " + str(self.score), True, WHITE)
        self.screen.blit(score, (10, 10))

        #Draw the live count
        lives = self.font.render("Lives : " + str(self.player.get_lives()), True, WHITE)
        self.screen.blit(lives, (self.game_width - self.game_height//12,10))

        #Update the keypress of the player
        self.update_keypresses()

        #Check object collisions
        self.score += self.check_collisions()

        #Update the moving objs
        self.update()

        #Return play state
        return State.PLAY

    def handle_gameover(self) -> State:
        """Handles drawing of the gameover screen"""

        #Update the stay status
        stay = self.end_update_keypresses()

        #If the player wants to stay
        if stay:

            #Keep the loop running
            running = True

            #Reset player score
            self.score = 0

            #Reset player state
            self.player.reset()

            #Remove all bullets
            self.up_bullets.empty()
            self.down_bullets.empty()

            #Remove all enemies
            self.enemies.empty()

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
            inst = self.end_font.render("Press Y to go back and N to quit", True, WHITE)
            self.screen.blit(inst, (self.game_height//12, self.game_height // 2 + self.game_height//12))
            
            #Return the gameover state
            return State.GAMEOVER


    def mainloop(self) -> None:
        """The mainloop to run the game"""

        #If debugging
        if self.debug:
            print("Running the main loop")

        #Loop variables
        running = True
        
        #Mainloop for pygame GUI
        while running:
            
            #Set the FPS
            self.clock.tick(self.fps)

            #Fill the background to black before updating the screen
            self.screen.fill(BLACK)
                
            #Load the screen based on the state
            self.state = self.states[self.state]()

            #Update the display with the screen
            pygame.display.update()

            #If the state is quit or player wats
            if self.state == State.QUIT or pygame.QUIT in map(lambda x: x.type, pygame.event.get()):
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
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int, game_width:int, game_height:int, debug:bool):
        """Constructor class for the moving object"""
        #Call the superclass init method
        super().__init__()

        #Storing the variables
        self.x = initial_x
        self.y = initial_y
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.game_width = game_width
        self.game_height = game_height
        self.debug = debug
        self.sensitivity = sensitivity
        self.changed = True
        
        #Load the image model
        self.image = pygame.image.load(obj_path)

        #Load the rect
        self.rect = self.image.convert().get_rect(center=(initial_x,initial_y))

    def move(self,x,y) -> None:
        """Main Move Method"""
        #Add the values to x and y to change position
        self.x += x
        self.y += y

        #Informed that rect has changed
        self.changed = True

    def move_up(self, length:int = None) -> None:
        """Move the object up"""
        return self.move(0,-length if length else -self.sensitivity)

    def move_down(self, length:int = None) -> None:
        """Move the object down"""
        return self.move(0,length if length else self.sensitivity)

    def move_left(self, length:int = None) -> None:
        """Move the object right"""
        return self.move(-length if length else -self.sensitivity,0)

    def move_right(self, length:int = None) -> None:
        """Move the object right"""
        return self.move(length if length else self.sensitivity,0)

    def get_x(self) -> int:
        """Get the x coord of the obj"""
        return self.x

    def get_y(self) -> int:
        """Get the y coord of the obj"""
        return self.y

    def update(self) -> None:
        """Update the object rect position"""

        #Set the position of the rect if it has changed from before
        if self.changed:
            self.rect = self.image.convert().get_rect(center=(self.x,self.y))
            self.changed = False

    def scale(self, width:int, height:int) -> None:
        """Scale the image"""
        
        #Scale the image to the new width and height defined
        self.image = pygame.transform.scale(self.image, (width, height))

        #Reload the rect
        self.rect = self.image.convert().get_rect(center=(self.x, self.y))

    def get_height(self) -> None:
        """Get the height of the image"""
        return self.image.get_height()

    def get_width(self) -> None:
        """Get the width of the image"""
        return self.image.get_width()

class Direction(enum.Enum):
    """Direction enum to store where objects are moving"""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Bullet(MovingObject):
    """Bullet class for the space invaders game"""
    
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int, direction:Direction, game_width:int, game_height:int, debug:bool):
        """The constructor for the bullet class"""
        #Call the superclass
        super().__init__(obj_path, sensitivity, initial_x, initial_y, game_width, game_height, debug)

        #Store the direction, move up it the enum is move up, else move it down
        if direction == Direction.UP:
            self.direction = self.move_up
        elif direction == Direction.DOWN:
            self.direction = self.move_down
        else:
            assert False, "Direction of bullet is invalid"

    def update(self) -> None:
        """Update the path of the bullet"""
        #Move the bullet
        self.direction()

        #Kill itself if the bullet is out of screen
        if self.y > self.game_height or self.y < 0:
            self.kill()
            #Do not continue to update position
            return

        #Update its coordinates
        return super().update()

class EnemyShip(MovingObject):
    """Enemyship obj"""
    def __init__(self, obj_path:str, sensitivity:int, initial_x:int, initial_y:int, lives:int, points:int, game_width:int, game_height:int, debug:bool):
        """Constructor for the enemy object"""

        #Call the superclass
        super().__init__(obj_path, sensitivity, initial_x, initial_y, game_width, game_height, debug)

        #Store variables
        self.lives = lives
        self.direction = Direction.RIGHT
        self.points = points

    def get_points(self) -> int:
        """Get the number of points the mob is worth"""
        return self.points

    def is_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroy 1 life of the ship"""
        if self.lives > 0:
            self.lives -= 1

    def get_lives(self) -> int: 
        """Gets the number of lives the ship has left"""
        return self.lives

    def change_direction(self):
        """Change the x direction the enemy is moving"""

        #Swap the Right and the left position
        if self.direction == Direction.RIGHT:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.RIGHT
        else:
            assert False, "Enemy ship direction is invalid"

    def update(self, multiplier:int) -> None:
        """Update the movement of the enemies"""

        #If enemyship is moving to the right and is not at the edge
        if self.direction == Direction.RIGHT and self.get_x() < self.game_width:

            #Move it to the right
            self.move_right(self.sensitivity*multiplier//1)

        #If it is moving to the left and is not at the edge
        elif self.direction == Direction.LEFT and self.get_x() > 0:

            #Move it to the left
            self.move_left(self.sensitivity*multiplier//1)

        #If it is at the edge
        else:
            #Move down
            self.move_down(self.sensitivity*4)

            #Swap direction of x movement
            self.change_direction()
            
        # if self.debug:
        #     print("Enemy updated")

        #Call superclass update
        super().update()

class EnemyShips(pygame.sprite.Group):
    def __init__(self, weight:int):
        """The main class for the enemy ships group"""

        #Initialise the superclass
        super().__init__()

        #Store variables
        self.weight = weight
    
    def update(self) -> None:
        """The update function of the group"""

        #The lower the number of enemies, the greater the speed
        super().update(self.weight//(len(self) if len(self) > 0 else 1))


class Player(MovingObject):
    """Player class"""
    def __init__(self, obj_path:str, sensitivity:int, game_width:int, game_height:int, init_life:int, fps:int ,debug:bool):
        """Constructor for the player"""
        
        #Call the superclass
        super().__init__(obj_path, sensitivity, game_width//2, game_height, game_width, game_height, debug)

        #Invicibility when it just spawned
        self.invincible = fps

        #Scale the player character
        self.scale(self.get_width()*2, self.get_height()*2)

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

    def move_up(self) -> None:
        """Move the player up"""
        #If the position is not at the max position allow the player to move up
        if self.y > self.image.get_height()//8:
            # super().move_up()
            pass
        elif self.debug:
            print("Hit Top most")

    def move_down(self) -> None:
        """Move the player down"""
        #If the player is not at the bottom of the screen allow the player to move down
        if self.y <= self.game_height:
            # super().move_down()
            pass
        elif self.debug:
            print("Hit Bottom most")

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

    def get_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroys the ship 1 time"""
        if not self.invincible:
            self.life -= 1 

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

        #Call the super update
        return super().update()

def main() -> None:
    """The main function for the file"""
    print("Please run the main.py file")

#Run the main function if this file is main
if __name__ == "__main__":
    main()