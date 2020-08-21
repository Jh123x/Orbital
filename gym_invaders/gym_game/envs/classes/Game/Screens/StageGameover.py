import pygame
from pygame.locals import *
from . import GameoverScreen
from .. import State, WHITE

class StageGameoverScreen(GameoverScreen):
    sound = None
    played = False

    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """The main class for stage gameovers"""
        #Call the superclass init
        super().__init__(screen_width, screen_height, screen, 0, debug) 

        #Set the current state
        self.set_state(State.STAGE_GAMEOVER)

    def write_score(self):
        """Draw the player lose screen"""
        self.write(self.end_font, WHITE, "Mission failed", self.screen_width // 2, self.screen_height // 2 - self.screen_height//15)
        self.write(self.end_font, WHITE, "We will get them next time", self.screen_width // 2, self.screen_height // 2)
