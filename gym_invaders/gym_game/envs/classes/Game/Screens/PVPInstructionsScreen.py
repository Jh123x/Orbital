from . import Screen
from .. import WHITE, State

class PVPInstructionsScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Main Class for PVP instructions screen"""

        #Calls the superclass
        super().__init__(screen_width, screen_height, State.PVP_INSTRUCTIONS, screen, 0, 0, debug)

        #Draw the header
        self.header = self.write(Screen.title_font, WHITE, "PVP Instructions", self.screen_width//2, self.screen_height//5)        

        #For alignment
        first_px = self.screen_height//2 - 30

        #Draw the instructions
        self.write(Screen.end_font, WHITE, "Player 1: ", screen_width//2, first_px)
        self.write(Screen.end_font, WHITE, "AD to move Space to shoot", screen_width//2, first_px + self.screen_height // 15)
        self.write(Screen.end_font, WHITE, "Player 2:", screen_width//2, first_px + self.screen_height // 7.5)
        self.write(Screen.end_font, WHITE, "Arrowkeys to move 0 to shoot", screen_width//2, first_px + self.screen_height//5)
        self.write(Screen.end_font, WHITE, "P to pause and unpause", screen_width//2, first_px + self.screen_height//5 + self.screen_height // 15)
        
        #Draw the back button
        self.back = self.write(Screen.end_font, WHITE, "Back", screen_width//2, screen_height//1.2)

    def check_keypresses(self) -> State:
        """Check the keypresses on the PVP instructions screen"""
        #If the player clicks on back
        if self.check_clicked(self.back):
            return State.INSTRUCTIONS_MENU

        #Otherwise return current state
        return State.PVP_INSTRUCTIONS

    def handle(self) -> State:
        """Handle the drawing of the PVP instructions screen"""

        #Update the screen
        self.update()

        #Check for keypresses
        return self.check_keypresses()