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
    def __init__(self, game_width:int, game_height:int, screen):
        """Constructor for the menu screen
            Arguments:
                game_width: the width of the game in pixels
                game_height: the height of the game in pixels
                screen: The screen that it is blited to
        """
        #Call the superclass
        super().__init__(game_width, game_height, State.MENU, screen)

        #Draw the title
        self.write(Screen.title_font, WHITE, "Space Invaders", self.game_width//2, self.game_height//5)

        #Draw the Play button
        self.rect_play = self.write(Screen.end_font,WHITE, "Play", self.game_width//2, self.game_height//2)

        #Draw the highscore button
        self.rect_highscore = self.write(Screen.end_font, WHITE, "High Score", self.game_width//2, self.game_height//15 + self.game_height//2)

        #Draw the instructions button
        self.rect_instruction = self.write(Screen.end_font, WHITE, "Instructions", self.game_width//2, self.game_height//7.5 + self.game_height//2)

        #Draw the quit button
        self.rect_end = self.write(Screen.end_font, WHITE, "Quit", self.game_width//2, self.game_height//5 + self.game_height//2)


    def update_keypresses(self) -> State:
        """Track the keypress for the menu
            Arguments:
                No arguments
            Returns: 
                Returns the State of the next game
        """
        #Get the keypresses of the user
        keys = pygame.key.get_pressed()

        #Check if the user press the return key
        if keys[K_RETURN]:

            #Start the game
            return State.PLAY

        #Check if the user epressed the escape key
        elif keys[K_ESCAPE]:

            #Quit the game
            return State.QUIT

        else:

            #Otherwise return none
            return None


    def check_mouse_pos(self, rects, states):
        """Check the position of the mouse on the menu to see what the player clicked
            Arguments:
                rect_play: Rectangle containing the play button
                rect_end: Rectangle containing the end button
                rect_highscore: Rectangle containing the highscore button
                rect_instructions: Rectangle containing the highscore button
            Return:
                Returns the next state of the game
        """
        for i in range(len(rects)):
            if self.check_clicked(rects[i]):
                return states[i]

        return State.MENU

    def handle(self) -> State:
        """Load the Menu onto the screen
            Arguments:
                No Arguments
            Returns:
                Returns the State the game should be in
        """
        self.update()

        #Get the keypresses of the player
        state = self.update_keypresses()

        #Check the position of the mouse to return the state
        return state if state else self.check_mouse_pos([self.rect_play, self.rect_end, self.rect_highscore, self.rect_instruction],[State.PLAY,State.QUIT, State.HIGHSCORE, State.INSTRUCTIONS])
