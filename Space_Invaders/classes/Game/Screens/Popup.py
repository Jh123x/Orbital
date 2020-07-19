import pygame
from . import Screen
from .. import State, Direction, WHITE

class Popup(Screen):
    def __init__(self, popup_width:int, popup_height:int, sentence:str, tick_life:int, initial_x:int, initial_y:int, screen, font = False, debug:bool = False):
        """Main Popup class"""

        #Store variables
        self.ttl = tick_life
        self.sentence = sentence

        #Call the Screen superclass init
        super().__init__(popup_width, popup_height, State.NONE, screen, initial_x - (len(sentence) * 5), initial_y, debug)

        #Fill itself black
        self.set_background((0,0,0))

        #If no font is set
        if not font:

            #Default to screen.font
            font = Screen.font

        #Render the words for the popup
        self.write(font, WHITE, sentence, popup_width // 2, popup_height//2)

    def update(self):
        """Update function for the popup"""
        #If time to live > 0
        if self.ttl:

            #Reduce the ttl of the popup
            self.ttl -= 1

            #Call the superclass update
            super().update()

            #Return itself
            return self
        else:
            return None