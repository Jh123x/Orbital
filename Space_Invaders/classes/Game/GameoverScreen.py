import pygame
from pygame.locals import *
try:
    from .Screens import Screen
    from .Enums import State
    from .Colors import WHITE
except ImportError:
    from Screens import Screen
    from .Enums import State
    from .Colors import WHITE

class GameoverScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen, score:int, new_high_score:bool, debug:bool = False):
        """Initialize the gameoverScreen class"""
        #Store the variables
        self.highscore = new_high_score
        self.score = score

        #Call the superclass method
        super().__init__(game_width, game_height, State.GAMEOVER, screen)

        #Draw the words for gameover
        self.write(self.title_font, WHITE, "Game Over", self.game_width//2, self.game_height//5)

        #Draw the score
        self.write(self.end_font, WHITE,"Score : " + str(self.score),self.game_width // 2, self.game_height // 2)

        #Prompt player to update
        self.write(self.end_font, WHITE, "Press Y to go back and N to quit", self.game_width//2, self.game_height // 2 + self.game_height//12)
        
    def update_keypresses(self) -> bool:
        """Check if player wants to stay"""
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #Check for y key
        if keys[K_y]:
            return True

        #Check for n key
        elif keys[K_n]:
            return False
        
        #Otherwise return None for it to be asked in the next iteration
        else:
            return None

    def handle(self) -> State:
        """Handles drawing of the gameover screen"""
        #Update itself into the screen
        self.update()

        #Update the stay status
        stay = self.update_keypresses()

        #If the player wants to stay
        if stay:
            return State.MENU
        
        #If the player does not want to stay
        elif stay == False:
            return State.QUIT

        #Otherwise keep on drawing
        else:
            
            #Return the gameover state
            return State.GAMEOVER