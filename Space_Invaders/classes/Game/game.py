#!/usr/bin/env python
import pygame
import datetime
import asyncio
from pygame.locals import *
from . import *

#Initialise pygame
pygame.init()

#Initialise the font
pygame.font.init()

#Initialise the sound
pygame.mixer.init()


def load_sprites(obj_list:list, paths:list):
    """Load the sprites for each of the items in parallel"""

    #Run functions concurrently
    for i, obj in enumerate(obj_list):

        #Add image sprites to each class concurrently
        asyncio.run(add_to_sprite(obj, paths[i]))

async def add_to_sprite(obj, sprite_path:str) -> None:
    """Add the pygame image to the object"""
    #For each object load the image and append it to the object
    for path in sprite_path:
        print(path)
        obj.sprites.append(pygame.image.load(path))
        
async def load_sound(sound_path:str, settings:int, volume:float, debug:bool) -> Sound:
    """Load the sound object"""
    return Sound(dict(map(lambda x: (x[0], pygame.mixer.Sound(x[1])), sound_path.items())), bool(int(settings)), volume, debug)

class GameWindow(object):
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int, icon_img_path:str, player_img_paths:tuple,
                 enemy_img_paths:tuple, bullet_img_paths:tuple, background_img_paths:tuple, explosion_img_paths:tuple, 
                 db_path:str, sound_path:dict, bg_limit:int, menu_music_paths:tuple, powerup_img_path:tuple, mothership_img_path:tuple, 
                 trophy_img_path:tuple, scout_img_path:tuple, brute_img_path:tuple, screenshot_path:str, story_img_path:str, wave:int = 1,  debug:bool = False):
        """The Main window for the Space defenders game"""
        
        #Load sprites
        load_sprites((Player, Bullet, EnemyShip, Background, Explosion, PowerUp, MotherShip, VictoryScreen, Scout, Brute, StoryTemplate), 
                    (player_img_paths, bullet_img_paths, enemy_img_paths, background_img_paths, explosion_img_paths, powerup_img_path, mothership_img_path, trophy_img_path, scout_img_path, brute_img_path, story_img_path))

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
        self.score = 0
        self.fps = maxfps
        self.sensitivity = sensitivity
        self.game_width = game_width
        self.game_height = game_height

        #Starting State
        self.state = State.MENU

        #Check if highscore is written
        self.written = False

        #Load the highscores
        self.score_board = ScoreBoard(db_path)

        #Set difficulty
        difficulty = int(self.settings_data['difficulty'])
        self.difficulty = Difficulty(difficulty if difficulty < 5 else 5)

        #Load the sounds into the game
        pygame.mixer.music.load(menu_music_paths[0])

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
        self.ai_vs = AIPVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3, debug)
        self.online = OnlinePVPScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, 3,  debug)
        self.one_player_menu = OnePlayerModeScreen(game_width, game_height, self.main_screen, debug)
        self.tutorial = TutorialScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug)
        self.story_mode = StoryModeScreen(game_width, game_height, self.main_screen, debug)
        self.ai_coop = AICoopScreen(game_width, game_height, self.main_screen, sensitivity, maxfps, self.difficulty, 3, debug)
        self.stage1 = Stage1Screen(game_width, game_height, self.main_screen, sensitivity, maxfps, debug)
        self.victory = None
        self.newhighscore = None
        self.pause = None
        self.pvp_gameover = None
        self.game_over = None

        #Sort the highscore
        self.highscore.sort_scores()

        #Store the variables
        self.popup = None
        self.prev = State.NONE
        self.cooldown = self.fps/5

        #Store the different screens in state
        self.screens = {
            State.MENU:self.menu,
            State.PLAYMODE:self.play_menu,
            State.PLAY:self.play,
            State.HIGHSCORE:self.highscore,
            State.INSTRUCTIONS_MENU: self.inst_menu,
            State.INSTRUCTIONS:self.instructions,
            State.PVP_INSTRUCTIONS: self.pvp_menu,
            State.TWO_PLAYER_MENU: self.two_player,
            State.AI_COOP: self.ai_coop,
            State.AI_VS: self.ai_vs,
            State.PVP: self.pvp,
            State.CLASSIC: self.classic,
            State.SETTINGS: self.settings,
            State.COOP: self.coop,
            # State.ONLINE: self.online,
            State.TUTORIAL: self.tutorial,
            State.ONE_PLAYER_MENU: self.one_player_menu,
            State.STORY_MENU: self.story_mode,
            State.STAGE1:self.stage1
        }
        
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
            State.AI_COOP: self.ai_coop.handle,
            State.AI_VS: self.ai_vs.handle,
            State.PVP: self.pvp.handle,
            State.TWO_PLAYER_GAMEOVER:self.handle_two_player_gameover,
            State.TWO_PLAYER_PAUSE: self.handle_two_player_pause,
            State.CLASSIC: self.classic.handle,
            State.SETTINGS: self.settings.handle,
            State.COOP: self.coop.handle,
            State.ONLINE: self.handle_online,
            State.QUIT:self.__del__,
            State.TUTORIAL: self.tutorial.handle,
            State.ONE_PLAYER_MENU: self.one_player_menu.handle,
            State.VICTORY: self.handle_victory,
            State.STORY_MENU: self.story_mode.handle,
            State.STAGE1: self.stage1.handle
        }

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

        #Add pause sound
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

        #Reset the cleared stage
        stage.reset()

        #If there is no victory screen or it is a different victory screen
        if not self.victory or self.victory.get_stage_name() != cleared_stage:
            self.victory = VictoryScreen(self.game_width, self.game_height, self.main_screen, cleared_stage, self.sound)

        #Handle the victory screen
        return self.victory.handle()
            
    
    def handle_online(self) -> State:
        """Handle the online game"""
        self.popup = Popup(320, 40, "Under Construction", self.fps, self.game_width//2 - 80, self.game_height//2, self.main_screen,font = Screen.end_font, debug = self.debug)
        return State.PLAYMODE
        # return self.online.handle()

    def handle_two_player_pause(self) -> State:
        """Handle the PVP pause screen"""

        #Check based on previous state
        prev_screen = self.screens[self.prev]
        scores = self.screens[self.prev].get_scores()

        #Create the pause screen
        self.two_player_pause = TwoPlayerPauseScreen(self.game_width, self.game_height, self.main_screen, *scores, self.prev, self.debug)

        #Return the function
        state = self.two_player_pause.handle()

        #If new state is menu state
        if state == State.MENU:

            #Reset the state
            prev_screen.reset()

            #Return menu state
            return state

        #If it goes back to the game
        elif state != State.TWO_PLAYER_PAUSE:

            #Return previous state
            return self.prev

        #Otherwise return the state
        return state

    def handle_newhighscore(self) -> State:
        """Handle the displaying of the highscore screen"""

        if not self.newhighscore or self.newhighscore.get_score() != self.play.get_score():
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
        """Handle the displaying of the pause screen"""

        #Get the correct score from the correct state
        score = self.screens[self.prev].get_score()

        #Create the pause screen if it is not already created
        if not self.pause or self.pause.get_score() != score:
            self.pause = PauseScreen(self.game_width,self.game_height, self.main_screen, score, self.prev, self.debug)

        #Handle the pause screen
        state = self.pause.handle()

        #If it is exiting out of the pause state
        if state != State.PAUSE and state != self.prev:
            
            #Reset the screen
            self.screens[self.prev].reset()

        #Return the next state
        return state

    def handle_two_player_gameover(self) -> State:
        """Handle the PVP gameover screen"""

        #Set variables based on previous state
        prev_screen = self.screens[self.prev]
        scores = prev_screen.get_scores()

        #Generate gameover screen if it is not found
        if not self.pvp_gameover or self.pvp_gameover.get_scores() != scores:
            self.pvp_gameover = TwoPlayerGameoverScreen(self.game_width, self.game_height, self.main_screen, *scores)

        #Get next state
        state = self.pvp_gameover.handle()

        #If the gameover screen is over
        if state != State.TWO_PLAYER_GAMEOVER:

            #Reset the environment
            prev_screen.reset()

        #Return the state
        return state
        
    def handle_gameover(self) -> State:
        """Handle the displaying of the gameover screen"""

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
        else:
            
            #Get the score of the previous screen
            score = self.screens[self.prev].get_score()

            #Create the gameover screen
            if not self.game_over or self.game_over.get_score() != score:
                self.game_over = GameoverScreen(self.game_width,self.game_height, self.main_screen, score, self.debug)

            #Check the state given by gameover
            state = self.game_over.handle()

            #If player is going back
            if state == State.MENU:

                #Mark written as false
                self.written = False

                #Reset the play screen
                self.screens[self.prev].reset()

        #Return the state
        return state

    def get_state(self) -> State:
        """Return the state the game is in"""
        return self.state

    async def screenshot(self) -> None:
        """Take a screenshot
            Runs in parallel to the game to reduce lag while screenshotting in game
        """
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

    def update(self) -> None:
        """Update the main screen"""

        #Set the background
        self.fill_background()

        #Check if background music should be playing
        if self.sound.get_state() != self.sound_state:

            #Get the state of sound
            self.sound_state = self.sound.get_state()

            #If sound is enabled
            if self.sound_state:

                #Play the music
                pygame.mixer.music.play(-1)

            #Otherwise
            else:

                #Pause the music
                pygame.mixer.music.pause()

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

    def post_process(self):
        """Do the post processing"""

        #Get the screen it is using
        screen = self.screens.get(self.state, None)

        #Do post process for the screen
        if screen:

            #Call the post process method
            screen.post_process()

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

        #Close the score board
        self.score_board.__del__()

        #Get the settings that was saved and save it to the Database
        self.settingsdb.update('volume',str(self.settings.get_volume()))
        self.settingsdb.update('background',str(self.settings.get_bg_no()))
        self.settingsdb.update('music',int(self.settings.get_music_enabled()))
        self.settingsdb.update('difficulty', int(self.settings.get_difficulty_no()))

        #Close the settingsdb
        self.settingsdb.__del__()

        #Quit the game
        pygame.display.quit()
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()

        #Debug message
        if self.debug:
            print("Closed Game Window")