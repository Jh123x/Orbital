from .. import MenuTemplate, WHITE, State


class StatsMenuScreen(MenuTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        # Call the superclass
        super().__init__(screen_width, screen_height, State.STAT_MENU_SCREEN, screen, 0, debug)

    def write_lines(self):
        """Write the lines of the Stats menu screen"""
        # Draw the title
        self.write(self.title_font, WHITE, "Different Stats", self.screen_width // 2, self.screen_height // 5)

        # Draw the Play button
        self.stats = self.write(self.end_font, WHITE, "Statistics", self.screen_width // 2, self.screen_height // 2)

        # Draw the highscore button
        self.achievements = self.write(self.end_font, WHITE, "Achievements", self.screen_width // 2,
                                       self.screen_height // 15 + self.screen_height // 2)

        # Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

    def get_rects(self):
        """Rects on the screen"""
        return (self.stats, self.achievements, self.back)

    def get_effects(self):
        """Effects of the rects"""
        return (State.STAT_MENU, State.ACHIEVEMENTS, State.MENU)
