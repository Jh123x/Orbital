import pygame
import random
from pygame.locals import *
from . import Screen
from .. import State, WHITE, Direction

class TwoPlayerGameoverScreen(Screen):

    #Check if the sound is played
    sound = None
    played = False

    def __init__(self, screen_width:int, screen_height:int, screen, p1_score:int, p2_score:int, debug:bool = False):
        """Constructor for the Two Player Gameover class"""
        if not TwoPlayerGameoverScreen.played and TwoPlayerGameoverScreen.sound:
            TwoPlayerGameoverScreen.sound.play('gameover')
            TwoPlayerGameoverScreen.played = True
        
        #Call the superclass
        super().__init__(screen_width, screen_height, State.TWO_PLAYER_GAMEOVER, screen, 0, 0, debug)

        #Store extra vars
        self.p1_score = p1_score
        self.p2_score = p2_score

        #Draw the scores on the screen
        self.write(Screen.title_font, WHITE, f"Game over", self.screen_width//2, self.screen_height//5)

        #Draw the winner
        if p1_score > p2_score:
            self.write(Screen.subtitle_font, WHITE, f"Player 1 Wins", self.screen_width//2, self.screen_height//2 - 120)
        elif p1_score == p2_score:
            self.write(Screen.subtitle_font, WHITE, f"Its a draw", self.screen_width//2, self.screen_height//2 - 120)
        else:
            self.write(Screen.subtitle_font, WHITE, f"Player 2 Wins", self.screen_width//2, self.screen_height//2 - 120)


        #Draw the scores of each of the players
        self.write(Screen.end_font, WHITE, f"Player 1 score: {self.p1_score}", self.screen_width//4, self.screen_height//2, Direction.LEFT)
        self.write(Screen.end_font, WHITE, f"Player 2 score: {self.p2_score}", self.screen_width//4, self.screen_height//2 + 45, Direction.LEFT)

        #Draw instructions to go back
        self.write(self.end_font, WHITE, "Press Y to go back and N to quit", self.screen_width//2, self.screen_height // 2 + self.screen_height//6)

    def get_scores(self) -> tuple:
        """Return the scores of the players"""
        return self.p1_score,self.p2_score

    def update_keypresses(self) -> bool:
        """Check if the player wants to play"""
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #Check for y key to indicate he wants to go back to menu
        if keys[K_y]:
            TwoPlayerGameoverScreen.played = True
            return True

        #Check for n key to indicate that the player wants to leave
        elif keys[K_n]:
            return False
        
        #Otherwise return None for it to be asked in the next iteration
        else:
            return None

    def handle(self) -> State:
        """Handle the drawing of the multiplayer gameover screen"""
        #Update the sprites
        self.update()

        #Update the keypresses
        stay = self.update_keypresses()

        #Check if player wants to stay
        if stay:

            #Reset sound played
            TwoPlayerGameoverScreen.played = False

            #Return to Main menu
            return State.MENU

        elif stay == False:

            #Reset sound played
            TwoPlayerGameoverScreen.played = False
            
            #Return Quit state
            return State.QUIT
        else:
            return self.state
