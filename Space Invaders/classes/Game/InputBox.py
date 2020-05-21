import pygame
from .Colors import *

class InputBox(object):
    def __init__(self, initial_x:int, initial_y:int, width:int, height:int, font, max_length = 5):
        """Constructor for the inputbox"""
        self.text = []
        self.max_length = max_length
        self.rect = pygame.Rect(initial_x, initial_y, width, height)
        self.rect.center = (initial_x, initial_y)
        self.color = WHITE
        self.font = font

    def update(self) -> None:
        """Update the InputBox"""
        width = max(self.max_length, len(self.text))
        self.rect.w = width

    def draw(self, screen) -> None:
        """Draw the input box"""
        screen.blit(self.font.render(f"{self.text}", True, self.color), self.rect)

    def input(self, char:str) -> None:
        """Add input"""
        self.text.append(char)

    def backspace(self) -> None:
        """Remove the last letter"""

        #If the text is not empty
        if self.text:

            #Remove the last character
            self.text.pop()

    def get_text(self) -> str:
        """Get what is in the inputbox"""
        return self.__str__()

    def __str__(self) -> str:
        return "".join(self.text)

    def __repr__(self) -> str:
        return "".join(self.text)