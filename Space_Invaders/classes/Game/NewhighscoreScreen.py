import pygame
from pygame.locals import *
try:
    from .Screens import Screen
    from .Enums import State, Direction
    from .Colors import WHITE
    from .InputBox import InputBox
except ImportError:
    from Screens import Screen
    from Enums import State, Direction
    from Colors import WHITE
    from InputBox import InputBox

class NewhighscoreScreen(Screen):

    #Input box for the player to key in his name
    inputbox = InputBox(300, 400, 30, Screen.end_font)

    def __init__(self, game_width:int, game_height:int, screen, score:int, debug:bool = False):
        """Main screen for the new highscore screen
            Arguments:
                game_width: Width of the game in pixels (int)
                game_height: Height of the game in pixels (int)
                screen: Surface to blit our screen onto (pygame.Surface)
                score: Score that the player obtained (int)
                debug: Toggles debugging on the screen (bool): default = False
            
            Static Methods: 
                get_name: Get the name that the player input into the inputbox
            
            Methods:
                draw: Draw the screen onto the surface
                handle: Handles the drawing of the screen onto the surface
        """
        #Call the superclass
        super().__init__(game_width, game_height, State.NEWHIGHSCORE, screen, debug)

        #Define new variables
        self.score = score
        
        #Draw the sprites
        self.draw()

    @staticmethod
    def get_name() -> str:
        """Get the name of that was keyed into the inputbox
            Arguments:
                No arguments
            Returns:
                Returns the string that was inputted (string)
        """
        return NewhighscoreScreen.inputbox.get_text()

    def draw(self) -> None:
        """Draw the Screen onto the Surface
            Arguments: 
                No arguments
            Return: 
                No return
        """

        #Start pixel to start drawing
        start_px = 100

        #Tell the user he has a new high score
        self.write(self.title_font, WHITE, f"NEW HIGH SCORE", self.game_width//2, start_px)

        #Tell the user to key in his name
        self.write(self.font, WHITE, f"Please key in your name and press enter", self.game_width//2, start_px + self.game_height//10)

        #Draw the inputbox
        NewhighscoreScreen.inputbox.blit(self.screen)
    
    def handle(self) -> State:
        """Handles the new highscore and get user's name from input
            Arguments: 
                No arguments
            Returns: 
                No return
        """
        #Check each keydown event in pygame event queue
        for event in tuple(filter(lambda x: x.type==pygame.KEYDOWN, pygame.event.get())):

            #Check if it is the backspace key
            if event.key == K_BACKSPACE:

                #Do backspace on the inputbox
                NewhighscoreScreen.inputbox.backspace()

            #Check if the player hit any other key
            elif event.key != K_RETURN:

                #Add the character to the inputbox
                NewhighscoreScreen.inputbox.add(event.unicode)

            #If the player hit the return key
            else:

                #Return Gameover State
                return State.GAMEOVER

        #Update the Inputbox
        NewhighscoreScreen.inputbox.update()

        #Draw the sprites
        self.draw()
        
        #Update the surface
        self.update()

        #Return the Current game state
        return State.NEWHIGHSCORE