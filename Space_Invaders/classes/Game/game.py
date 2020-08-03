#!/usr/bin/env python
import pygame
import datetime
import asyncio
import os
from pygame.locals import *
from . import *

class GameWindow(object):
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple,
                 enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, explosion_img_paths:tuple, 
                 db_path:str, sound_path:dict, bg_limit:int, menu_music_paths:tuple, powerup_img_path:tuple, mothership_img_path:tuple, 
                 trophy_img_path:tuple, scout_img_path:tuple, brute_img_path:tuple, screenshot_path:str, story_img_path:str, crabs_img_path:str, 
                 place_holder_path:str, pointer_img_path:tuple, wave:int = 1,  debug:bool = False):
        """The Main window for the Space defenders game"""
        
        #Load sprites
        load_sprites((Player, Bullet, EnemyShip, Background, Explosion, MotherShip, VictoryScreen, Scout, Brute, Crabs), 
                    (player_img_paths, bullet_img_paths, enemy_img_paths, background_img_paths, explosion_img_paths, mothership_img_path, trophy_img_path, scout_img_path, brute_img_path, crabs_img_path))

        load_sprites_dict((StoryTemplate, PowerUp, MobInstructionsScreen),
                        (story_img_path, powerup_img_path, place_holder_path))

        #Load the pointers
        load_pointers(pointer_img_path, Screen)

        #Store debug variable
        self.debug = debug

        #Storing the path for screenshots
        self.screenshot_dir = screenshot_path

        #Load setting menu settings
        self.settingsdb = SettingsDB(db_path)
        self.settings_data = dict(map(lambda x: x[1:], self.settingsdb.fetch_all()))

        #Load sounds
        self.sound = asyncio.run(load_sound(sound_path, self.settings_data['music'], float(self.settings_data['volume']), self.debug))

        #Set the title
        pygame.display.set_caption("Space Invaders")

        #Load and set the Icon
        icon = pygame.image.load(icon_img_path)
        pygame.display.set_icon(icon)

        #Set the dimensions
        self.main_screen = pygame.display.set_mode((game_width,game_height), pygame.DOUBLEBUF | pygame.HWSURFACE, 32)

        #Initialise the pygame vars
        self.clock = pygame.time.Clock()
        self.sensitivity = sensitivity
        self.game_height = game_height
        self.game_width = game_width
        self.fps = maxfps

        #Starting State
        self.state = State.MENU

        #Check if highscore is written
        self.written = False

        #Load the highscores
        self.score_board = ScoreBoard(db_path)

        #Set difficulty
        difficulty = int(self.settings_data['difficulty'])
        self.difficulty = Difficulty(difficulty if difficulty < 6 else 6)

        #Load the sounds into the game
        pygame.mixer.music.load(menu_music_paths[0])

        #Create the background object
        self.bg = Background(int(self.settings_data['background']), game_width, game_height, bg_limit, debug)

        #Store the variables
        self.cooldown = self.fps // 5
        self.prev = State.NONE
        self.popup = None

        #Store the different screens in state
        self.screens = {
            State.PLAY:                 PlayScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, 3, debug = self.debug),
            State.CLASSIC:              ClassicScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, debug = self.debug),
            State.SETTINGS:             SettingsScreen(game_width, game_height, self.main_screen, self.fps, self.sound, self.bg, self.difficulty, debug),
            State.HIGHSCORE:            HighscoreScreen(game_width, game_height, self.main_screen, self.score_board.fetch_all(), debug = self.debug),
            State.AI_COOP:              AICoopScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, 3, debug),
            State.COOP:                 CoopScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, 3,  debug),
            State.ONLINE:               OnlinePVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3,  debug),
            State.PVP:                  LocalPVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3,  debug),
            State.POWERUP_INSTRUCTIONS: PowerupInstructionsScreen(game_width, game_height, self.main_screen, self.fps, debug),
            State.AI_VS:                AIPVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3, debug),
            State.TUTORIAL:             TutorialScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.STAGE1:               Stage1Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.STAGE2:               Stage2Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.STAGE3:               Stage3Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.STAGE4:               Stage4Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.STAGE5:               Stage5Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.STAGE6:               Stage6Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug),
            State.MOBS_INSTRUCTIONS:    MobInstructionsScreen(game_width, game_height, self.main_screen, self.fps, debug),
            State.MENU:                 MenuScreen(game_width, game_height, self.main_screen, debug = self.debug),
            State.INSTRUCTIONS_MENU:    InstructionsMenuScreen(game_width, game_height, self.main_screen,  debug),
            State.INSTRUCTIONS:         InstructionScreen(game_width, game_height, self.main_screen, self.debug),
            State.PVP_INSTRUCTIONS:     PVPInstructionsScreen(game_width, game_height, self.main_screen, debug),
            State.TWO_PLAYER_MENU:      TwoPlayerScreen(game_width, game_height, self.main_screen,  self.debug),
            State.ONE_PLAYER_MENU:      OnePlayerModeScreen(game_width, game_height, self.main_screen, debug),
            State.STORY_MENU:           StoryModeScreen(game_width, game_height, self.main_screen, debug),
            State.PLAYMODE:             PlayModeScreen(game_width, game_height, self.main_screen,  debug),
            State.AI_MENU:              AIMenuScreen(game_width, game_height, self.main_screen, debug),
            State.STAGE_GAMEOVER:       None,
            State.STAGE_PAUSE:          None,
            State.VICTORY:              None,
            State.NEWHIGHSCORE:         None,
            State.PAUSE:                None,
            State.TWO_PLAYER_GAMEOVER:  None,
            State.GAMEOVER:             None,
            State.TWO_PLAYER_PAUSE:     None,
        }
        
        #Store the different states the menu has
        self.states = {
            State.TWO_PLAYER_GAMEOVER:  self.handle_two_player_gameover,
            State.TWO_PLAYER_PAUSE:     self.handle_two_player_pause,
            State.STAGE_GAMEOVER:       self.handle_stage_gameover,
            State.NEWHIGHSCORE:         self.handle_newhighscore,
            State.STAGE_PAUSE:          self.handle_stage_pause,
            State.GAMEOVER:             self.handle_gameover,
            State.VICTORY:              self.handle_victory,
            State.ONLINE:               self.handle_online,
            State.PAUSE:                self.handle_pause,
            State.QUIT:                 self.__del__,
        }

        #Sort the highscore
        self.screens[State.HIGHSCORE].sort_scores()

        #Load sound state:
        self.sound_state = self.sound.get_state()
        
        #Initialise the music
        pygame.mixer.music.load(menu_music_paths[0])

        #Play the music if sound is enabled
        if self.sound_state:

            #Loop forever
            pygame.mixer.music.play(-1)

        #Load the sounds into the relavant Sprites
        Bullet.sound = self.sound

        #Add explosion sound
        Explosion.sound = self.sound

        #Add Powerup sound
        PowerUp.sound = self.sound

        #Add pause sounds
        TwoPlayerPauseScreen.sound = self.sound
        PauseScreen.sound = self.sound
        GameoverScreen.sound = self.sound
        TwoPlayerGameoverScreen.sound = self.sound

    def handle_victory(self) -> State:
        """Handle the drawing of the victory screen"""
        #Get the cleared stage
        stage = self.screens[self.prev]

        #Get the name of the stage cleared
        cleared_stage = stage.get_stage_name()

        #If there is no victory screen or it is a different victory screen
        if not self.screens[State.VICTORY] or self.screens[State.VICTORY].get_stage_name() != cleared_stage:

            #Create a new victory screen
            self.screens[State.VICTORY] = VictoryScreen(self.game_width, self.game_height, self.main_screen, cleared_stage, self.sound)

            #Reset the cleared stage
            stage.reset()

        #Handle the victory screen
        return self.screens[State.VICTORY].handle()
    
    def handle_online(self) -> State:
        """Handle the online game"""

        #Currently waiting for a place to host the server
        self.popup = Popup(320, 40, "Under Construction", self.fps, self.game_width//2 - 80, self.game_height//2, self.main_screen,font = Screen.end_font, debug = self.debug)

        #Return playmode for now until server is found
        return State.PLAYMODE

        #Handle the online mode
        # return self.screens[State.ONLINE].handle()

    def _handle_pause(self, pause_state:State, screen_type):
        #Check based on previous state
        prev_screen = self.screens[self.prev]

        #If the screen is not created / different
        if not self.screens[pause_state] or prev_screen.comparator() != self.screens[pause_state].comparator():
            
            #Check based on previous state
            prev_screen = self.screens[self.prev]
            comp = self.screens[self.prev].comparator()

            #Create the pause screen
            self.screens[pause_state] = screen_type(self.game_width, self.game_height, self.main_screen, comp, self.prev, self.debug)

        #Return the function
        state = self.screens[pause_state].handle()

        #If new state is menu state
        if state == State.MENU:

            #Reset the state
            prev_screen.reset()

            #Return menu state
            return state

        #If it goes back to the game
        elif state != pause_state:

            #Return previous state
            return self.prev

        #Otherwise return the state
        return state

    def handle_two_player_pause(self) -> State:
        """Handle the PVP pause screen"""

        #Call the handle pause method
        return self._handle_pause(State.TWO_PLAYER_PAUSE, TwoPlayerPauseScreen)

    def handle_pause(self) -> State:
        """Handle the displaying of the pause screen"""

        #Call the handle pause method
        return self._handle_pause(State.PAUSE, PauseScreen)

    def handle_stage_pause(self) -> State:
        """Handle the pause screen for stages"""

        #Call the handle pause method
        return self._handle_pause(State.STAGE_PAUSE, StagePauseScreen)

    def handle_newhighscore(self) -> State:
        """Handle the displaying of the highscore screen"""

        #If there is a new highscore that is different from before
        if not self.screens[State.NEWHIGHSCORE] or self.screens[State.NEWHIGHSCORE].get_score() != self.screens[State.PLAY].get_score():

            #Create the new highscore screen
            self.screens[State.NEWHIGHSCORE] = NewhighscoreScreen(self.game_width, self.game_height, self.main_screen, self.screens[State.PLAY].get_score())

        #Get the next state
        state = self.screens[State.NEWHIGHSCORE].handle()

        #If the state is gameover
        if state == State.GAMEOVER:
            
            #Debugging information
            if self.debug:
                print(f"Name:{NewhighscoreScreen.get_name()}\nScore:{self.screens[State.PLAY].get_score()}")

            #Update the score of the player
            self.screens[State.HIGHSCORE].update_score(self.screens[State.NEWHIGHSCORE].get_name(), self.screens[State.PLAY].get_score())

            #Clear the input box
            NewhighscoreScreen.inputbox.clear()
            
            #Mark as highscore written
            self.written = True

        #Return the next state
        return state

    def _handle_gameovers(self, gameover_state:State, screen_type) -> State:
        """A General handle for gameover modes"""
            
        #Get the score of the previous screen
        comp = self.screens[self.prev].comparator()

        #Create the gameover screen
        if not self.screens[gameover_state] or self.screens[gameover_state].comparator() != comp or self.screens[gameover_state].get_prev_state() != self.prev:

            #Create a new gameover screen
            self.screens[gameover_state] = screen_type(self.game_width, self.game_height, self.main_screen, comp, self.prev, self.debug)

        #Check the state given by gameover
        state = self.screens[gameover_state].handle()

        #If player is going back
        if state != gameover_state:

            #Reset the play screen
            self.screens[self.prev].reset()

            #Mark written as false
            self.written = False

        #Return the state
        return state

    def handle_two_player_gameover(self) -> State:
        """Handle the PVP gameover screen"""

        #Return the state
        return self._handle_gameovers(State.TWO_PLAYER_GAMEOVER, TwoPlayerGameoverScreen)

    def handle_stage_gameover(self) -> State:
        """Handle the displaying of the gameover screen"""

        #Return the state
        return self._handle_gameovers(State.STAGE_GAMEOVER, StageGameoverScreen)
        
    def handle_gameover(self) -> State:
        """Handle the displaying of the gameover screen"""

        #Check for new highscore
        if self.prev == State.PLAY or self.prev == State.NEWHIGHSCORE:

            #If it is a new highscore
            if self.screens[State.HIGHSCORE].beat_highscore(self.screens[State.PLAY].get_score()) and not self.written:

                #Go to the new highscore state
                return State.NEWHIGHSCORE
            
        #Call the main handle gameover method
        return self._handle_gameovers(State.GAMEOVER, GameoverScreen)

    def get_state(self) -> State:
        """Return the state the game is in"""
        return self.state

    async def screenshot(self) -> None:
        """Take a screenshot
            Runs in parallel to the game to reduce lag while screenshotting in game
        """
        #Check if the screenshot folder is not there
        if not os.path.isdir(self.screenshot_dir):

            #Create the screenshot_dir folder
            os.mkdir(self.screenshot_dir)

        #Save a screenshot named based on date and time
        name = os.path.join(self.screenshot_dir, f'{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.png')

        #Play the screenshot sound
        self.sound.play('screenshot')

        #Print debug message
        if self.debug:
            print(f"Saved at: {name}")
        
        #Save the image
        pygame.image.save(self.main_screen, name)

    def check_keypresses(self) -> None:
        """Check global keypresses within the game"""

        #Get the keys which are pressed
        keys = pygame.key.get_pressed()

        #Check each key individually
        if keys[K_x] and self.state != State.NEWHIGHSCORE:

            #Run the screenshot in parallel
            asyncio.run(self.screenshot())

            #Create a 1 second popup saying screenshot is taken 
            self.popup = Popup(20*8, 30, "Screenshot taken", self.fps, self.game_width//2, 15, self.main_screen, font = Screen.font, debug = self.debug)

    def fill_background(self) -> None:
        """Set the background"""

        #If the background is present
        if self.bg.is_present():

            #Fill it with the background img
            self.bg.update(self.main_screen)
        
        #Otherwise
        else:

            #Fill the background to black
            self.main_screen.fill(BLACK)

    def find_method(self, state) -> State:
        """Find the appropriate method to execute"""

        #Try to find the method in self.states
        handle_method = self.states.get(state, None)

        #If method is found execute it else call the default handle
        return handle_method() if handle_method else self.screens.get(self.state).handle()

    def check_sound(self):
        """Check if bg should be playing"""
        #Check if background music should be playing
        if self.sound.get_state() != self.sound_state:

            #Get the state of sound
            self.sound_state = self.sound.get_state()

            #If sound is enabled
            if self.sound_state:

                #Play the music looped infinitely (-1)
                pygame.mixer.music.play(-1)

            #Otherwise
            else:

                #Pause the music
                pygame.mixer.music.pause()

    def update(self) -> None:
        """Update the main screen"""

        #Set the background
        self.fill_background()

        #Check sound
        self.check_sound()

        #Save previous state
        prev = self.state

        #If on cooldown
        if self.cooldown:

            #Lower cooldown
            self.cooldown -= 1

            #Run the state
            self.find_method(prev)

        #Otherwise
        else:

            #Check if there is new state
            self.state = self.find_method(prev)

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

    def post_process(self):
        """Do the post processing"""

        #Get the screen it is using
        screen = self.screens.get(self.state, None)

        #Do post process for the screen
        if screen:

            #Call the post process method
            screen.post_process()

    def mainloop(self) -> None:
        """The mainloop to load the screen of the game"""

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

            #Check Global keypresses
            self.check_keypresses()

            #Update the display with the screen
            pygame.display.update()

            #Do post processes
            self.post_process()

            #If the state is quit or player closes the game
            if self.state == State.QUIT or pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):

                #Set running to false
                running = False

        #Play the exit sound
        self.sound.play('exit')

    def __del__(self) -> None:
        """Destructor for the game window. Closes all the relavent processes"""

        #Add the new highscores into DB
        self.score_board.add_all(*self.screens[State.HIGHSCORE].get_scores())

        #Remove all entries beyond 5
        self.score_board.remove_all(*self.screens[State.HIGHSCORE].get_removed())

        #Close the score board
        self.score_board.__del__()

        #Get the settings that was saved and save it to the Database
        self.settingsdb.update('difficulty', int(self.screens[State.SETTINGS].get_difficulty_no()))
        self.settingsdb.update('music',int(self.screens[State.SETTINGS].get_music_enabled()))
        self.settingsdb.update('background',str(self.screens[State.SETTINGS].get_bg_no()))
        self.settingsdb.update('volume',str(self.screens[State.SETTINGS].get_volume()))

        #Close the settingsdb
        self.settingsdb.__del__()

        #Quit the game
        pygame.quit()

        #Debug message
        if self.debug:
            print("Closed Game Window")