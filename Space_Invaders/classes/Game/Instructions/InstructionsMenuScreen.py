from .. import State, WHITE, MenuTemplate


class InstructionsMenuScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """Main Instructions menu screen"""

        # A list to store the rects
        self.rects = []

        # Initialise the effects
        self.effects = (
        State.INSTRUCTIONS, State.PVP_INSTRUCTIONS, State.POWERUP_INSTRUCTIONS, State.MOBS_INSTRUCTIONS, State.MENU)

        # Call the superclass
        super().__init__(screen_width, screen_height, State.INSTRUCTIONS_MENU, screen, debug)

    def write_lines(self) -> None:
        """Write the lines for the instruction menus"""
        # Draw the header
        self.header = self.write(self.title_font, WHITE, "Instructions", self.screen_width // 2,
                                 self.screen_height // 5)

        # For alignment
        first_px = self.screen_height // 2

        # Draw the endless mode button
        self.rects.append(self.write(self.end_font, WHITE, "Single Player Modes", self.screen_width // 2, first_px))

        # Draw the PVP mode Instructions
        self.rects.append(self.write(self.end_font, WHITE, "2 Player Modes", self.screen_width // 2,
                                     first_px + self.screen_height // 15))

        # Draw the Powerup instructions
        self.rects.append(
            self.write(self.end_font, WHITE, "Powerups", self.screen_width // 2, first_px + self.screen_height // 7.5))

        # Draw the sprites instructions
        self.rects.append(
            self.write(self.end_font, WHITE, "Enemies", self.screen_width // 2, first_px + self.screen_height // 5))

        # Draw the back button
        self.rects.append(self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2))

    def get_rects(self) -> tuple:
        """Get the rects on the screen"""
        return tuple(self.rects)

    def get_effects(self) -> tuple:
        """Get the effect on the screen"""
        return self.effects
