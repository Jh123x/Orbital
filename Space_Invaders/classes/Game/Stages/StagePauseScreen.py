import pygame
from .. import State, WHITE, PauseScreen

class StagePauseScreen(PauseScreen):

    def __init__(self, screen_width:int, screen_height:int, screen, previous_state: State, debug:bool = False):
        """Constructor for the Stage pause screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, 0, previous_state, debug)
        
        #Set the current state
        self.set_state(State.STAGE_PAUSE)

    def write_lines(self) -> None:
        """Write the lines of the pause screen"""

        #Draw the title of the pause screen
        self.write(self.title_font, WHITE, "Paused", self.screen_width//2, self.screen_height//5)
        
        #Draw the score of the person currently
        self.write(self.subtitle_font, WHITE, f"Stage {self.get_stage()}", self.screen_width//2, self.screen_height//2)

        #Draw the instructions on how to quit/unpause
        self.write(self.end_font, WHITE, f"Click on the button or the shortcut", self.screen_width//2, self.screen_height//2 + self.screen_height // 15)

        #Draw the instructions to unpause
        self.unpause = self.write(self.end_font, WHITE, "Unpause (P)", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

        #Draw the instructions to quit
        self.quit = self.write(self.end_font, WHITE, "Quit (Esc)", self.screen_width//2, self.screen_height//5 + self.screen_height//2)

    def get_stage(self) -> int:
        """Return the current stage of the game"""
        return self.previous_state.value - 99

    def get_stage_name(self) -> str:
        """Return the name of the stage"""
        return f"Stage {self.get_stage()}"