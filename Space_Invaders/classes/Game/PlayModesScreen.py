#Play mode screen
import pygame
from pygame.locals import *
try:
    from .Enums import State
    from .Screens import Screen
    from .Colors import WHITE
except:
    from Enums import State
    from Screens import Screen
    from Colors import WHITE

class PlayModeScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Main screen for the different play modes"""

        #Call the super class
        super().__init__(screen_width, screen_height, State.PLAYMODE, screen, 0, 0, debug)

        #First pixel for alignment
        first_pixel = self.screen_height // 2 + 100

        #Draw the Header
        self.header = self.write(Screen.title_font, WHITE, "Modes", self.screen_width//2, self.screen_height//4)

        #Draw the rectangles for the different game modes
        #Rectangle for the endless mode (Default)
        self.play = self.write(Screen.end_font, WHITE, "Endless Mode", self.screen_width//2, first_pixel)

        #2 Player mode (2 player mode menu)
        self.two_player = self.write(Screen.end_font, WHITE, "2 Player mode", self.screen_width//2, first_pixel + self.screen_height//15)

        #Back button
        self.back = self.write(Screen.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height//1.2)

    def check_mouse_clicks(self) -> State:
        """Check the button that the player pressed"""

        #If the endless mode play button is pressed
        if self.check_clicked(self.play):

            #Go to the play state
            return State.PLAY

        #If the two player mode is pressed, go to the 2 player mode
        elif self.check_clicked(self.two_player):

            #Go to the two player mode menu
            return State.TWO_PLAYER_MENU

        #If the player press the back button
        elif self.check_clicked(self.back):

            #Go to the main menu after that
            return State.MENU

        #Otherwise the player has not decided
        return False

    def check_keypresses(self) -> State:
        """Check the keyboard inputsof the user"""
        #Get the keypresses that the user pressed
        keys = pygame.key.get_pressed()

        #Check if the esc key is pressed
        if keys[K_ESCAPE]:
            return State.MENU

        #Otherwise
        else:

            #Return the current mode
            return self.state

    def handle(self):
        """Method to handle the drawing of the screen"""
        #Update the sprites
        self.update()

        #Check the clicks
        state = self.check_mouse_clicks()

        #If the player has not clicked, check the keypresses
        return state if state else self.check_keypresses()