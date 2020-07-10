import pygame
import random
from pygame.locals import *
from . import PlayScreen
from .. import BlockGroup, State, Difficulty, MotherShip

class ClassicScreen(PlayScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty:Difficulty, wave:int = 1, player_lives:int = 3,debug:bool = False):
        """Classic screen for the game
            Main class to draw the classic screen for the game
        """
        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, difficulty, wave, player_lives, 0, debug)

        #Change the state to classic
        self.state = State.CLASSIC

    def spawn_scout(self, *args):
        """Overridden spawn scout class"""
        return

    def reset(self) -> None:
        """Reset the classic screen"""
        #Call superclass reset
        super().reset()

        #Reset the 5 blocks
        self.blocks = BlockGroup(self.screen_width, self.screen_height//1.2, self.screen, 5, self.player1.get_height() + 10)