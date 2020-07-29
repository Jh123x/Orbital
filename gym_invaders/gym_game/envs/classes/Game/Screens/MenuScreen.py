import pygame
from pygame.locals import *
from . import Screen
from .. import State, WHITE

class MenuScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Constructor for the Main Menu screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.MENU, screen, 0, 0, debug)

        #Draw the title
        self.write(self.title_font, WHITE, "Space Invaders", self.screen_width//2, self.screen_height//5)

        #Draw the Play button
        self.rect_play = self.write(self.end_font,WHITE, "Play", self.screen_width//2, self.screen_height//2)

        #Draw the highscore button
        self.rect_highscore = self.write(self.end_font, WHITE, "High Score", self.screen_width//2, self.screen_height//15 + self.screen_height//2)

        #Draw the instructions button
        self.rect_instruction = self.write(self.end_font, WHITE, "Instructions", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

        #Draw the settings button
        self.rect_settings = self.write(self.end_font, WHITE, "Settings", self.screen_width//2, self.screen_height//5 + self.screen_height//2)

        #Draw the quit button
        self.rect_end = self.write(self.end_font, WHITE, "Quit", self.screen_width//2, self.screen_height//1.2)


    def update_keypresses(self) -> State:
        """Track the keypress for the menu"""

        #Get the keypresses of the user
        keys = pygame.key.get_pressed()

        #Check if the user press the return key
        if keys[K_RETURN]:

            #Start the game
            return State.PLAYMODE

    def check_mouse(self, rects:list, states:list):
        """Check the position of the mouse on the menu to see what the player clicked
            Arguments:
                rects: List of Rects to be checked (list of pygame.Rects)
                states: List of states to be returned if it is clicked (list of States)
            Return:
                Returns the next state of the game (State)
        """
        
        #Iterate through each of the rects
        for i in range(len(rects)):

            #Check if the rect is clicked
            if self.check_clicked(rects[i]):

                #Return the state if it is clicked
                return states[i]

        #Otherwise return the Menu state
        return State.MENU

    def handle(self) -> State:
        """Load the Menu onto the screen
            Arguments:
                No Arguments
            Returns:
                Returns the State the game should be in (State)
        """
        #Update the screen
        self.update()

        #Check for keypress of user
        state = self.update_keypresses()

        #Check the position of the mouse to return the state and combine it with the keypress of user
        return state if state else self.check_mouse([self.rect_play, self.rect_end, self.rect_highscore, self.rect_instruction, self.rect_settings],[State.PLAYMODE,State.QUIT, State.HIGHSCORE, State.INSTRUCTIONS_MENU, State.SETTINGS])
