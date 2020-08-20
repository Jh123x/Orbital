# Play mode screen
import pygame
from pygame.locals import *

from . import MenuTemplate
from .. import State, WHITE


class PlayModeScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """Main screen for the different play modes"""

        # Call the super class
        super().__init__(screen_width, screen_height, State.PLAYMODE, screen, debug)

    def write_lines(self) -> None:
        """Write the lines for the Play Mode screen"""
        # First pixel for alignment
        first_pixel = self.screen_height // 2

        # Draw the Header
        self.header = self.write(self.title_font, WHITE, "Modes", self.screen_width // 2, self.screen_height // 5)

        # Draw the rectangles for the different game modes
        # Rect for tutorial
        self.tutorial = self.write(self.end_font, WHITE, "Tutorial", self.screen_width // 2,
                                   first_pixel + self.screen_height // 5)

        # Rect for AI modes
        self.ai_modes = self.write(self.end_font, WHITE, "AI Modes", self.screen_width // 2,
                                   first_pixel + self.screen_height // 7.5)

        # Rect for the single player mode
        self.one_player = self.write(self.end_font, WHITE, "1 Player Modes", self.screen_width // 2, first_pixel)

        # 2 Player mode (2 player mode menu)
        self.two_player = self.write(self.end_font, WHITE, "2 Player Modes", self.screen_width // 2,
                                     first_pixel + self.screen_height // 15)

        # Back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

    def get_rects(self):
        # Store all the buttons
        return (self.one_player, self.two_player, self.ai_modes, self.tutorial, self.back)

    def get_effects(self):
        # Get the desired output states
        return (State.ONE_PLAYER_MENU, State.TWO_PLAYER_MENU, State.AI_MENU, State.TUTORIAL, State.MENU)
