# Play mode screen
import pygame
from pygame.locals import *

from .. import State, WHITE, MenuTemplate


class AIMenuScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """Main screen for the different play modes"""

        # Draw the rects
        self.rects = []

        # Call the super class
        super().__init__(screen_width, screen_height, State.AI_MENU, screen, debug)

        # Initialise the popup
        self.popup = None

    def write_lines(self):
        """Write the screens for the AI menu"""

        # Draw the first pixel
        first_pixel = self.screen_height // 2

        # Draw the header
        self.write(self.title_font, WHITE, "AI Modes", self.screen_width // 2, self.screen_height // 5)

        # Draw the coop with AI mode
        self.rects.append(self.write(self.end_font, WHITE, "Coop with AI", self.screen_width // 2, first_pixel))

        # Draw the ai versus mode
        self.rects.append(self.write(self.end_font, WHITE, "Versus AI", self.screen_width // 2,
                                     first_pixel + self.screen_height // 15))

        # Draw the back button
        self.rects.append(self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2))

    def get_rects(self) -> tuple:
        """Get the rectangles"""
        return self.rects

    def get_effects(self) -> tuple:
        """Get the effects"""
        return (State.AI_COOP, State.AI_VS, State.PLAYMODE)

    def handle(self) -> State:
        """Handle the drawing of the 2 players screen"""

        # If there is a popup
        if self.popup:
            # Update the popup
            self.popup.update()

        # Call the superclass handle
        return super().handle()
