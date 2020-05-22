import pygame
from pygame.locals import *
try:
    from .Colors import *
except ImportError:
    from Colors import *

class InputBox(object):
    def __init__(self, initial_x:int, initial_y:int, height:int, font, max_length = 10):
        """Constructor for the inputbox"""
        self.text = []
        self.max_length = max_length
        self.x = initial_x
        self.y = initial_y
        self.height = height
        self.color = WHITE
        self.font = font
        self.update()

    def update(self) -> None:
        """Update the InputBox"""
        self.width = len(self.text)*15
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
    
    def clear(self) -> None:
        """Clear the input"""
        self.text.clear()

    def add(self, char:str) -> None:
        """Add input"""
        if len(self.text) <= self.max_length:
            self.text.append(char.strip())

    def blit(self, screen):
        screen.blit(self.font.render(self.get_text(), True, WHITE), self.rect)

    def backspace(self) -> None:
        """Remove the last letter"""
        #If the text is not empty
        if self.text:
            #Remove the last character
            self.text.pop()

    def get_text(self) -> str:
        """Get what is in the inputbox"""
        return "".join(self.text)
        
def main():
    pygame.font.init()
    screen = pygame.display.set_mode((100,100))
    box = InputBox(50,50,50,pygame.font.Font(pygame.font.get_default_font(),15))
    while True:
        for event in tuple(filter(lambda x: x.type==pygame.KEYDOWN, pygame.event.get())):
            if event.key == K_BACKSPACE:
                print("Backspace")
                box.backspace()
            elif event.key != K_RETURN:
                print(event.unicode)
                box.add(event.unicode)
            else:
                print("Return")
                return
        box.update()
        box.blit(screen)
        print(box.get_text())

if __name__ == '__main__':
    main()


