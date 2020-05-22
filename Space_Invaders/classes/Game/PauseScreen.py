import pygame
from pygame.locals import *

try:
    from .Screens import Screen
    from .Enums import State
    from .Colors import WHITE

except ImportError:
    from Screens import Screen
    from Enums import State
    from Colors import WHITE

class PauseScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen:int, score:int, debug:bool = False):
        """Main class for the pause screen"""
        #Call the superclass
        super().__init__(game_width, game_height, State.PAUSE, screen)

        #Draw the title of the pause screen
        self.write(self.title_font, WHITE, "Paused", self.game_width//2, self.game_height//5)
        
        #Draw the score of the person currently
        self.write(self.end_font, WHITE, f"Score: {score}", self.game_width//2, self.game_height//5 + self.game_height//15)

        #Draw the instructions to unpause
        self.write(self.end_font, WHITE, "Press O to unpause", self.game_width//2, self.game_height//15 + self.game_height//2)

        #Draw the instructions to quit
        self.write(self.end_font, WHITE, "Escape to quit, score will not be saved", self.game_width//2, self.game_height//7.5 + self.game_height//2)

    def update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen"""

        #Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        #Return the play state if the player unpause his game
        if keys[K_o]:
            return State.PLAY

        #If the player press the escape key, quit the game
        if keys[K_ESCAPE]:
            return State.MENU
        
        #Return the current state if the player has not unpaused
        return State.PAUSE

    def handle(self) -> State:
        """Handles the drawing of the pause screen"""
        #Update the screen itself
        self.update()

        #Detect the keypress for the unpause button
        return self.update_keypresses()