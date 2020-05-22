try:
    from .Screens import Screen
    from .Colors import WHITE
    from .Enums import State
except ImportError:
    from Screens import Screen
    from Colors import WHITE
    from Enums import State

class InstructionScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen, debug:bool = False):
        """Screen for displaying the instructions
            Arguments:  
                game_width: Width of the screen in pixels (int)
                game_height: Height of the screen in pixels (int)
                screen: Surface that the screen will be drawn on (pygame.Surface)
                debug: Toggles debug mode (bool)

            Methods:
                handle: Handles the drawing of the instructions screen on the surface
        """

        #Call the superclass
        super().__init__(game_width, game_height, State.INSTRUCTIONS, screen, debug)

        #The first pixel to align
        first_px = self.game_height//2

        #Draw the header
        self.write(Screen.title_font, WHITE, "Instructions", self.game_width//2, first_px - self.game_height//5)

        #Draw the instructions
        self.write(Screen.end_font, WHITE, "Use AD or arrow keys to move", self.game_width//2, first_px)
        self.write(Screen.end_font, WHITE, "Press spacebar to shoot, P to pause", self.game_width//2, first_px + self.game_height//15)
        self.write(Screen.end_font, WHITE, "Press O to unpause", self.game_width//2, first_px + self.game_height//7.5)

        #Draw the back button
        self.back_rect = self.write(Screen.end_font,WHITE, "Back", self.game_width//2, self.game_height-self.game_height//5)

    def handle(self) -> State:
        """Load the Instructions onto the screen
            Arguments:
                No Arguments
            Returns:
                Returns the State the game should be in (State)
        """

        #Update onto the screen
        self.update()

        #Check if the back button is clicked
        if self.check_clicked(self.back_rect):
            return State.MENU

        #Otherwise return the current state
        return self.state