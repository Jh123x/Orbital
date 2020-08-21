from . import MenuTemplate
from .. import WHITE, State, Direction


class StoryModeScreen(MenuTemplate):
    videos = []

    def __init__(self, screen_width: int, screen_height: int, screen, debug: bool = False):
        """Constructor for Story mode screen"""

        # Store the current number of stages
        self.stages = 6

        # Create list to store the buttons
        self.video_buttons = []

        # Call the superclass
        super().__init__(screen_width, screen_height, State.STORY_MENU, screen, debug)

    def write_lines(self):
        """Write the lines for the screen"""
        # Draw the title
        self.write(self.title_font, WHITE, "Story modes", self.screen_width / 2, self.screen_height / 5)

        # Put a video for the StoryMode:
        self.create_videos()

        # Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height / 1.2)

    def get_stages(self) -> int:
        """Get the total number of stages in the story mode"""
        return self.stages

    def create_videos(self) -> None:
        """Create videos buttons for the videos"""

        # Iterate through all the stage videos
        for i in range(1, self.get_stages() // 2 + 1):
            # Append the button to the buttons list for checking later
            self.video_buttons.append(self.write(self.end_font, WHITE, f"Stage {i}   ", self.screen_width // 2 - 40,
                                                 self.screen_height // 2 + (40 * i) - 30, Direction.RIGHT))

        for i in range(1, self.get_stages() - self.get_stages() // 2 + 1):
            # Append the button to the buttons list for checking later
            self.video_buttons.append(
                self.write(self.end_font, WHITE, f" Stage {self.get_stages() // 2 + i}", self.screen_width // 2 + 40,
                           self.screen_height // 2 + (40 * i - self.get_stages() // 2 + 1) - 30, Direction.LEFT))

    def get_rects(self):
        """Return the rects"""
        return tuple(self.video_buttons + [self.back])

    def get_effects(self):
        """Return the effects"""
        return tuple([State(100 + i) for i in range(self.stages)] + [State.ONE_PLAYER_MENU])

    def check_mousepress(self) -> State:
        """Check the mouse press of the user"""
        # Check if the user clicked the back button
        if self.check_clicked(self.back):
            # Return menu state
            return State.ONE_PLAYER_MENU

        # Loop through the the video buttons
        for index, rect in enumerate(self.video_buttons):
            if self.check_clicked(rect):
                return State(100 + index)

        # Return the current state
        return self.state
