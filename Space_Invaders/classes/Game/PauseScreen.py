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
    def __init__(self, screen_width:int, screen_height:int, screen, score:int, debug:bool = False):
        """Main class for the pause screen
            Arguments:
                screen_width: The width of the game in terms of pixels (int)
                screen_height: The height of the game in terms of pixels (int)
                screen: The Surface that the screen is drawn onto (pygame.Surface)
                score: Score that the player has currently (int)
                debug: Toggles debug mode (bool)

            Methods:
                update_keypresses: Update the state based on keypress of user
                handle: handles the drawing of the pause state
        """
        #Call the superclass
        super().__init__(screen_width, screen_height, State.PAUSE, screen, 0, 0, debug)

        #Draw the title of the pause screen
        self.write(self.title_font, WHITE, "Paused", self.screen_width//2, self.screen_height//5)
        
        #Draw the score of the person currently
        self.write(self.end_font, WHITE, f"Score: {score}", self.screen_width//2, self.screen_height//5 + self.screen_height//15)

        #Draw the instructions to unpause
        self.write(self.end_font, WHITE, "Press O to unpause", self.screen_width//2, self.screen_height//15 + self.screen_height//2)

        #Draw the instructions to quit
        self.write(self.end_font, WHITE, "Escape to quit, score will not be saved", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

    def update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen
            Arguments:
                No arguments:
            Returns: 
                No return
        """

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
        """Handles the drawing of the pause screen
            Arguments:
                No arguments:
            Returns: 
                Returns the next state the game is suppose to be in
        """
        #Update the screen itself
        self.update()

        #Detect the keypress for the unpause button
        return self.update_keypresses()