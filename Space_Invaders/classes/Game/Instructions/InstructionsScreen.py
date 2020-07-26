from .. import Sound, WHITE, State, Screen

class InstructionScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Screen for displaying the instructions"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.INSTRUCTIONS, screen, 0, 0, debug)

        #The first pixel to align
        first_px = self.screen_height//2 - 100

        #Draw the header
        self.write(Screen.title_font, WHITE, "Instructions", self.screen_width//2, first_px - self.screen_height//7)

        #Draw the instructionsw
        self.write(Screen.end_font, WHITE, "Use AD or arrow keys to move", self.screen_width//2, first_px)
        self.write(Screen.end_font, WHITE, "Press spacebar to shoot", self.screen_width//2, first_px + self.screen_height//15)
        self.write(Screen.end_font, WHITE, "Press P to pause and unpause", self.screen_width//2, first_px + self.screen_height//7.5)
        self.write(Screen.end_font, WHITE, "Press X to screenshot anytime", self.screen_width//2, first_px + self.screen_height//5)

        #Draw the back button
        self.back_rect = self.write(Screen.end_font,WHITE, "Back", self.screen_width//2, self.screen_height//1.2)

    def handle(self) -> State:
        """Load the Instructions onto the screen"""

        #Update onto the screen
        self.update()

        #Check if the back button is clicked
        if self.check_clicked(self.back_rect):

            #Go back to the instructions menu
            return State.INSTRUCTIONS_MENU

        #Otherwise return the current state
        return self.state