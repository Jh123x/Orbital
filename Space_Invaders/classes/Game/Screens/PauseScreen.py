import pygame
from pygame.locals import *

from . import MenuTemplate
from .. import State, WHITE


class PauseScreen(MenuTemplate):
    # Check if the pause sound has been played
    sound = None

    def __init__(self, screen_width: int, screen_height: int, screen, score: int, previous_state: State,
                 debug: bool = False):
        """Main class for the pause screen"""

        # Store the score
        self.p1_score = score

        # Store the previous state
        self.previous_state = previous_state

        # Call the superclass
        super().__init__(screen_width, screen_height, State.PAUSE, screen, debug)

        # Set sound played to false
        self.played = False

        # Set a cd
        self.cd = 20

        # Write the lines
        self.write_lines()

    def write_lines(self):
        """Write the lines required for Pause screen"""
        # Draw the title of the pause screen
        self.write(self.title_font, WHITE, "Paused", self.screen_width // 2, self.screen_height // 5)

        # Draw the score of the person currently
        self.write(self.subtitle_font, WHITE, f"Score: {self.p1_score}", self.screen_width // 2,
                   self.screen_height // 2)

        # Draw the instructions on how to quit/unpause
        self.write(self.end_font, WHITE, f"Click on the button or the shortcut", self.screen_width // 2,
                   self.screen_height // 2 + self.screen_height // 15)

        # Draw the instructions to unpause
        self.unpause = self.write(self.end_font, WHITE, "Unpause (P)", self.screen_width // 2,
                                  self.screen_height // 7.5 + self.screen_height // 2)

        # Draw the instructions to quit
        self.quit = self.write(self.end_font, WHITE, "Quit (Esc)", self.screen_width // 2,
                               self.screen_height // 5 + self.screen_height // 2)

    def get_score(self) -> int:
        """Get the score displayed for the pause screen"""
        return self.p1_score

    def comparator(self) -> int:
        """Comparison function"""
        return self.get_score()

    def get_rects(self):
        return (self.quit, self.unpause)

    def get_effects(self):
        return (State.MENU, self.previous_state)

    def update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen"""

        # Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        # If the button is still under cooldown
        if not self.cd:

            # Return the play state if the player unpause his game
            if keys[K_p]:
                self.played = False
                self.cd = 20
                return self.previous_state

            # If the player press the escape key, quit the game
            if keys[K_ESCAPE]:
                self.played = False
                self.cd = 20
                return State.MENU

        # Return the current state if the player has not unpaused
        return super().update_keypresses()

    def handle(self) -> State:
        """Handles the drawing of the pause screen"""

        # If there is a pausescreen sound and it has not played
        if not self.played and self.sound:
            # Play the pause screen sound
            self.sound.play('pause')
            self.played = True

        # If the cooldown is still there
        if self.cd:
            self.cd -= 1

        # Call the superclass handle
        return super().handle()
