from . import MenuTemplate
from .. import State, WHITE

class ResetScreen(MenuTemplate):

    def __init__(self, screen_width: int, screen_height: int, screen, tracker, highscore, debug: bool = False):

        #Call the superclass init
        super().__init__(screen_width, screen_height, State.RESET_SCREEN, screen, debug)

        #Store the tracker
        self.tracker = tracker

        #Store highscores
        self.highscore = highscore

    def write_lines(self) -> None:
        """Write the lines for the settings screen"""

        # Draw the Header
        self.write(self.title_font, WHITE, "Are you sure", self.screen_width // 2, self.screen_height // 5)

        #Write the text
        self.write(self.end_font, WHITE, "This will reset stats", self.screen_width // 2, self.screen_height // 2)
        self.write(self.end_font, WHITE, "and achievements", self.screen_width // 2, self.screen_height // 2 + self.screen_height // 15)

        #Draw the reset button
        self.yes = self.write(self.end_font, WHITE, "Yes", self.screen_width // 2, self.screen_height //1.2 - self.screen_height//15)

        # Draw the back button
        self.no = self.write(self.end_font, WHITE, "No", self.screen_width // 2, self.screen_height // 1.2)

    def reset_stats(self):
        """Reset the statistics"""

        #Reset the stats
        self.tracker.reset()

        #Reset the achievements
        self.tracker.reset_achieved()

        #Reset highscore
        self.highscore.clear()

        #Go back to previous state
        return State.SETTINGS

    def get_rects(self):
        """Return the rects of the rect"""
        return (self.yes, self.no)

    def get_effects(self):
        """Return the effects for the rects"""
        return (self.reset_stats, State.SETTINGS)
