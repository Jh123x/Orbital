import pygame
from .. import State, WHITE, Screen, ImageObject


class Popup(Screen):
    def __init__(self, popup_width: int, popup_height: int, sentence: str, tick_life: int, initial_x: int,
                 initial_y: int, screen, font=False, debug: bool = False):
        """Main Popup class"""

        # Store variables
        self.ttl = tick_life
        self.sentence = sentence
        self.image = []
        width, height = font.size(sentence)

        # Call the Screen superclass init
        super().__init__(popup_width, popup_height, State.NONE, screen, initial_x - popup_width // 2, initial_y,
                         debug)

        # Fill itself black
        self.set_background((0, 0, 0))

        # If no font is set
        if not font:
            # Default to screen.font
            font = self.font

        # Render the words for the popup
        self.write(font, WHITE, sentence, popup_width // 2, popup_height // 2)

    def add_sprite(self, image, x: int, y: int):
        """Add the sprite to x,y in the popup"""
        self.image.append(ImageObject(x, y, 50, 50, image))

    def update(self):
        """Update function for the popup"""
        # If time to live > 0
        if self.ttl:

            # Draw the images
            for img in self.image:
                img.draw(self.screen)

            # Reduce the ttl of the popup
            self.ttl -= 1

            # Call the superclass update
            super().update()

            # Return itself
            return self
        else:
            return None
