import pygame
from pygame.locals import *

from . import MenuTemplate
from .. import State, WHITE, ImageObject, Direction


class MenuScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """Constructor for the Main Menu screen"""

        # Call the superclass
        super().__init__(screen_width, screen_height, State.MENU, screen, debug)

    def write_lines(self) -> None:
        """Write lines for the menu"""

        # Draw the title
        self.write(self.title_font, WHITE, "Space Invaders", self.screen_width // 2, self.screen_height // 5)

        # Draw the Play button
        self.rect_play = self.write(self.end_font, WHITE, "Play", self.screen_width // 2, self.screen_height // 2)

        #Draw the highscore button
        self.stats = self.write(self.end_font, WHITE, "Statistics", self.screen_width//2, self.screen_height//15 + self.screen_height//2)

        #Draw the instructions button
        self.rect_instruction = self.write(self.end_font, WHITE, "Game Info", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

        # Draw the settings button
        self.rect_settings = self.write(self.end_font, WHITE, "Settings", self.screen_width // 2,
                                        self.screen_height // 5 + self.screen_height // 2)

        #Draw the quit button
        self.rect_end = self.write(self.end_font, WHITE, "Quit", self.screen_width//2, self.screen_height//1.2)

        #Get the dimensions of the credits
        text = "Created by Stephen and Junhua"
        _, text_height = self.font.size(text)

        #Draw the credits
        self.write(self.font, WHITE, text, 0, self.screen_height - text_height, direction = Direction.LEFT)

    def get_rects(self):
        """Get the rects for the Menu Screen"""
        return (self.rect_play, self.stats, self.rect_instruction, self.rect_settings, self.rect_end)

    def get_effects(self):
        """Get the effects for Menu Screen"""
        return (State.PLAYMODE, State.STAT_MENU_SCREEN, State.INSTRUCTIONS_MENU, State.SETTINGS, State.QUIT)

