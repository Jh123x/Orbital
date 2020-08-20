import random

import pygame
from pygame.locals import *

from . import GameoverScreen
from .. import State, WHITE, Direction


class TwoPlayerGameoverScreen(GameoverScreen):
    # Check if the sound is played
    sound = None

    def __init__(self, screen_width: int, screen_height: int, screen, player_scores: tuple, prev_state,
                 debug: bool = False):
        """Constructor for the Two Player Gameover class"""

        # Store extra vars
        self.p1_score = player_scores[0]
        self.p2_score = player_scores[1]

        # Call the superclass
        super().__init__(screen_width, screen_height, screen, player_scores[0], prev_state, debug)

        # Set the state to 2 player gameover
        self.set_state(State.TWO_PLAYER_GAMEOVER)

    def write_scores(self):
        """Write the scores of the players"""
        # Draw the winner
        if self.p1_score > self.p2_score:
            self.write(self.subtitle_font, WHITE, f"Player 1 Wins", self.screen_width // 2,
                       self.screen_height // 2 - 120)
        elif self.p1_score == self.p2_score:
            self.write(self.subtitle_font, WHITE, f"Its a draw", self.screen_width // 2, self.screen_height // 2 - 120)
        else:
            self.write(self.subtitle_font, WHITE, f"Player 2 Wins", self.screen_width // 2,
                       self.screen_height // 2 - 120)

        # Draw the scores of each of the players
        self.write(self.end_font, WHITE, f"Player 1 score: {self.p1_score}", self.screen_width // 4,
                   self.screen_height // 2, Direction.LEFT)
        self.write(self.end_font, WHITE, f"Player 2 score: {self.p2_score}", self.screen_width // 4,
                   self.screen_height // 2 + 45, Direction.LEFT)

    def write_lines(self) -> None:
        """Draw the contents of 2 player gameover"""
        # Draw the scores on the screen
        self.write(self.title_font, WHITE, f"Game over", self.screen_width // 2, self.screen_height // 5)

        # Draw player scores
        self.write_scores()

        # Draw the fixed buttons
        first_px = self.screen_height // 2
        self.try_again = self.write(self.end_font, WHITE, "Try Again (T)", self.screen_width // 2,
                                    first_px + self.screen_height // 7.5)
        self.menu = self.write(self.end_font, WHITE, "Back to Menu (Y)", self.screen_width // 2,
                               first_px + self.screen_height // 5)
        self.quit = self.write(self.end_font, WHITE, "Quit (N)", self.screen_width // 2, self.screen_height // 1.2)

    def get_scores(self) -> tuple:
        """Return the scores of the players"""
        return self.p1_score, self.p2_score

    def comparator(self) -> tuple:
        """The comparator for 2 player gameover"""
        return self.get_scores()
