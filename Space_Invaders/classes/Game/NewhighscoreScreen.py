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
    inputbox = InputBox(300, 400, 30, Screen.end_font)
    def __init__(self, game_width:int, game_height:int, screen:int, score:int):

        #Call the superclass
        super().__init__(game_width, game_height, State.NEWHIGHSCORE, screen)

        #Define new variables
        self.score = score
        
        #Draw the sprites
        self.draw()

    @staticmethod
    def get_name() -> str:
        return NewhighscoreScreen.inputbox.get_text()

    def draw(self) -> None:
        start_px = 100
        #Tell the user he has a new high score
        self.write(self.title_font, WHITE, f"NEW HIGH SCORE", self.game_width//2, start_px)

        #Tell the user to key in his name
        self.write(self.font, WHITE, f"Please key in your name and press enter", self.game_width//2, start_px + self.game_height//10)

        #Draw the Box
        NewhighscoreScreen.inputbox.blit(self.screen)
    
    def handle(self) -> State:
        """Tell the user that he got a new highscore and enter his name"""
        #Handle the keying in of name
        for event in tuple(filter(lambda x: x.type==pygame.KEYDOWN, pygame.event.get())):
            if event.key == K_BACKSPACE:
                NewhighscoreScreen.inputbox.backspace()
            elif event.key != K_RETURN:
                NewhighscoreScreen.inputbox.add(event.unicode)
            else:
                return State.GAMEOVER

        #Update the Inputbox
        NewhighscoreScreen.inputbox.update()

        #Draw the sprites
        self.draw()
        
        #Update the surface
        self.update()

        return State.NEWHIGHSCORE