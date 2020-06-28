import pygame
from pygame.locals import *
from . import Screen, Popup
from .. import WHITE, State

class TwoPlayerScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Constructor for the main class for the 2 player screen"""

        #Call the superclass screen
        super().__init__(screen_width, screen_height, State.TWO_PLAYER_MENU, screen, 0, 0, debug)

        #Draw the first pixel used for alignment
        first_pixel = self.screen_height // 2

        #Draw the header
        self.write(Screen.title_font, WHITE, "2 player modes", self.screen_width // 2 ,self.screen_height // 5) 

        #Draw the modes
        #Draw the coop with AI mode
        self.ai_coop = self.write(Screen.end_font, WHITE, "Coop with AI", self.screen_width // 2, first_pixel)

        #Draw the ai versus mode
        self.ai_vs = self.write(Screen.end_font, WHITE, "Versus AI", self.screen_width // 2, first_pixel + self.screen_height // 15)

        #Draw the Player vs player mode
        self.local_vs = self.write(Screen.end_font, WHITE, "Player VS Player", self.screen_width // 2, first_pixel + self.screen_height // 7.5)

        #Draw the Player and Player Coop
        self.coop = self.write(Screen.end_font, WHITE, "2 Player Coop", self.screen_width // 2, first_pixel + self.screen_height // 5)

        #Draw the back button
        self.back = self.write(Screen.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

        #Popup to show that it is still under construction
        self.popup = None
    
    def check_mouse_press(self) -> State:
        """Check the mouse press of the user"""

        #Check if the person clicked on the AI Coop rect
        if self.check_clicked(self.ai_coop):
            self.popup = Popup(200, 20, "Still under construction", 60, self.screen_width//2, 10, self.screen, font = Screen.font, debug = self.debug)
            #Return the AI Coop mode state
            return State.AI_COOP

        #Check if the person clicked on the AI Vs rect
        elif self.check_clicked(self.ai_vs):

            #Return the AI Vs mode state
            return State.AI_VS
        
        #Check if the pereson clicked on the 
        elif self.check_clicked(self.local_vs):
            self.popup = Popup(200, 20, "Still under construction", 60, self.screen_width//2, 10, self.screen)
            #Return the local PVP state
            return State.PVP

        #If the player clicked on the back key
        elif self.check_clicked(self.back):

            #Return the previous screen
            return State.PLAYMODE

        #If the person clicked on coop
        elif self.check_clicked(self.coop):

            #Return the Coop mode
            return State.COOP

        #Otherwise
        return State.TWO_PLAYER_MENU


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

              