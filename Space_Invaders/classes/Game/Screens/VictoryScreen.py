from . import MenuTemplate
from .. import Sound, WHITE, State, ImageObject


class VictoryScreen(MenuTemplate):
    # Store the sprites used for the victory screen
    sprites = []

    def __init__(self, screen_width: int, screen_height: int, screen, prev_stage: str, sound: Sound = None,
                 debug: bool = False):
        """The constructor for Victory Screen"""

        # If sound is enabled
        if sound and sound.get_state():
            # Play victory music
            sound.play('victory')

        # Store the stage that is cleared
        self.stage_name = prev_stage

        # Initialise the superclass
        super().__init__(screen_width, screen_height, State.VICTORY, screen, debug)

        # Show the trophy in the middle of the screen
        self.trophy = ImageObject(screen_width // 2, screen_height // 2 - 50, 50, 50, self.sprites[1])
        self.trophy.scale(100, 100)

    def write_lines(self) -> None:
        """Write the lines for the victory screen"""
        # Define central pixel
        first_px = self.screen_height // 2 + 50

        # Write the main part of the screen
        self.write(self.title_font, WHITE, "VICTORY", self.screen_width // 2, self.screen_height // 5)

        # Write the stage that was cleared
        self.write(self.end_font, WHITE, f"{self.stage_name} cleared", self.screen_width // 2, first_px)

        # Write the next stage button
        if self.get_stage_name().lower() != "stage 6" and self.get_stage_name().lower() != 'tutorial':
            self.next_stage = self.write(self.end_font, WHITE, "Next Stage", self.screen_width // 2,
                                         self.screen_height // 1.2 - self.screen_height // 15)
        else:
            self.next_stage = None

        # Write the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

    def get_stage_name(self) -> str:
        """Gets the stage name that is currently displayed"""
        return self.stage_name

    def get_stage(self) -> int:
        """Return the stage number"""
        if self.next_stage:
            return int(self.get_stage_name()[6:])
        else:
            return 0

    def get_rects(self) -> tuple:
        """Get the rects for Victory Screen"""
        if self.next_stage:
            return (self.next_stage, self.back)
        else:
            return (self.back,)

    def get_effects(self) -> tuple:
        """Get the effects of the Victory Screen"""
        if self.next_stage:
            return (State(self.get_stage() + 99), State.MENU)
        else:
            return (State.MENU,)

    def update(self):
        """Victory screen update class"""

        # Call the superclass update
        super().update()

        # Draw trophy on the screen
        self.trophy.draw(self.screen)
