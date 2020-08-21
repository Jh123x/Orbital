from .. import WHITE, State, MenuTemplate


class PVPInstructionsScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """Main Class for PVP instructions screen"""

        # Calls the superclass
        super().__init__(screen_width, screen_height, State.PVP_INSTRUCTIONS, screen, debug)

    def write_lines(self):
        """Write the lines"""

        # Draw the header
        self.header = self.write(self.title_font, WHITE, "PVP Instructions", self.screen_width // 2,
                                 self.screen_height // 5)

        # For alignment
        first_px = self.screen_height // 2 - 30

        # Draw the instructions
        self.write(self.end_font, WHITE, "Player 1: ", self.screen_width // 2, first_px)
        self.write(self.end_font, WHITE, "AD to move Space to shoot", self.screen_width // 2,
                   first_px + self.screen_height // 15)
        self.write(self.end_font, WHITE, "Player 2:", self.screen_width // 2, first_px + self.screen_height // 7.5)
        self.write(self.end_font, WHITE, "Arrowkeys to move 0 to shoot", self.screen_width // 2,
                   first_px + self.screen_height // 5)
        self.write(self.end_font, WHITE, "P to pause and unpause", self.screen_width // 2,
                   first_px + self.screen_height // 5 + self.screen_height // 15)

        # Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

    def get_rects(self):
        return (self.back,)

    def get_effects(self):
        return (State.INSTRUCTIONS_MENU,)
