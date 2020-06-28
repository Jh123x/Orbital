#!/usr/bin/env python
import pygame
<<<<<<< HEAD
import random
import datetime
import asyncio
import time
from pygame.locals import *
from . import *
=======
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
>>>>>>> master

#Initialise pygame
pygame.init()

#Initialise the font
pygame.font.init()

#Initialise the sound
pygame.mixer.init()

<<<<<<< HEAD
def load_sprites(obj_list:list, paths:list):
    """Load the sprites for each of the items in parallel"""

    #Run functions concurrently
    for i, obj in enumerate(obj_list):
        asyncio.run(add_to_sprite(obj, paths[i]))

async def add_to_sprite(obj, sprite_path:str) -> None:
=======
def add_to_sprite(obj:object, sprite_path:tuple) -> None:
>>>>>>> master
    """Add the pygame image to the object"""
    #For each object add it to the sprite path
    for path in sprite_path:
        obj.sprites.append(pygame.image.load(path))

<<<<<<< HEAD
async def load_sound(sound_path:str, settings:int, debug:bool) -> Sound:
    """Load the sound object"""
    return Sound(dict(map(lambda x: (x[0], pygame.mixer.Sound(x[1])), sound_path.items())), bool(int(settings)), debug)

class GameWindow(object):
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple,
                 enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, explosion_img_paths:tuple, 
                 db_path:str, sound_path:dict, bg_limit:int, wave:int = 1,  debug:bool = False):
=======
class GameWindow(object):
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple,
                 enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, explosion_img_paths:tuple, 
                 p_settings:dict, wave:int = 1,  debug:bool = False):
>>>>>>> master
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
<<<<<<< HEAD
                db_path: Path to the database file
=======
>>>>>>> master
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
<<<<<<< HEAD
        self.main_screen = pygame.display.set_mode((game_width,game_height))

        #Initialise the pygame window
        self.clock = pygame.time.Clock()
=======
        self.main_screen = pygame.display.set_mode((game_height,game_width))
        self.screen = pygame.Surface((game_height,game_width), pygame.SRCALPHA, 32)

        #Initialise the pygame window
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((game_width,game_height))

        #Storing the game variables
        self.p_settings = p_settings
>>>>>>> master
        self.debug = debug
        self.score = 0
        self.fps = maxfps
        self.sensitivity = sensitivity
        self.game_width = game_width
        self.game_height = game_height
<<<<<<< HEAD

        #Starting State
        self.state = State.MENU

        #Check if highscore is written
        self.written = False

        #Load the highscores
        self.score_board = ScoreBoard(db_path)

        #Load setting menu settings
        self.settingsdb = SettingsDB(db_path)
        self.settings_data = dict(map(lambda x: x[1:], self.settingsdb.fetch_all()))

        #Set difficulty
        difficulty = int(self.settings_data['difficulty'])
        self.difficulty = Difficulty(difficulty if difficulty < 5 else 5)

        #Load sprites
        load_sprites((Player, Bullet, EnemyShip, Background, Explosion), (player_img_paths, bullet_img_paths, enemy_img_paths, background_img_paths, explosion_img_paths))

        #Load sounds
        self.sound = asyncio.run(load_sound(sound_path,self.settings_data['music'],self.debug))

        #Create the background object
        self.bg = Background(int(self.settings_data['background']), game_width, game_height, bg_limit, debug)

        #Create the Screen objects
        self.instructions = InstructionScreen(game_width, game_height, self.main_screen,  debug = self.debug)
        self.menu = MenuScreen(game_width, game_height, self.main_screen, debug = self.debug)
        self.play = PlayScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, 3, debug = self.debug)
        self.play_menu = PlayModeScreen(game_width, game_height, self.main_screen,  debug)
        self.highscore = HighscoreScreen(game_width, game_height, self.main_screen, self.score_board.fetch_all(), debug = self.debug)
        self.two_player = TwoPlayerScreen(game_width, game_height, self.main_screen,  self.debug)
        self.pvp = LocalPVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3,  debug)
        self.pvp_menu = PVPInstructionsScreen(game_width, game_height, self.main_screen, debug)
        self.inst_menu = InstructionsMenuScreen(game_width, game_height, self.main_screen,  debug)
        self.classic = ClassicScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, debug = self.debug)
        self.settings = SettingsScreen(game_width, game_height, self.main_screen, self.fps, self.sound, self.bg, self.difficulty, debug)
        self.coop = CoopScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, 3,  debug)
        self.ai_vs = AIPVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3,  debug)
        self.online = OnlinePVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3,  debug)

        #Store the variables
        self.popup = None
        self.prev = State.NONE
        self.cooldown = self.fps/5
=======
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
>>>>>>> master
        
        #Store the different states the menu has
        self.states = {
            State.MENU:self.menu.handle,
<<<<<<< HEAD
            State.PLAYMODE:self.play_menu.handle,
=======
>>>>>>> master
            State.PLAY:self.play.handle,
            State.HIGHSCORE:self.highscore.handle,
            State.NEWHIGHSCORE:self.handle_newhighscore,
            State.GAMEOVER:self.handle_gameover,
<<<<<<< HEAD
            State.INSTRUCTIONS_MENU: self.inst_menu.handle,
            State.INSTRUCTIONS:self.instructions.handle,
            State.PVP_INSTRUCTIONS: self.pvp_menu.handle,
            State.PAUSE:self.handle_pause,
            State.TWO_PLAYER_MENU: self.two_player.handle,
            State.AI_COOP: self.two_player.handle,
            State.AI_VS: self.ai_vs.handle,
            State.PVP: self.pvp.handle,
            State.TWO_PLAYER_GAMEOVER:self.handle_two_player_gameover,
            State.TWO_PLAYER_PAUSE: self.handle_two_player_pause,
            State.CLASSIC: self.classic.handle,
            State.SETTINGS: self.settings.handle,
            State.COOP: self.coop.handle,
            State.ONLINE: self.online.handle,
            State.QUIT:self.__del__
        }

        #Load the sounds into the relavant Sprites
        Bullet.sound = self.sound

        #Add explosion sound
        Explosion.sound = self.sound

        #Add pause sound
        TwoPlayerPauseScreen.sound = self.sound
        PauseScreen.sound = self.sound
        GameoverScreen.sound = self.sound
        TwoPlayerGameoverScreen.sound = self.sound

    def handle_two_player_pause(self) -> State:
        """Handle the PVP pause screen"""

        #Check based on previous state
        if self.prev == State.PVP:
            prev = State.PVP
            prevs = self.pvp
            scores = self.pvp.get_scores()
        elif self.prev == State.COOP:
            prev = State.COOP
            prevs = self.coop
            scores = self.coop.get_scores()
        elif self.prev == State.AI_VS:
            prev = State.AI_VS
            pres = self.ai_vs
            scores = self.ai_vs.get_scores()
        else:
            assert False, f"{self.state}, cannot be paused"

        #Create the pause screen
        self.two_player_pause = TwoPlayerPauseScreen(self.game_width, self.game_height, self.main_screen, *scores, self.prev, self.debug)

        #Return the function
        state = self.two_player_pause.handle()

        #If new state is menu state
        if state == State.MENU:

            #Reset the state
            pres.reset()
            return state

        #If it goes back to the game
        elif state != State.TWO_PLAYER_PAUSE:
            return prev

        #Otherwise return the state
        return state
=======
            State.INSTRUCTIONS:self.instructions.handle,
            State.PAUSE:self.handle_pause,
            State.QUIT:self.__del__
        }

        #Create the background object
        self.bg = Background(p_settings['bg'], game_width, game_height)
>>>>>>> master

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
<<<<<<< HEAD

        #Get the correct score
        if self.prev == State.PLAY:
            score = self.play.get_score()
            
        elif self.prev == State.CLASSIC:
            score = self.classic.get_score()
        
        else:
            assert False, "Invalid game mode"

        #Create the pause screen
        self.pause = PauseScreen(self.game_width,self.game_height, self.main_screen, score, self.prev, self.debug)

        #Handle the pause screen
        state = self.pause.handle()

        if state != self.prev:
            if self.prev == State.PLAY:
               self.play.reset()
                
            elif self.prev == State.CLASSIC:
                self.classic.reset()

        return state

    def handle_two_player_gameover(self) -> State:
        """Handle the PVP gameover screen"""
        #Check based on previous state
        if self.prev == State.PVP:
            prev = State.PVP
            pres = State.pvp
            scores = self.pvp.get_scores()

        elif self.prev == State.COOP:
            prev = State.COOP
            pres = self.coop
            scores = self.coop.get_scores()

        elif self.prev == State.AI_VS:
            prev = State.AI_VS
            pres = self.ai_vs
            scores = self.ai_vs.get_scores()

        elif self.prev == State.ONLINE:
            prev = State.ONLINE
            pres = self.online
            scores = self.online.get_scores()

        else:
            assert False, f"{self.state}, cannot have gameover"

        #Generate gameover screen
        self.pvp_gameover = TwoPlayerGameoverScreen(self.game_width, self.game_height, self.main_screen, *scores)

        #Get next state
        state = self.pvp_gameover.handle()

        #If the gameoverscreen is over
        if state != State.TWO_PLAYER_GAMEOVER:
            pres.reset()

        #Return the state
        return state
=======
        #Create the pause screen
        self.pause = PauseScreen(self.game_width,self.game_height, self.main_screen, self.play.get_score(), self.debug)

        #Handle the pause screen
        return self.pause.handle()
>>>>>>> master
        
    def handle_gameover(self) -> State:
        """Handle the displaying of the gameover screen
            Arguments: 
                No arguments
            Returns: 
                Returns the next state the game is suppose to be in (State)
        """
<<<<<<< HEAD

        #Check previous state
        if self.prev == State.PLAY or self.prev == State.NEWHIGHSCORE:

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

        #If it is classic mode
        elif self.prev == State.CLASSIC:

            #Create the gameover screen
            self.game_over = GameoverScreen(self.game_width,self.game_height, self.main_screen, self.classic.get_score(), self.debug)

            #Check the state given by gameover
            state = self.game_over.handle()

            #If player is going back
            if state == State.MENU:

                #Mark written as false
                self.written = False

                #Reset the play screen
                self.classic.reset()
=======
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
>>>>>>> master

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

<<<<<<< HEAD
    async def screenshot(self) -> None:
        """Take a screenshot
            Runs in parallel to the game to reduce lag while screenshotting in game
        """
        #Save a screenshot named based on date and time
        name = f'screenshots/{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.png'

        #Play the screenshot sound
        self.sound.play('screenshot')

        #Print debug message
        if self.debug:
            print(f"Saved at: {name}")
        
        #Save the image
        pygame.image.save(self.main_screen, name)

    def check_keypresses(self) -> None:
        """Check global keypresses within the game
            Arguments:
                No arguments
            Returns:
                No return
        """

        #Get the keys which are pressed
        keys = pygame.key.get_pressed()

        #Check each key individually
        if keys[K_x] and self.state != State.NEWHIGHSCORE:

            #Run the screenshot in parallel
            asyncio.run(self.screenshot())

            #Create a 1 second popup saying screenshot is taken 
            self.popup = Popup(20*8, 30, "Screenshot taken", self.fps, self.game_width//2, 15, self.main_screen, debug = self.debug)

    def update(self) -> None:
        """Update the main screen"""

        #If the background is present
        if self.bg.is_present():

            #Fill it with the background img
            self.bg.update(self.main_screen)
        
        #Otherwise
        else:

            #Fill the background to black
            self.main_screen.fill(BLACK)

        #Save previous state
        prev = self.state

        #If on cooldown
        if self.cooldown:

            #Lower cooldown
            self.cooldown -= 1

            #Continue running current state
            self.states[self.state]()

        #Otherwise
        else:

            #Check if there is new state
            self.state = self.states[self.state]()

        #If the state is different
        if prev != self.state:

            #Play the click sound
            self.sound.play('click')

            #Set the self.prev state
            self.prev = prev

            #Reset the cooldown
            self.cooldown = self.fps//5

            #Reset Popups
            self.popup = None


        #Check popups
        if self.popup:

            #Update popups
            self.popup.update()

=======
>>>>>>> master
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

<<<<<<< HEAD
            #Update game states
            self.update()
=======
            #If the background is present
            if self.bg.is_present():

                #Fill it with the background img
                self.bg.update(self.main_screen)
            else:

                #Fill the background to black 
                self.main_screen.fill(BLACK)

            #Load the screen based on the state
            self.state = self.states[self.state]()
>>>>>>> master

            #Update the display with the screen
            pygame.display.update()

<<<<<<< HEAD
            #Check Global keypresses
            self.check_keypresses()

=======
>>>>>>> master
            #If the state is quit or player closes the game
            if self.state == State.QUIT or pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):
                running = False

<<<<<<< HEAD
        #Play the exit sound
        self.sound.play('exit')
=======
        #Close the window
        self.__del__()
>>>>>>> master

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

<<<<<<< HEAD
        #Get the settings that was saved and save it to the DB
        self.settingsdb.update('background',str(self.settings.get_bg_no()))
        self.settingsdb.update('music',int(self.settings.get_music_enabled()))
        self.settingsdb.update('difficulty', int(self.settings.get_difficulty_no()))
=======
        #Close the database
        self.score_board.__del__()
>>>>>>> master

        #Quit the game
        pygame.display.quit()
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()
<<<<<<< HEAD

        #Debug message
        if self.debug:
            print("Closed Game Window")
=======
>>>>>>> master
