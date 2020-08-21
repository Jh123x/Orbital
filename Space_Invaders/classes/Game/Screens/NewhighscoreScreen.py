import pygame
from pygame.locals import *

from . import Screen
from .. import InputBox, State, WHITE


class NewhighscoreScreen(Screen):
    # Input box for the player to key in his name
    inputbox = InputBox(300, 400, 30, Screen.end_font)

    def __init__(self, screen_width: int, screen_height: int, screen, score: int, debug: bool = False):
        """Main screen for the new highscore screen"""

        # Call the superclass
        super().__init__(screen_width, screen_height, State.NEWHIGHSCORE, screen, 0, 0, debug)

        # Define new variables
        self.score = score

        # Start pixel to start drawing
        start_px = 100

        # Tell the user he has a new high score
        self.write(self.title_font, WHITE, f"New High Score", self.screen_width // 2, start_px)

        # Write the score the user got
        self.write(self.end_font, WHITE, f"Score: {self.score}", self.screen_width // 2,
                   start_px + self.screen_height // 10)

        # Tell the user to key in his name
        self.write(self.font, WHITE, f"Please enter your name and press enter", self.screen_width // 2,
                   start_px + self.screen_height // 5)

        # Draw the sprites
        self.draw()

    def get_score(self) -> int:
        """Get the score of the player"""
        return self.score

    @staticmethod
    def get_name() -> str:
        """Get the name of that was keyed into the inputbox"""
        return NewhighscoreScreen.inputbox.get_text()

    def draw(self) -> None:
        """Draw the Screen onto the Surface"""

        # Draw the inputbox
        NewhighscoreScreen.inputbox.blit(self.screen)

    def handle(self) -> State:
        """Handles the new highscore and get user's name from input"""

        # Check each keydown event in pygame event queue
        for event in tuple(filter(lambda x: x.type == pygame.KEYDOWN, pygame.event.get())):

            # Check if it is the backspace key
            if event.key == K_BACKSPACE:

                # Do backspace on the inputbox
                NewhighscoreScreen.inputbox.backspace()

            # Check if the player hit any other key
            elif event.key != K_RETURN:

                # Add the character to the inputbox
                NewhighscoreScreen.inputbox.add(event.unicode)

            # If the player hit the return key
            else:

                # Return Gameover State
                return State.GAMEOVER

        # Update the Inputbox
        NewhighscoreScreen.inputbox.update()

        # Draw the sprites
        self.draw()

        # Update the surface
        self.update()

        # Check if the player wants to pause or quit
        if self.check_quit():
            return State.QUIT

        # Return the Current game state
        return State.NEWHIGHSCORE
