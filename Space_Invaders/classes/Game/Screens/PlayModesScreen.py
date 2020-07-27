#Play mode screen
import pygame
from pygame.locals import *
from . import Screen
from .. import State, WHITE

class PlayModeScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Main screen for the different play modes"""

        #Call the super class
        super().__init__(screen_width, screen_height, State.PLAYMODE, screen, 0, 0, debug)

        #First pixel for alignment
        first_pixel = self.screen_height // 2

        #Draw the Header
        self.header = self.write(Screen.title_font, WHITE, "Modes", self.screen_width//2, self.screen_height//5)

        #Draw the rectangles for the different game modes
        #Rect for tutorial
        tutorial = self.write(Screen.end_font, WHITE, "Tutorial", self.screen_width//2, first_pixel)

        #Rect for AI modes
        ai_modes = self.write(Screen.end_font, WHITE, "AI modes", self.screen_width //2, first_pixel + self.screen_height//15)

        #Rect for the single player mode
        one_player = self.write(Screen.end_font, WHITE, "1 Player modes", self.screen_width //2, first_pixel + self.screen_height//7.5)

        #2 Player mode (2 player mode menu)
        two_player = self.write(Screen.end_font, WHITE, "2 Player Modes", self.screen_width//2, first_pixel + self.screen_height//5)

        #Back button
        back = self.write(Screen.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height//1.2)

        #Store all the buttons
        self.buttons = [tutorial, ai_modes, one_player, two_player, back]
        self.modes = [State.TUTORIAL, State.AI_MENU, State.ONE_PLAYER_MENU, State.TWO_PLAYER_MENU, State.MENU]

    def check_mouse_clicks(self) -> State:
        """Check the button that the player pressed"""

        #Check if any buttons were clicked
        result = tuple(map(lambda x: self.check_clicked(x), self.buttons))

        #Iterate through the clicks
        for index, click in enumerate(result):

            #If anything was clicked
            if click:

                #Return the corresponding mode
                return self.modes[index]

        #Otherwise the player has not decided
        return False

    def check_keypresses(self) -> State:
        """Check the keyboard inputsof the user"""
        #Check if any buttons were clicked
        result = tuple(map(lambda x: self.check_clicked(x), self.buttons))

        #Iterate through the clicks
        for index, click in enumerate(result):

            #If anything was clicked
            if click:

                #Return the corresponding mode
                return self.modes[index]

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