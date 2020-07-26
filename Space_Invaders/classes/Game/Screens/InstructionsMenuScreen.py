from . import Screen
from .. import State, WHITE

class InstructionsMenuScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Main Instructions menu screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.INSTRUCTIONS_MENU, screen, 0, 0, debug)

        #Draw the header
        self.header = self.write(Screen.title_font, WHITE, "Instructions", self.screen_width//2, self.screen_height//5)        

        #For alignment
        first_px = self.screen_height//2

        #Draw the endless mode button
        self.endless_instructions = self.write(Screen.end_font, WHITE, "Single Player Modes", self.screen_width//2, first_px)

        #Draw the PVP mode Instructions
        self.pvp_instructions = self.write(Screen.end_font, WHITE, "2 Player Modes", self.screen_width//2, first_px + self.screen_height//15)

        #Draw the Powerup instructions
        self.powerups = self.write(Screen.end_font, WHITE, "Powerups", self.screen_width//2, first_px + self.screen_height//7.5)

        #Draw the sprites instructions
        self.mobs = self.write(Screen.end_font, WHITE, "Enemies", self.screen_width//2, first_px + self.screen_height//5)

        #Draw the back button
        self.back = self.write(Screen.end_font, WHITE, "Back", screen_width//2, screen_height//1.2)

    def check_keypresses(self) -> State:
        """Check the keypresses on the instructions menu screen"""

        #If the person clicked on the endless instructions
        if self.check_clicked(self.endless_instructions):
            return State.INSTRUCTIONS

        #If the player clicked on the PVP instructions
        elif self.check_clicked(self.pvp_instructions):
            return State.PVP_INSTRUCTIONS

        #If the player clicked the back button
        elif self.check_clicked(self.back):
            return State.MENU

        #If the player clicked on powerups
        elif self.check_clicked(self.powerups):
            return State.POWERUP_INSTRUCTIONS

        #If the player click on mobs
        elif self.check_clicked(self.mobs):
            return State.MOBS_INSTRUCTIONS

        #Otherwise return the current state
        else:
            return self.state

    def handle(self) -> State:
        """Handle the drawing of the menu"""
        
        #Update the screen
        super().update()

        #Check keypresses
        return self.check_keypresses()

