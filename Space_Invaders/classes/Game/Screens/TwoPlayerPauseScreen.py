import pygame
from pygame.locals import *
from . import PauseScreen
from .. import WHITE, State, Direction

class TwoPlayerPauseScreen(PauseScreen):

    def __init__(self, screen_width:int, screen_height:int, screen, p1_score:int, p2_score:int, previous_state:State, debug:bool = False):
        """Main class for PVP pause screen"""

        #Store the vars
        self.p2_score = p2_score
        
        #Call the superclass
        super().__init__(screen_width, screen_height, screen, p1_score, previous_state, debug)

        #Set state as 2 player pause
        self.set_state(State.TWO_PLAYER_PAUSE)

    def write_lines(self):
        """Write the lines"""
        #Draw the header
        self.write(self.title_font, WHITE, "Paused", self.screen_width//2, self.screen_height//5)

        #First pixel used for alignment
        first_pixel = self.screen_height // 2

        #Draw the player 1 score
        self.write(self.end_font, WHITE, f"Player 1: {self.p1_score}", self.screen_width//4, first_pixel, Direction.LEFT)

        #Draw the player 2 score
        self.write(self.end_font, WHITE, f"Player 2: {self.p2_score}", self.screen_width//4, first_pixel + self.screen_height//15, Direction.LEFT)

        #Draw the instructions to unpause
        self.unpause = self.write(self.end_font, WHITE, "Unpause (P)", self.screen_width//4, first_pixel + self.screen_height//7.5, Direction.LEFT)

        #Draw the instructions to quit
        self.quit = self.write(self.end_font, WHITE, "Quit (Esc)", self.screen_width//4, first_pixel + self.screen_height//5, Direction.LEFT)

    def get_scores(self) -> tuple:
        """Return the score of the 2 players"""
        return self.get_score(),self.p2_score
