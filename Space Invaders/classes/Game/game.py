#!/usr/bin/env python
import pygame
import pygame.freetype
import random
import asyncio
from pygame.locals import *
try:
    from .Enums import *
    from .database import ScoreBoard
    from .Player import Player
    from .Bullet import Bullet
    from .EnemyShip import EnemyShip
    from .Explosion import Explosion
    from .Background import Background
    from .Colors import *
    from .InputBox import InputBox
    from .Screens import *
except ImportError:
    from Enums import *
    from database import ScoreBoard
    from Player import Player
    from Bullet import Bullet
    from EnemyShip import EnemyShip
    from Explosion import Explosion
    from Background import Background
    from Colors import *
    from InputBox import InputBox
    from Screens import *

#Initialise pygame
pygame.init()

#Initialise the font
pygame.font.init()

#Initialise the sound
pygame.mixer.init()

def add_to_sprite(obj:object, sprite_path:tuple) -> None:
    """Add the pygame image to the object"""
    #For each object add it to the sprite path
    for path in sprite_path:
        obj.sprites.append(pygame.image.load(path))

class GameWindow(object):
    """The main game window for Space invaders"""
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple,
                 enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, explosion_img_paths:tuple, 
                 p_settings:dict, wave:int = 1,  debug:bool = False):
        """The constructor for the main window"""

        #Set the dimensions
        self.main_screen = pygame.display.set_mode((game_height,game_width))
        self.screen = pygame.Surface((game_height,game_width), pygame.SRCALPHA, 32)

        #Storing the game variables
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
        self.difficulty = Difficulty(p_settings['difficulty'] if p_settings['difficulty'] < 5 else 5)
        self.written = True

        #Load the highscores
        self.score_board = ScoreBoard("data/test.db")
        self.scores = sorted(self.score_board.fetch_all(),key = lambda x: x[2], reverse = True)

        #Create the static screens
        self.instructions = InstructionScreen(game_width, game_height, self.main_screen)
        self.menu = MenuScreen(game_width, game_height, self.main_screen)
        self.settings = SettingsMenu(game_width,game_height, self.main_screen)
        
        #Store the different states the menu has
        self.states = {
            State.MENU:self.menu.handle,
            State.PLAY:self.handle_play,
            State.HIGHSCORE:self.handle_highscore,
            State.NEWHIGHSCORE:self.handle_newhighscore,
            State.GAMEOVER:self.handle_gameover,
            State.INSTRUCTIONS:self.instructions.handle,
            State.PAUSE:self.handle_pause,
            State.SETTINGS: self.settings.handle,
            State.QUIT:self.__del__
        }

        #Set the title
        pygame.display.set_caption("Space Invaders")

        #Load the Icon
        icon = pygame.image.load(icon_img_path)
        pygame.display.set_icon(icon)

        #Initialise the pygame window
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((game_width,game_height))

        #Create the main groups
        #Bullets shot by player
        self.up_bullets = pygame.sprite.Group()

        #Bullet from Mobs
        self.down_bullets = pygame.sprite.Group()

        #Enemyships
        self.enemies = EnemyShips()

        #Explosions
        self.explosions = pygame.sprite.Group()

        #Load player ship images into Player object 
        add_to_sprite(Player, player_img_paths)

        #Load Bullet images into Bullet Object 
        add_to_sprite(Bullet, bullet_img_paths)

        #Load enemy ships into enemy ship objects 
        add_to_sprite(EnemyShip, enemy_img_paths)

        #Load the backgrounds into Background obj
        add_to_sprite(Background, background_img_paths)

        #Load the sprites for the explosion
        add_to_sprite(Explosion, explosion_img_paths)

        #Create the main sprites
        self.player = Player(sensitivity, game_width, game_height - 50, 3, maxfps, debug)

        #Create the background object
        self.bg = Background(p_settings['bg'], game_width, game_height)

        #Fonts
        self.font = pygame.font.Font(pygame.font.get_default_font(),game_width//40)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(),game_width//20)
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), game_width // 10)

        #Input vars
        self.inputbox = InputBox(self.game_width//2, self.game_height//2, 100, 30, self.end_font, 5)

    def get_2d_array(self):
        """Returns the 2d array of pixels without the background
            Arguments:
                No arguments
            Returns:
                Return a 2d array of colored pixels
        """
        return pygame.surfarray.pixels3d(self.screen)
    
    def get_screen_bound(self)-> tuple:
        """
        Return the dimensions of the game screen
        """
        return (self.game_width,self.game_height)
    
    def get_score(self)-> int:
        """
        Get score of the game at this point
        """
        return self.score

    def write(self, font_type, color:Color, word:str, x_pos:int, y_pos:int, direction:Direction = Direction.CENTER) -> None:
        """Draw the object onto the screen"""
        #Write the word with the font
        sentence = font_type.render(word, True, WHITE)

        #Get the rect of the font
        if direction == Direction.CENTER:
            rect_sentence = sentence.get_rect(center = (x_pos, y_pos))
        elif direction == Direction.LEFT:
            rect_sentence = sentence.get_rect(left = x_pos, top = y_pos)

        #Draw the sentence onto the screen
        self.screen.blit(sentence, rect_sentence)

        #Return the rect for the sentence
        return rect_sentence
        

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
            self.explosions.add(Explosion(self.player,self.fps//2,self.player.get_x(),self.player.get_y(),self.game_width,self.game_height))

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.up_bullets, self.down_bullets, True, True)

        #Get ships destroyed
        ships = list(pygame.sprite.groupcollide(self.up_bullets, self.enemies, True, False).values())

        if self.debug:
            print(ships)

        #If the list of collision is non-empty
        if ships:
            #Get the ship it collided with 
            ship = ships[0][0]

            #Destroy the first ship in the list
            ship.destroy()

            if self.debug:
                print(f"Ship destroyed")
        
            #Remove the ship from groupp if it has 0 lives
            if ship.is_destroyed():

                #Spawn an explosion in its place
                self.explosions.add(Explosion(0, self.fps//4, ship.get_x(), ship.get_y(), self.game_width, self.game_height, 0, self.debug))

                #Remove the ship from all groups
                ship.kill()

                #Remove sprites that collide with bullets and return the sum of all the scores
                return ship.get_points()

        #If nothing is destroyed return 0
        return 0

    def update(self) -> None:
        """Update the player obj onto the screen"""

        #Update the player position
        self.player.update()

        #Update the enemy group
        self.enemies.update()

        #Update the explosions group
        self.explosions.update()

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

        #Draw the explosions
        self.explosions.draw(self.screen)

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

            #Create the bullet
            bullet2 = Bullet(self.sensitivity * 1.5, enemy.get_x() + enemy.get_width()//3, enemy.get_y(), Direction.DOWN, self.game_width, self.game_height, self.debug)

            #Rotate the bullet 180 degrees
            bullet2.rotate(180)

            #Add the bullet to the bullet group
            self.down_bullets.add(bullet2)

    def spawn_bullets(self):
        """Spawn the bullets for each of the entities"""

        #Create the bullet object
        bullet = Bullet(self.sensitivity * 1.5, self.player.get_center()[0], self.player.y, Direction.UP, self.game_width, self.game_height, self.debug)

        #Add the bullet to the bullet group
        self.up_bullets.add(bullet)
    
    def check_clicked(self, rect) -> bool:
        """Check if the player clicked on the rect"""

        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()

        #If player pressed the button
        return pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos)

    def pause_update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen"""

        #Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        #Return the play state if the player unpause his game
        if keys[K_o]:
            return State.PLAY

        #If the player press the escape key, quit the game
        if keys[K_ESCAPE]:
            return State.MENU
        
        #Return the current state if the player has not unpaused
        return State.PAUSE

    def handle_newhighscore(self) -> State:
        """Tell the user that he got a new highscore and enter his name"""
        #Check if the player is an AI
        if self.player.isAI():
            return State.GAMEOVER
        
        #Define new variables
        start_px = 100
        
        #Tell the user he has a new high score
        self.write(self.title_font, WHITE, f"NEW HIGH SCORE", self.game_width//2, start_px)

        #Tell the user to key in his name
        self.write(self.font, WHITE, f"Please key in your name and press enter", self.game_width//2, start_px + self.game_height//10)

        #Handle the keying in of name
        for event in tuple(filter(lambda x: x.type==pygame.KEYDOWN, pygame.event.get())):
            if event.key == K_RETURN:
                #Add the name and score to database
                self.scores.append((None, self.inputbox.get_text(), self.score))
                self.scores.sort(reverse=True, key = lambda x: x[2])
                self.written = True
                return State.GAMEOVER
            elif event.key == K_BACKSPACE:
                self.inputbox.backspace()
            else:
                self.inputbox.input(event.unicode)
        
        #Update the Inputbox
        self.inputbox.update()

        #Draw the Box
        self.inputbox.draw(self.screen)

        return State.NEWHIGHSCORE

    def handle_highscore(self) -> State:
        """Handles the drawing of the highscore screen"""

        #Draw the highscore header
        self.write(self.title_font, WHITE, f"HIGH SCORES", self.game_width//2, 100)

        #Start pixel to print the score
        start_px = 200

        #Draw the scores of the players
        for index, item in enumerate(self.scores[:5]):

            #Draw the first half of the scoreboard
            self.write(self.end_font, WHITE, f"{index+1}. {item[1]}".ljust(15, ' '), self.game_width//4, start_px + self.game_height//(15/(index+1)),Direction.LEFT)

            #Draw the 2nd half of the scoreboard
            self.write(self.end_font, WHITE, f"{item[2]:<5}",self.game_width//1.6, start_px + self.game_height//(15/(index+1)),Direction.LEFT)

        #Draw the button for back
        end_rect = self.write(self.end_font, WHITE, "Back", self.game_width//2, self.game_height//2 + self.game_height//3)

        #Check for click
        if self.check_clicked(end_rect):
            return State.MENU
        else:
            return State.HIGHSCORE

    def handle_pause(self) -> State:
        """Handles the drawing of the pause screen"""

        #Draw the title of the pause screen
        self.write(self.title_font, WHITE, "Paused", self.game_width//2, self.game_height//5)
        
        #Draw the score of the person currently
        self.write(self.end_font, WHITE, f"Score: {self.score}", self.game_width//2, self.game_height//5 + self.game_height//15)

        #Draw the instructions to unpause
        self.write(self.end_font, WHITE, "Press O to unpause", self.game_width//2, self.game_height//15 + self.game_height//2)

        #Draw the instructions to quit
        self.write(self.end_font, WHITE, "Escape to quit, score will not be saved", self.game_width//2, self.game_height//7.5 + self.game_height//2)

        #Detect the keypress for the unpause button
        return self.pause_update_keypresses()

    def handle_play(self) -> State:
        """Handles the drawing of the play string"""

        if self.written:
            self.written = False

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
        #Check if player has got a new highscore
        if not self.written and (self.score > self.scores[-1][-1] or len(self.scores) < 5):
            return State.NEWHIGHSCORE

        #Update the stay status
        stay = self.end_update_keypresses()

        #If the player wants to stay
        if stay:

            #Keep the loop running
            running = True

            #Reset player score
            self.score = 0

            #Reset Wave Number
            self.wave = 0

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
            gameover = self.write(self.title_font, WHITE, "Game Over", self.game_width//2, self.game_height//5)

            #Draw the score
            self.write(self.end_font, WHITE,"Score : " + str(self.score),self.game_width // 2, self.game_height // 2)

            #Prompt player to update
            self.write(self.end_font, WHITE, "Press Y to go back and N to quit", self.game_width//2, self.game_height // 2 + self.game_height//12)
            
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

            #If the background is present
            if self.bg.is_present():

                #Fill it with the background img
                self.bg.update(self.main_screen)
            else:

                #Fill the background to black 
                self.main_screen.fill(BLACK)

            #Load the screen based on the state
            self.state = self.states[self.state]()

            #Update the display with the screen
            pygame.display.update()

            #If the state is quit or player closes the game
            if self.state == State.QUIT or pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):
                running = False

        #Close the window
        self.__del__()

    def __del__(self) -> None:
        """Destructor for the game window"""
        #Write the new highscores into DB
        self.score_board.add_all(*self.scores)

        #Remove the last 3 entries
        self.score_board.remove_all(*self.scores[5:])

        #Close the database
        self.score_board.__del__()

        #Quit the game
        pygame.display.quit()
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()

class EnemyShips(pygame.sprite.Group):
    def __init__(self):
        """The main class for the enemy ships group"""
        #Initialise the superclass
        super().__init__()

    def update(self) -> None:
        """The update function of the group"""
        #The lower the number of enemies, the greater the speed
        super().update(2 // (len(self) if len(self) > 0 else 1))

def main() -> None:
    """The main function for the file"""
    print("Please run the main.py file")

#Run the main function if this file is main
if __name__ == "__main__":
    main()