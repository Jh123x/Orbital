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

class MenuScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Constructor for the menu screen
            Arguments:
                screen_width: the width of the game in pixels (int)
                screen_height: the height of the game in pixels (int)
                screen: The screen that it is blited to (pygame.Surface)
                debug: Toggles debug mode (bool)

            Methods:
                update_keypress: Checks for the keypress of the player and mutate relavant states
                check_mouse: Check for the user's click on the screen
                handle: Handles the drawing and updating of the objects on the screen
        """
        #Call the superclass
        super().__init__(screen_width, screen_height, State.MENU, screen, 0, 0, debug)

        #Draw the title
        self.write(Screen.title_font, WHITE, "Space Invaders", self.screen_width//2, self.screen_height//5)

        #Draw the Play button
        self.rect_play = self.write(Screen.end_font,WHITE, "Play", self.screen_width//2, self.screen_height//2)

        #Draw the highscore button
        self.rect_highscore = self.write(Screen.end_font, WHITE, "High Score", self.screen_width//2, self.screen_height//15 + self.screen_height//2)

        #Draw the instructions button
        self.rect_instruction = self.write(Screen.end_font, WHITE, "Instructions", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

        #Draw the quit button
        self.rect_end = self.write(Screen.end_font, WHITE, "Quit", self.screen_width//2, self.screen_height//5 + self.screen_height//2)


    def update_keypresses(self) -> State:
        """Track the keypress for the menu
            Arguments:
                No arguments
            Returns: 
                Returns the State of the next game (State)
                or 
                None if there are no relavant keys which are pressed
        """
        #Get the keypresses of the user
        keys = pygame.key.get_pressed()

        #Check if the user press the return key
        if keys[K_RETURN]:

            #Start the game
            return State.PLAY

        else:
            #Otherwise return none
            return None

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
        return state if state else self.check_mouse([self.rect_play, self.rect_end, self.rect_highscore, self.rect_instruction],[State.PLAY,State.QUIT, State.HIGHSCORE, State.INSTRUCTIONS])
