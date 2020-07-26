import pygame
from pygame.locals import *
from . import Screen, PauseScreen
from .. import State, WHITE


class StagePauseScreen(PauseScreen):

    def __init__(self, screen_width:int, screen_height:int, screen, previous_state: State, debug:bool = False):
        """Constructor for the Stage pause screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, 0, previous_state, debug)
        
        #Set the current state
        self.set_state(State.STAGE_PAUSE)

    def get_stage(self) -> int():
        """Return the current stage of the game"""
        return self.previous_state.value - 99

    def write_lines(self):
        #Draw the title of the pause screen
        self.write(Screen.title_font, WHITE, "Paused", self.screen_width//2, self.screen_height//5)
        
        #Draw the score of the person currently
        self.write(Screen.subtitle_font, WHITE, f"Stage {self.get_stage()}", self.screen_width//2, self.screen_height//2)

        #Draw the instructions to unpause
        self.write(Screen.end_font, WHITE, "Press P to unpause", self.screen_width//2, self.screen_height//15 + self.screen_height//2)

        #Draw the instructions to quit
        self.write(Screen.end_font, WHITE, "Escape to quit, score will not be saved", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)