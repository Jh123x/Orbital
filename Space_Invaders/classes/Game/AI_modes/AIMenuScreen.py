#Play mode screen
import pygame
from pygame.locals import *
from .. import State, WHITE, Screen

class AIMenuScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Main screen for the different play modes"""

        #Call the super class
        super().__init__(screen_width, screen_height, State.AI_MENU, screen, 0, 0, debug)

        #Draw the first pixel
        first_pixel = self.screen_height // 2

        #Draw the header
        self.write(self.title_font, WHITE, "AI Modes", self.screen_width // 2 ,self.screen_height // 5)

        #Draw the coop with AI mode
        self.ai_coop = self.write(self.end_font, WHITE, "Coop with AI", self.screen_width // 2, first_pixel)

        #Draw the ai versus mode
        self.ai_vs = self.write(self.end_font, WHITE, "Versus AI", self.screen_width // 2, first_pixel + self.screen_height // 15)

        #Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

        #Initialise the popup
        self.popup = None

    def check_mouse_press(self) -> State:
        """Check the mouse press of the user"""

        #Check if the person clicked on the AI Coop rect
        if self.check_clicked(self.ai_coop):

            #Return the AI Coop mode state
            return State.AI_COOP

        #Check if the person clicked on the AI Vs rect
        elif self.check_clicked(self.ai_vs):

            #Return the AI Vs mode state
            return State.AI_VS

        #Check if the person clicked on the back button
        elif self.check_clicked(self.back):

            #Return to the play menu
            return State.PLAYMODE

        #Otherwise return current state
        return self.state

    def handle(self) -> State:
        """Handle the drawing of the 2 players screen"""

        #If there is a popup
        if self.popup:
            
            #Update the popup
            self.popup.update()

        #Update the screen
        self.update()

        #Check the mouse press and return the correct state
        return self.check_mouse_press()