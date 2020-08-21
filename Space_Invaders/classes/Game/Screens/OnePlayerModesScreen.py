from . import MenuTemplate
from .. import State, WHITE


class OnePlayerModeScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """The main screen for 1 player mode"""

        # Store the button rects
        self.buttons = []
        self.modes = (State.STORY_MENU, State.CLASSIC, State.PLAY, State.ONLINE, State.PLAYMODE)

        # Call the superclass
        super().__init__(screen_width, screen_height, State.ONE_PLAYER_MENU, screen, debug)

    def write_lines(self) -> None:
        """Write the lines for one player mode screen"""
        # Single player modes
        self.write(self.title_font, WHITE, "1 Player Modes", self.screen_width // 2, self.screen_height // 5)

        # Draw the screen for the story mode
        self.buttons.append(
            self.write(self.end_font, WHITE, "Story Mode", self.screen_width // 2, self.screen_height // 2))

        # Draw the rectangles for the classic button
        self.buttons.append(self.write(self.end_font, WHITE, "Classic Mode", self.screen_width // 2,
                                       self.screen_height // 15 + self.screen_height // 2))

        # Draw the rectangles for the endless button
        self.buttons.append(self.write(self.end_font, WHITE, "Endless Mode", self.screen_width // 2,
                                       self.screen_height // 7.5 + self.screen_height // 2))

        # Draw the online button
        self.buttons.append(self.write(self.end_font, WHITE, "Online Mode", self.screen_width // 2,
                                       self.screen_height // 5 + self.screen_height // 2))

        # Draw the back button
        self.buttons.append(self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2))

    def get_rects(self) -> tuple:
        """Get the rects for the screen"""
        return self.buttons

    def get_effects(self) -> tuple:
        """Get the effects for the screen"""
        return self.modes
