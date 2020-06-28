#!/usr/bin/env python
import pygame
import pygame.freetype
import random
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
    from .InstructionsScreen import InstructionScreen
    from .MenuScreen import MenuScreen
    from .PlayScreen import PlayScreen
    from .GameoverScreen import GameoverScreen
    from .PauseScreen import PauseScreen
    from .EnemyGroup import EnemyShips
    from .HighscoreScreen import HighscoreScreen
    from .NewhighscoreScreen import NewhighscoreScreen
    
except ImportError as exp:
    from Enums import *
    from database import ScoreBoard
    from Player import Player
    from Bullet import Bullet
    from EnemyShip import EnemyShip
    from Explosion import Explosion
    from Background import Background
    from Colors import *
    from InputBox import InputBox
    from InstructionsScreen import InstructionScreen
    from MenuScreen import MenuScreen
    from PlayScreen import PlayScreen
    from GameoverScreen import GameoverScreen
    from PauseScreen import PauseScreen
    from EnemyGroup import EnemyShips
    from HighscoreScreen import HighscoreScreen
    from NewhighscoreScreen import NewhighscoreScreen

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
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple,
                 enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, explosion_img_paths:tuple, 
                 p_settings:dict, wave:int = 1,  debug:bool = False):
        """The constructor for the main window
            Arguments:
                Sensitivity: Sensitivity of controls (int)
                maxfps: Max fps for the game to go (int)
                game_width: Width of the game window (int)
                game_height: Height of the game window (int)
                icon_img_path: Path to icon image (string)
                player_img_paths: Paths to all player images (tuple of string)
                enemy_img_paths: Paths to all enemy sprites (tuple of string)
                bullet_img_paths: Paths to all the bullet sprites (tuple of string)
                background_img_path: Path to the background (string)
                explosion_img_paths: Path to all the explosion sprites (string)
                p_settings: Dictionary of setting values (dictionary)
                wave: Wave of the mobs to start (int): default = 1
                debug: Toggle whether the game is in debug mode (bool): default = False

            Methods:
                handle_newhighscore: Handles the display of new highscores
                handle_pause: Handles the display of the pause screen
                handle_gameover: Handles the state of the gameover screen
                get_state: Get the current state of the game
                mainloop: Run the mainloop for the gamewindow
        """

        #Set the title
        pygame.display.set_caption("Space Invaders")

        #Load and set the Icon
        icon = pygame.image.load(icon_img_path)
        pygame.display.set_icon(icon)

        #Set the dimensions
        self.main_screen = pygame.display.set_mode((game_height,game_width))
        self.screen = pygame.Surface((game_height,game_width), pygame.SRCALPHA, 32)

        #Initialise the pygame window
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((game_width,game_height))

        #Storing the game variables
        self.p_settings = p_settings
        self.debug = debug
        self.score = 0
        self.fps = maxfps
        self.sensitivity = sensitivity
        self.game_width = game_width
        self.game_height = game_height
        self.state = State.MENU
        self.written = False
        self.difficulty = Difficulty(p_settings['difficulty'] if p_settings['difficulty'] < 5 else 5)

        #Load the highscores
        self.score_board = ScoreBoard("data/test.db") #TODO To be changed when game is officially launched

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

        #Create the Screen objects
        self.instructions = InstructionScreen(game_width, game_height, self.main_screen, debug = self.debug)
        self.menu = MenuScreen(game_width, game_height, self.main_screen, debug = self.debug)
        self.play = PlayScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug = self.debug)
        self.highscore = HighscoreScreen(game_width, game_height, self.main_screen, self.score_board.fetch_all(), debug = self.debug)
        
        #Store the different states the menu has
        self.states = {
            State.MENU:self.menu.handle,
            State.PLAY:self.play.handle,
            State.HIGHSCORE:self.highscore.handle,
            State.NEWHIGHSCORE:self.handle_newhighscore,
            State.GAMEOVER:self.handle_gameover,
            State.INSTRUCTIONS:self.instructions.handle,
            State.PAUSE:self.handle_pause,
            State.QUIT:self.__del__
        }

        #Create the background object
        self.bg = Background(p_settings['bg'], game_width, game_height)

    def handle_newhighscore(self) -> State:
        """Handle the displaying of the highscore screen
            Arguments: 
                No arguments
            Returns:
                Returns the state the game is suppose to be in next (State)
        """
        #Create the new highscore screen
        self.newhighscore = NewhighscoreScreen(self.game_width, self.game_height, self.main_screen, self.play.get_score())

        #Get the next state
        state = self.newhighscore.handle()

        #If the state is gameover
        if state == State.GAMEOVER:
            
            #Debugging information
            if self.debug:
                print(f"Name:{NewhighscoreScreen.get_name()}\nScore:{self.play.get_score()}")

            #Update the score of the player
            self.highscore.update_score(self.newhighscore.get_name(), self.play.get_score())

            #Clear the input box
            NewhighscoreScreen.inputbox.clear()
            
            #Mark as highscore written
            self.written = True

        #Return the next state
        return state

    def handle_pause(self) -> State:
        """Handle the displaying of the pause screen
            Arguments:
                No arguments
            Returns:
                Returns the next state the game is suppose to be in (State)
        """
        #Create the pause screen
        self.pause = PauseScreen(self.game_width,self.game_height, self.main_screen, self.play.get_score(), self.debug)

        #Handle the pause screen
        return self.pause.handle()
        
    def handle_gameover(self) -> State:
        """Handle the displaying of the gameover screen
            Arguments: 
                No arguments
            Returns: 
                Returns the next state the game is suppose to be in (State)
        """
        #If it is a new highscore
        if self.highscore.beat_highscore(self.play.get_score()) and not self.written:

            #Go to the new highscore state
            return State.NEWHIGHSCORE

        #Create the gameover screen
        self.game_over = GameoverScreen(self.game_width,self.game_height, self.main_screen, self.play.get_score(), self.debug)

        #Check the state given by gameover
        state = self.game_over.handle()

        #If player is going back
        if state == State.MENU:

            #Mark written as false
            self.written = False

            #Reset the play screen
            self.play.reset()

        #Return the state
        return state

    def get_state(self) -> State:
        """Return the state the game is in
            Arguments:
                No arguments
            Returns: 
                Returns the current state of the game (State)
        """
        return self.state

    def mainloop(self) -> None:
        """The mainloop to load the screen of the game
            Arguments: 
                No arguments
            Returns:
                No return
        """

        #Print the mainloop run based on debug mode
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
        """Destructor for the game window.
            Closes all the relavent processes
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #Add the new highscores into DB
        self.score_board.add_all(*self.highscore.get_scores())

        #Remove all entries beyond 5
        self.score_board.remove_all(*self.highscore.get_removed())

        #Close the database
        self.score_board.__del__()

        #Quit the game
        pygame.display.quit()
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()