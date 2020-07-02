from . import Screen
from .. import Sound, WHITE, State

class VictoryScreen(Screen):
    sprites = []
    def __init__(self,screen_width:int, screen_height:int, screen, prev_stage:str, sound:Sound = None, debug:bool = False):
        """The Victory Screen"""

        #Initialise the superclass
        super().__init__(screen_width, screen_height, State.VICTORY, screen, 0, 0, debug)

        #If sound is enabled
        if sound and sound.get_state():

            #Play victory music
            sound.play('victory')

        #Store the stage that is cleared
        self.stage_name = prev_stage

        #Write the main part of the screen
        self.write(Screen.title_font, WHITE, "VICTORY", self.screen_width//2, self.screen_height // 5)

        #Write the stage that was cleared
        self.write(Screen.end_font, WHITE, f"{prev_stage} cleared", self.screen_width//2, self.screen_height // 2)

        #Write the back button
        self.back = self.write(Screen.end_font, WHITE, "back", self.screen_width//2, self.screen_height // 1.2)

    def get_stage_name(self) -> str:
        """Gets the stage name that is currently displayed"""
        return self.stage_name

    def check_keypresses(self) -> State:
        """Check the keypresses"""

        #Check if the user clicked the back button
        if self.check_clicked(self.back):

            #Return menu state
            return State.MENU

        return self.state

    def handle(self) -> State:
        """Handle the victory state"""

        #Call the superclass handle state
        super().update()

        #Check the keypresses
        return self.check_keypresses()




