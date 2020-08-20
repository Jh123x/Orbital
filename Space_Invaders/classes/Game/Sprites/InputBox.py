import pygame
from pygame.locals import *

from .. import WHITE


class InputBox(object):
    def __init__(self, initial_x: int, initial_y: int, height: int, font, max_length: int = 10):
        """Constructor for the inputbox"""

        # Store the variables
        self.text = []
        self.max_length = max_length
        self.x = initial_x
        self.y = initial_y
        self.height = height
        self.color = WHITE
        self.font = font

        # Update the rect of the inputBox
        self.update()

    def update(self) -> None:
        """Update the InputBox"""

        # Set the width of the input box
        self.width = len(self.text) * 15

        # Draw the rect for box
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Set the center for box
        self.rect.center = (self.x, self.y)

    def clear(self) -> None:
        """Clear the input"""
        self.text.clear()

    def add(self, char: str) -> None:
        """Add input"""
        if char != '' and len(self.text) <= self.max_length:
            self.text.append(char)

    def blit(self, screen) -> None:
        """Draw the inputbox onto the screen"""
        screen.blit(self.font.render(self.get_text(), True, self.color), self.rect)

    def backspace(self) -> None:
        """Remove the last letter"""
        # If the text is not empty
        if self.text:
            # Remove the last character
            self.text.pop()

    def get_text(self) -> str:
        """Get input in inputbox"""
        return "".join(self.text)
