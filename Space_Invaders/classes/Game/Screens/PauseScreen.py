import pygame
from pygame.locals import *
from . import Screen
from .. import State, WHITE

class PauseScreen(Screen):

    #Check if the pause sound has been played
    sound = None
    played = False

    def __init__(self, screen_width:int, screen_height:int, screen, score:int, previous_state: State, debug:bool = False):
        """Main class for the pause screen"""
        
        #If there is a pausescreen sound
        if PauseScreen.sound and not PauseScreen.played:

            #Play the pause screen sound
            PauseScreen.sound.play('pause')
            PauseScreen.played = True

        #Call the superclass
        super().__init__(screen_width, screen_height, State.PAUSE, screen, 0, 0, debug)

        #Store the score
        self.score = score

        #Store the previous state
        self.previous_state = previous_state

        #Set a cooldown
        self.cooldown = 20

        #Write the lines
        self.write_lines()
        
    def write_lines(self):
        """Write the lines required for Pause screen"""
        #Draw the title of the pause screen
        self.write(self.title_font, WHITE, "Paused", self.screen_width//2, self.screen_height//5)
        
        #Draw the score of the person currently
        self.write(self.subtitle_font, WHITE, f"Score: {self.score}", self.screen_width//2, self.screen_height//2)

        #Draw the instructions on how to quit/unpause
        self.write(self.end_font, WHITE, f"Click on the button or the shortcut", self.screen_width//2, self.screen_height//2 + self.screen_height // 15)

        #Draw the instructions to unpause
        self.unpause = self.write(self.end_font, WHITE, "Unpause (P)", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

        #Draw the instructions to quit
        self.quit = self.write(self.end_font, WHITE, "Quit (Esc)", self.screen_width//2, self.screen_height//5 + self.screen_height//2)

    def get_score(self) -> int:
        """Get the score displayed for the pause screen"""
        return self.score

    def update_keypresses(self) -> State:
        """Check for the keypresses within the pause screen"""

        #Getting the keys which are pressed
        keys = pygame.key.get_pressed()

        #If the button is still under cooldown
        if not self.cooldown:

            #Return the play state if the player unpause his game
            if keys[K_p]:
                PauseScreen.played = False
                self.cooldown = 20
                return self.previous_state

            #If the player press the escape key, quit the game
            if keys[K_ESCAPE]:
                PauseScreen.played = False
                self.cooldown = 20
                return State.MENU
        
        #Return the current state if the player has not unpaused
        return self.state

    def check_clicks(self):
        """Check the clicks done by the player"""

        #If the player clicked on the quit button
        if self.check_clicked(self.quit):
            PauseScreen.played = False
            self.cooldown = 20
            return State.MENU
            
        #If the player clicked on the unpause button
        elif self.check_clicked(self.unpause):
            PauseScreen.played = False
            self.cooldown = 20
            return self.previous_state

        #Otherwise
        return None

    def handle(self) -> State:
        """Handles the drawing of the pause screen"""
        #Update the screen itself
        self.update()

        if self.cooldown:
            self.cooldown -= 1

        #Detect the keypress
        state = self.check_clicks()
        return self.update_keypresses() if not state else state