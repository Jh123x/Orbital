import pygame
from pygame.locals import *
from . import Screen
from .. import WHITE, State, Direction

class TwoPlayerPauseScreen(Screen):
    sound = None
    played = False
    def __init__(self, screen_width:int, screen_height:int, screen, p1_score:int, p2_score:int, prev_state:State, debug:bool = False):
        """Main class for PVP pause screen"""
        
        #Call the superclass
        super().__init__(screen_width, screen_height, State.TWO_PLAYER_PAUSE, screen, 0, 0, debug)

        #Play the pause sound
        if TwoPlayerPauseScreen.sound and not TwoPlayerPauseScreen.played:
            #Play the sound
            TwoPlayerPauseScreen.sound.play('pause')
            TwoPlayerPauseScreen.played = True

        #Store the vars
        self.p1 = p1_score
        self.p2 = p2_score
        self.prev = prev_state

        #Draw the header
        self.write(Screen.title_font, WHITE, "Paused", screen_width//2, screen_height//5)

        #First pixel used for alignment
        first_pixel = screen_height // 2

        #Draw the player 1 score
        self.write(Screen.end_font, WHITE, f"Player 1: {p1_score}", screen_width//4, first_pixel, Direction.LEFT)

        #Draw the player 2 score
        self.write(Screen.end_font, WHITE, f"Player 2: {p2_score}", screen_width//4, first_pixel + self.screen_height//15, Direction.LEFT)

        #Draw the instructions to unpause
        self.write(Screen.end_font, WHITE, "Press O to unpause", self.screen_width//4, first_pixel + self.screen_height//7.5, Direction.LEFT)

        #Draw the instructions to quit
        self.write(Screen.end_font, WHITE, "Escape to quit", self.screen_width//4, first_pixel + self.screen_height//5, Direction.LEFT)
        

    def update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen
            Arguments:
                No arguments:
            Returns: 
                No return
        """
        #Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        #Return the play state if the player unpause his game
        if keys[K_o]:
            TwoPlayerPauseScreen.played = False
            return self.prev

        #If the player press the escape key, quit the game
        elif keys[K_ESCAPE]:
            TwoPlayerPauseScreen.played = False
            return State.MENU
        
        else:
            #Return the current state if the player has not unpaused
            return State.TWO_PLAYER_PAUSE

    def handle(self) -> State:
        """Handle the drawing of the pause screen"""
        #Update the screen
        self.update()

        #Check keypresses
        return self.update_keypresses()