import pygame
from pygame.locals import *
from . import Screen
from .. import State, WHITE

class GameoverScreen(Screen):
    sound = None
    played = False
    def __init__(self, screen_width:int, screen_height:int, screen, score:int, debug:bool = False):
        """Initialize the gameoverScreen class
            Arguments:
                screen_width: Width of the game in terms of pixels (int)
                screen_height: Height of the game in terms of pixels (int)
                screen: Surface to draw the screen onto (pygame.Surface)
                score: Score of the player (int)
                debug: Toggles debug mode (bool): default = False

            Methods:
                update_keypress: detects the keypress of the player
                handle: handles the drawing of the screen onto the surface and internal state
        """

        #If sound exist and have not been played
        if not GameoverScreen.played and GameoverScreen.sound:

            #Play the sound
            GameoverScreen.sound.play('gameover')

            #Set sound played to true
            GameoverScreen.played = True

        #Store the variables
        self.score = score

        #Call the superclass method
        super().__init__(screen_width, screen_height, State.GAMEOVER, screen, 0, 0, debug)

        #Draw the words for gameover
        self.write(self.title_font, WHITE, "Game Over", self.screen_width//2, self.screen_height//5)

        #Draw the score
        self.write(self.end_font, WHITE,"Score : " + str(self.score),self.screen_width // 2, self.screen_height // 2)

        #Prompt player to update
        self.write(self.end_font, WHITE, "Press Y to go back and N to quit", self.screen_width//2, self.screen_height // 2 + self.screen_height//12)

    def get_score(self):
        """Return the score of the player"""
        return self.score
        
    def update_keypresses(self) -> bool:
        """Check if player wants to stay
            Arguments: 
                No arguments
            Returns: 
                Returns a bool to determine if the player wants to stay (bool)
        """
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #Check for y key to indicate he wants to go back to menu
        if keys[K_y]:
            return True

        #Check for n key to indicate that the player wants to leave
        elif keys[K_n]:
            return False
        
        #Otherwise return None for it to be asked in the next iteration
        else:
            return None

    def handle(self) -> State:
        """Handles drawing of the gameover screen
            Arguments:
                No argument
            Returns: 
                Return the next state the game should be in (State)
        """
        #Update itself into the screen
        self.update()

        #Update the stay status
        stay = self.update_keypresses()

        #If the player wants to stay
        if stay:

            #Reset sound played to False
            GameoverScreen.played = False

            #Return next state to be menu
            return State.MENU
        
        #If the player does not want to stay
        elif stay == False:

            #Return the quit state
            return State.QUIT

        #Otherwise keep on drawing gameover screen
        else:
            
            #Return the gameover state
            return State.GAMEOVER