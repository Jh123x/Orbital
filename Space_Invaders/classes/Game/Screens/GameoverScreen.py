import pygame
from pygame.locals import *

from . import MenuTemplate
from .. import State, WHITE


class GameoverScreen(MenuTemplate):
    sound = None

    def __init__(self, screen_width: int, screen_height: int, screen, score: int, prev_state: State,
                 debug: bool = False):
        """Constructor for the gameover screen for 1 player modes"""

        # Set the sound played to False
        self.played = False

        # Store the variables
        self.score = score

        # Store the previous state
        self.prev = prev_state

        # Call the superclass method
        super().__init__(screen_width, screen_height, State.GAMEOVER, screen, debug)

    def write_lines(self) -> None:
        """Write lines of the gameover screen"""

        # Draw the words for gameover
        self.write(self.title_font, WHITE, "Game Over", self.screen_width // 2, self.screen_height // 5)

        # Draw the score
        self.write_score()

        # Prompt player to update
        first_px = self.screen_height // 2
        self.try_again = self.write(self.end_font, WHITE, "Try Again (T)", self.screen_width // 2,
                                    first_px + self.screen_height // 7.5)
        self.menu = self.write(self.end_font, WHITE, "Back to Menu (Y)", self.screen_width // 2,
                               first_px + self.screen_height // 5)
        self.quit = self.write(self.end_font, WHITE, "Quit (N)", self.screen_width // 2, self.screen_height // 1.2)

    def get_prev_state(self):
        """Return the previous state before the gameover"""
        return self.prev

    def write_score(self):
        """Draw the score"""
        # Draw the score
        self.write(self.end_font, WHITE, "Total Score : " + str(self.score), self.screen_width // 2,
                   self.screen_height // 2)

    def get_score(self):
        """Return the score of the player"""
        return self.score

    def comparator(self):
        """The comparator for the gameover screen"""
        return self.get_score()

    def get_rects(self) -> tuple:
        """Get the rects for the gameover screen"""
        return (self.try_again, self.menu, self.quit)

    def get_effects(self) -> tuple:
        """Get the effects for the gameover screen"""
        return (self.get_prev_state(), State.MENU, State.QUIT)

    def update_keypresses(self) -> State:
        """Check if player wants to stay"""

        # Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        # Check for y key to indicate he wants to go back to menu
        if keys[K_y]:
            return State.MENU

        # Check for n key to indicate that the player wants to leave
        elif keys[K_n]:
            return State.QUIT

        # Check if the t key is pressed
        elif keys[K_t]:

            # Return the previous state for the player to try again
            return self.get_prev_state()

        # Otherwise return None for it to be asked in the next iteration
        else:
            return super().update_keypresses()

    def handle(self) -> State:
        """Handles drawing of the gameover screen"""

        # If sound exist and have not been played
        if not self.played and self.sound:
            # Play the sound
            self.sound.play('gameover')

            # Set sound played to true
            self.played = True

        # Call the superclass handle method
        return super().handle()
