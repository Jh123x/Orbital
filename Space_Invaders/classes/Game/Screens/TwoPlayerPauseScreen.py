import pygame
from pygame.locals import *
from . import Screen
from .. import WHITE, State, Direction

class TwoPlayerPauseScreen(Screen):

    #Check if the paused sound is played
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
        self.cooldown = 20

        #Draw the header
        self.write(self.title_font, WHITE, "Paused", screen_width//2, screen_height//5)

        #First pixel used for alignment
        first_pixel = screen_height // 2

        #Draw the player 1 score
        self.write(self.end_font, WHITE, f"Player 1: {p1_score}", screen_width//4, first_pixel, Direction.LEFT)

        #Draw the player 2 score
        self.write(self.end_font, WHITE, f"Player 2: {p2_score}", screen_width//4, first_pixel + self.screen_height//15, Direction.LEFT)

        #Draw the instructions to unpause
        self.unpause = self.write(self.end_font, WHITE, "Unpause (P)", self.screen_width//4, first_pixel + self.screen_height//7.5, Direction.LEFT)

        #Draw the instructions to quit
        self.quit = self.write(self.end_font, WHITE, "Quit (Esc)", self.screen_width//4, first_pixel + self.screen_height//5, Direction.LEFT)

    def get_scores(self) -> tuple:
        """Return the score of the 2 players"""
        return self.p1,self.p2

    def update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen"""

        #Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        #If the button is still under cooldown
        if not self.cooldown:

            #Return the play state if the player unpause his game
            if keys[K_p]:
                TwoPlayerPauseScreen.played = False
                self.cooldown = 20
                return self.prev

            #If the player press the escape key, quit the game
            if keys[K_ESCAPE]:
                TwoPlayerPauseScreen.played = False
                self.cooldown = 20
                return State.MENU
        
        #Return the current state if the player has not unpaused
        return self.state

    def check_clicks(self):
        """Check the clicks done by the player"""

        #If the player clicked on the quit button
        if self.check_clicked(self.quit):
            TwoPlayerPauseScreen.played = False

            #Set a cooldown
            self.cooldown = 20

            #Return previous state
            return State.MENU
            
        #If the player clicked on the unpause button
        elif self.check_clicked(self.unpause):
            TwoPlayerPauseScreen.played = False

            #Set a cooldown
            self.cooldown = 20

            #Return previous state
            return self.prev

        #Otherwise
        else:
            return None

    def handle(self) -> State:
        """Handles the drawing of the 2 player pause screen"""
        #Update the screen itself
        self.update()

        if self.cooldown:
            self.cooldown -= 1

        #Detect the keypress
        state = self.check_clicks()
        return self.update_keypresses() if not state else state