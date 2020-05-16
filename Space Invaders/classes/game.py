#!/usr/bin/env python
import pygame
import pygame.freetype
import enum
import sys
import random
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
    PAUSE = 4
    QUIT = -1
    

class GameWindow(object):
    """The main game window for Space invaders"""
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple, enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, p_settings:dict, wave:int = 1,  debug:bool = False):
        """The constructor for the main window"""

        #Storing the variables
        self.fps = maxfps
        self.p_settings = p_settings
        self.debug = debug
        self.score = 0
        self.game_width = game_width
        self.game_height = game_height
        self.wave = wave-1
        self.state = State.MENU
        self.sensitivity = sensitivity
        self.bullet_cooldown = 0
        self.spawn_state = 0

        #Store the different states the menu has
        self.states = {
            State.MENU:self.handle_menu,
            State.PLAY:self.handle_play,
            State.GAMEOVER:self.handle_gameover,
            State.PAUSE:self.handle_pause,
            State.QUIT:self.__del__
        }

        #Initialise pygame
        pygame.init()

        #Initialise the font
        pygame.font.init()

        #Initialise the sound
        pygame.mixer.init()

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
        self.enemies = EnemyShips() #Enemies

        #Load player ship images into Player object 
        self.add_to_sprite(Player, player_img_paths)

        #Load Bullet images into Bullet Object 
        self.add_to_sprite(Bullet, bullet_img_paths)

        #Load enemy ships into enemy ship objects 
        self.add_to_sprite(EnemyShip, enemy_img_paths)

        #Load the backgrounds into Background obj
        self.add_to_sprite(Background, background_img_paths)

        #Create the main sprites
        self.player = Player(self.p_settings['ship']-1, sensitivity, game_width, game_height - 50, 3, maxfps, debug)

        #Create the background object
        self.bg = Background(p_settings['bg']-1, game_width, game_height)

        #Other sprites
        self.font = pygame.font.Font(pygame.font.get_default_font(),game_width//40)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(),game_width//20)
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), game_width // 10)

    def add_to_sprite(self, obj:object, sprite_path:tuple) -> None:
        """Add the pygame image to the object"""

        #For each object add it to the sprite path
        for path in sprite_path:
            obj.sprites.append(pygame.image.load(path))

    def get_state(self) -> State:
        """Return the state the game is in"""
        return self.state

    def update_keypresses(self) -> bool:
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
        if keys[K_SPACE] and not self.bullet_cooldown:

            #Spawn a bullet
            self.spawn_bullets()

            #Set the bullet on cooldown
            self.bullet_cooldown = self.fps // (3 * 0.95 ** self.wave)

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

    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies into the game"""
        #Adding sprites
        if number <= 6:
            self.enemies.add([EnemyShip(self.sensitivity, self.game_width//4 + i*self.game_width//10, self.game_height//10, random.randint(1,self.wave), self.game_width,  self.game_height, self.debug) for i in range(number)])
        else:
            for j in range(number//6 if number // 6 < 5 else 5):
                self.enemies.add([EnemyShip(self.sensitivity, self.game_width//4 + i*self.game_width//10, self.game_height//10 + EnemyShip.sprites[0].get_height() * j, random.randint(1,self.wave), self.game_width,  self.game_height, self.debug) for i in range(6)])
            
    def check_collisions(self) -> int:
        """Check the objects which collided"""
        #Check if player has collided with bullets
        bullet_collide = pygame.sprite.spritecollide(self.player, self.down_bullets, True)
        
        #If the set is not empty reduce player life
        if len(bullet_collide) > 0:

            #If it is in debug mode, print the event
            if self.debug:
                print("Player hit")

            #Destroy 1 of the player's life
            self.player.destroy()

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.up_bullets, self.down_bullets, True, True)

        #Get ships destroyed
        ships = list(pygame.sprite.groupcollide(self.up_bullets, self.enemies, True, False).values())

        if self.debug:
            print(ships)

        if ships:
        #Destroy the first ship in the list
            ships[0][0].destroy()
            if self.debug:
                print(f"Ship destroyed")
        
            #Remove the ship from groupp if it has 0 lives
            if ships[0][0].is_destroyed():

                #Remove the sprite from the group
                self.enemies.remove(ships[0][0])

                #Remove sprites that collide with bullets and return the sum of all the scores
                return ships[0][0].get_points()

        #If nothing is destroyed return 0
        return 0

    def update(self) -> None:
        """Update the player obj onto the screen"""

        #Update the player position
        self.player.update()

        #Update the enemy group
        self.enemies.update()

        #Spawn bullets for enemies
        self.spawn_enemy_bullets()

        #Update the bullets positions
        self.up_bullets.update()
        self.down_bullets.update()
        self.up_bullets.draw(self.screen)
        self.down_bullets.draw(self.screen)
        if self.debug:
            print(f"Number of player bullets: {len(self.up_bullets)}")

        #Draw the enemy
        self.enemies.draw(self.screen)
        if self.debug:
            print(f"Number of enemies: {len(self.enemies)}")

        #Draw player object
        self.screen.blit(self.player.image, self.player.rect)

    def spawn_enemy_bullets(self) -> None:
        """Spawns a bullet randomly for the enemy"""
        #Check if the enemy can shoot
        rand = random.randint(0,self.fps*50)
        if rand > self.fps:
            if self.debug:
                print(f"Random generated: {rand}")
            return

        #Get a random bullet for the entity to shoot
        if len(self.enemies):
            enemy = random.sample(set(self.enemies),1)
        else:
            enemy = None

        #If the set is non-empty
        if enemy:

            #Get the first element of the set
            enemy = enemy[0]

        if self.debug:
            print(enemy)

        #Create the bullet
        bullet2 = Bullet(self.sensitivity * 1.5, enemy.get_x() + enemy.get_width()//3, enemy.get_y(), Direction.DOWN, self.game_width, self.game_height, self.debug)

        #Add the bullet to the bullet group
        self.down_bullets.add(bullet2)

    def spawn_bullets(self):
        """Spawn the bullets for each of the entities"""

        #Spawn bullet for the player
        #Create the bullet object
        bullet = Bullet(self.sensitivity * 1.5, self.player.get_x() + self.player.get_width()//3, self.player.y, Direction.UP, self.game_width, self.game_height, self.debug)

        #Add the bullet to the bullet group
        self.up_bullets.add(bullet)
        

    def check_mouse_pos(self, rect_play, rect_end):
        """Check the position of the mouse on the menu to see what the player clicked"""
        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()

        #Set click to false
        click = False

        #If player pressed the button
        if pygame.mouse.get_pressed()[0]:
            if self.debug:
                print(f"Mouse clicked {pygame.mouse.get_pressed()}")
            click = True

        #If mousedown and position colide with play
        if rect_play.collidepoint(mouse_pos) and click:
            return State.PLAY

        #If mousedown and position colide with quit
        elif rect_end.collidepoint(mouse_pos) and click:
            return State.QUIT

        #Otherwise the player has not decided
        else:
            #Return menu state
            return State.MENU

    def pause_update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen"""

        #Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        #Return the play state if the player unpause his game
        if keys[K_o]:
            return State.PLAY
        
        #Return the current state if the player has not unpaused
        return State.PAUSE

    def handle_pause(self) -> State:
        """Handles the drawing of the pause screen"""

        #Draw the title of the pause screen
        title = self.title_font.render("Paused", True, WHITE)
        rect_title = title.get_rect(center = (self.game_width//2, self.game_height//5))
        self.screen.blit(title, rect_title)

        #Draw the instructions to unpause
        inst1 = self.end_font.render("Press O to unpause", True, WHITE)
        rect_inst1 = inst1.get_rect(center=(self.game_width//2, self.game_height//15 + self.game_height//2))
        self.screen.blit(inst1, rect_inst1)

        #Detect the keypress for the unpause button
        return self.pause_update_keypresses()

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
        inst1 = self.end_font.render("Use AD or arrow keys to move", True, WHITE)
        rect_inst1 = inst1.get_rect(center=(self.game_width//2, self.game_height//1.5))
        self.screen.blit(inst1, rect_inst1)

        inst2 = self.end_font.render("Press Spacebar to shoot, P to pause", True, WHITE)
        rect_inst2 = inst2.get_rect(center=(self.game_width//2, self.game_height//1.5 + self.game_height//15))
        self.screen.blit(inst2, rect_inst2)

        #Check the position of the mouse to return the state
        return self.check_mouse_pos(rect_play, rect_end)

    def handle_play(self) -> State:
        """Handles the drawing of the play string"""

        #If player is destroyed, go to gameover state
        if self.player.is_destroyed():
            return State.GAMEOVER

        #Check if any of the enemies touched the bottom of the screen
        if [x for x in self.enemies if x.get_y() > self.game_height - self.player.get_height()]:

            #If it is debugging mode, print out what happened
            if self.debug:
                print("Alien hit the player")
                
            #If so it is gameover for the player
            return State.GAMEOVER

        #Spawn if there are no enemies 
        if not len(self.enemies):

            #Increase the wave number
            self.wave += 1

            #Spawn the aliens
            self.spawn_enemies(int(6 * self.wave))

        #Draw the score
        score = self.font.render(f"Score : {self.score}" , True, WHITE)
        self.screen.blit(score, (10, 10))

        #Draw the live count
        lives = self.font.render(f"Lives : {self.player.get_lives()}", True, WHITE)
        self.screen.blit(lives, (self.game_width - self.game_height//12,10))

        #Draw the wave number
        wave = self.font.render(f"Wave : {self.wave}", True, WHITE)
        self.screen.blit(wave, (self.game_width//2, 10))

        #Check object collisions
        self.score += self.check_collisions()

        #Check the player keypress
        self.update_keypresses()

        #Update the moving objs
        self.update()

        #Check if the player wants to pause
        if len(list(filter(lambda x: x.type == pygame.KEYDOWN and x.key == K_p, pygame.event.get()))):
            return State.PAUSE

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

            #Fills the background
            if self.bg.is_present():
                #Fill it with the background img
                self.bg.update(self.screen)
            else:
                #Fill the background to black 
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

class Background(pygame.sprite.Sprite):
    sprites = []
    def __init__(self, bg_no:int, game_width:int, game_height:int):
        """Constructor for the background class"""

        #Calls the superclass
        super().__init__()

        #Gets the background image if any
        self.image = Background.sprites[bg_no] if bg_no >= len(Background.sprites) else None
        self.rect = None

        #If there is a background image get the rect for it
        if self.image != None:

            #Scale the image to the correct size
            self.image = pygame.transform.scale(self.image, (game_width, game_height))

            #Get the rect
            self.rect = self.image.get_rect()

            #Set the top left of rect to top left of the game
            self.rect.left, self.rect.top = 0,0

    def is_present(self) -> bool:
        """Check if there is a valid background"""
        return self.image

    def update(self, screen) -> None:
        """Blit the background to the screen"""
        screen.blit(self.image, self.rect)

class MovingObject(pygame.sprite.Sprite):
    """Main class for all objects that move"""

    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, game_width:int, game_height:int, debug:bool):
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

        #Load the rect
        self.load_rect()

    def load_rect(self):
        """Load the rectangle for the obj"""
        #Create the rectangle for the MovingObject Object
        self.rect = pygame.Rect(self.image.get_rect().left, self.image.get_rect().top, self.get_width(), self.get_height())
        self.rect.center=(self.x,self.y)

        #Inflate the model to the correct size
        self.rect.inflate(self.get_width()//2,self.get_height()//2)

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
            self.load_rect()
            self.changed = False

    def scale(self, width:int, height:int) -> None:
        """Scale the image"""
        
        #Scale the image to the new width and height defined
        self.image = pygame.transform.scale(self.image, (width, height))

        #Reload the rect
        self.load_rect()

    def get_height(self) -> None:
        """Get the height of the image"""
        return self.image.get_height()

    def get_width(self) -> None:
        """Get the width of the image"""
        return self.image.get_width()

class Direction(enum.Enum):
    """Direction enum to store where objects are moving"""
    UP = 1
    DOWN = -1
    LEFT = -2
    RIGHT = 2

class Bullet(MovingObject):
    """Bullet class for the space invaders game"""
    #Static method to store sprites
    sprites = []
    
    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, direction:Direction, game_width:int, game_height:int, debug:bool):
        """The constructor for the bullet class"""
        #Load the image 
        self.image = self.sprites[0]

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, debug)

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
    #Static method to store sprites
    sprites = []
    def __init__(self, sensitivity:int, initial_x:int, initial_y:int, lives:int,  game_width:int, game_height:int, debug:bool):
        """Constructor for the enemy object"""

        #Load the correct image
        self.image = self.sprites[lives-1 if lives < len(EnemyShip.sprites) else len(EnemyShip.sprites)-1]

        #Call the superclass
        super().__init__(sensitivity, initial_x, initial_y, game_width, game_height, debug)

        #Store variables
        self.lives = lives
        self.direction = Direction.RIGHT
        self.points = 10 * self.lives

    def get_points(self) -> int:
        """Get the number of points the mob is worth"""
        return self.points

    def is_destroyed(self) -> bool:
        """Returns whether the ship is destroyed"""
        return self.get_lives() == 0

    def destroy(self) -> None:
        """Destroy 1 life of the ship"""
        if self.lives:
            self.lives -= 1
            if not self.is_destroyed():
                self.image = self.sprites[self.lives-1 if self.lives < len(EnemyShip.sprites) else len(EnemyShip.sprites)-1]

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
            self.move_down(self.get_height()//4)

            #Swap direction of x movement
            self.change_direction()
            
        # if self.debug:
        #     print("Enemy updated")

        #Call superclass update
        super().update()

class EnemyShips(pygame.sprite.Group):
    def __init__(self):
        """The main class for the enemy ships group"""

        #Initialise the superclass
        super().__init__()

    
    def update(self) -> None:
        """The update function of the group"""

        #The lower the number of enemies, the greater the speed
        super().update(2 // (len(self) if len(self) > 0 else 1))


class Player(MovingObject):
    """Player class"""
    #Static method to store sprites
    sprites = []
    def __init__(self, ship_no:int, sensitivity:int, game_width:int, game_height:int, init_life:int, fps:int ,debug:bool):
        """Constructor for the player"""
        #Load the image
        if ship_no < len(Player.sprites):
            self.image = Player.sprites[ship_no]
        else:
            self.image = Player.ships[0]
        
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

        #Call the super update
        return super().update()

def main() -> None:
    """The main function for the file"""
    print("Please run the main.py file")

#Run the main function if this file is main
if __name__ == "__main__":
    main()