#!/usr/bin/env python
import pygame
import pygame.freetype
import random
import datetime
from pygame.locals import *
from . import *
from .Screens import *
    

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
                 p_settings:dict, db_path:str, wave:int = 1,  debug:bool = False):
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
        self.main_screen = pygame.display.set_mode((game_width,game_height))

        #Initialise the pygame window
        self.clock = pygame.time.Clock()

        #Storing the game variables
        self.p_settings = p_settings
        self.debug = debug
        self.score = 0
        self.fps = maxfps
        self.sensitivity = sensitivity
        self.game_width = game_width
        self.game_height = game_height

        #Starting State
        self.state = State.MENU

        #Check if highscore is written
        self.written = False

        #Set difficulty
        self.difficulty = Difficulty(p_settings['difficulty'] if p_settings['difficulty'] < 5 else 5)

        #Load the highscores
        self.score_board = ScoreBoard(db_path)

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
        self.play_menu = PlayModeScreen(game_width, game_height, self.main_screen, debug)
        self.highscore = HighscoreScreen(game_width, game_height, self.main_screen, self.score_board.fetch_all(), debug = self.debug)
        self.two_player = TwoPlayerScreen(game_width, game_height, self.main_screen, self.debug)
        self.pvp = LocalPVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3, debug)
        self.pvp_menu = PVPInstructionsScreen(game_width, game_height, self.main_screen, debug)
        self.inst_menu = InstructionsMenuScreen(game_width, game_height, self.main_screen, debug)
        self.classic = ClassicScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug = self.debug)
        self.popup = None
        self.prev = None
        self.cooldown = self.fps/5
        
        #Store the different states the menu has
        self.states = {
            State.MENU:self.menu.handle,
            State.PLAYMODE:self.play_menu.handle,
            State.PLAY:self.play.handle,
            State.HIGHSCORE:self.highscore.handle,
            State.NEWHIGHSCORE:self.handle_newhighscore,
            State.GAMEOVER:self.handle_gameover,
            State.INSTRUCTIONS_MENU: self.inst_menu.handle,
            State.INSTRUCTIONS:self.instructions.handle,
            State.PVP_INSTRUCTIONS: self.pvp_menu.handle,
            State.PAUSE:self.handle_pause,
            State.TWO_PLAYER_MENU: self.two_player.handle,
            State.AI_COOP: self.two_player.handle,
            State.AI_VS: self.two_player.handle,
            State.PVP: self.pvp.handle,
            State.PVP_GAMEOVER:self.handle_PVP_gameover,
            State.PVP_PAUSE: self.handle_PVP_pause,
            State.CLASSIC: self.classic.handle,
            State.QUIT:self.__del__
        }

        #Create the background object
        self.bg = Background(p_settings['bg'], game_width, game_height)

    def handle_PVP_pause(self) -> State:
        """Handle the PVP pause screen"""
        #Create the pause screen
        self.PVP_pause = PVPPauseScreen(self.game_width, self.game_height, self.main_screen, *self.pvp.get_scores(), self.debug)

        #Return the function
        state = self.PVP_pause.handle()

        #If the state changes
        if state != State.PVP_PAUSE:
            self.pvp.reset()

        #Return the state
        return state

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
        if self.prev == State.PLAY:
            #Create the pause screen
            self.pause = PauseScreen(self.game_width,self.game_height, self.main_screen, self.play.get_score(), self.prev, self.debug)
        elif self.prev == State.CLASSIC:
            #Create the pause screen
            self.pause = PauseScreen(self.game_width,self.game_height, self.main_screen, self.classic.get_score(), self.prev, self.debug)

        #Handle the pause screen
        return self.pause.handle()

    def handle_PVP_gameover(self) -> State:
        """Handle the PVP gameover screen"""
        #Generate gameover screen
        self.pvp_gameover = PVPGameoverScreen(self.game_width,self.game_height,self.main_screen, *self.pvp.get_scores())

        #Get next state
        state = self.pvp_gameover.handle()

        #If the state changes
        if state != State.PVP_GAMEOVER:
            self.pvp.reset()

        #Return the state
        return state
        
    def handle_gameover(self) -> State:
        """Handle the displaying of the gameover screen
            Arguments: 
                No arguments
            Returns: 
                Returns the next state the game is suppose to be in (State)
        """
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

            #Save a screenshot named based on date and time
            name = f'screenshots/{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.png'

            #Print debug message
            if self.debug:
                print(name)
            
            #Save the image
            pygame.image.save(self.main_screen, name)

            #Create a 1 second popup saying screenshot is taken 
            self.popup = Popup(20*8, 30, "Screenshot taken", self.fps, self.game_width//2, 15, self.main_screen, debug = self.debug)

    def update(self) -> None:
        #If the background is present
        if self.bg.is_present():

            #Fill it with the background img
            self.bg.update(self.main_screen)
        else:

            #Fill the background to black 
            self.main_screen.fill(BLACK)

        #Save previous state
        prev = self.state

        #Load the screen based on the state
        if self.cooldown:
            self.cooldown -= 1
            self.states[self.state]()
        else:
            self.state = self.states[self.state]()

        #If the state is different
        if prev != self.state:

            #Set the self.prev state
            self.prev = prev

            #Reset the cooldown
            self.cooldown = self.fps/5

            #Reset Popups
            self.popup = None


        #Check popups
        if self.popup:

            #Update popups
            self.popup.update()

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

            #Update game states
            self.update()

            #Update the display with the screen
            pygame.display.update()

            #Check Global keypresses
            self.check_keypresses()

            #If the state is quit or player closes the game
            if self.state == State.QUIT or pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):
                running = False

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

        #Quit the game
        pygame.display.quit()
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()

        #Debug message
        if self.debug:
            print("Closed Game Window")
